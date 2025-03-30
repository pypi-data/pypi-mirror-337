import asyncio
from collections import deque
from typing import Any, Deque, Dict, Optional

import paho.mqtt.client as mqtt
from aioworkers.core.base import AbstractConnector
from aioworkers.core.formatter import FormattedEntity
from aioworkers.queue.base import AbstractQueue
from aioworkers.storage.base import AbstractStorage


class Base(AbstractConnector, FormattedEntity):
    _client: mqtt.Client
    _mids: Dict[int, asyncio.Future]

    def set_config(self, config):
        super().set_config(config)
        self._host = self.config.get("host", default="localhost")
        self._port = self.config.get("port") or 1883

        if client_id := self.config.get("client_id"):
            client_id = str(client_id)
        self._client_id = client_id

        self._qos = self.config.get_int("qos", default=0)
        self._retain = self.config.get_int("retain", default=False)

        self._protocol = mqtt.MQTTv311
        protocol = self.config.get("protocol")
        if protocol in ("5", 5):
            self._protocol = mqtt.MQTTv5
        elif protocol in ("3.1", 3.1):
            self._protocol = mqtt.MQTTv31

        self._user = self.config.get("user")
        self._password = self.config.get("password")

    async def init(self):
        self._mids = {}
        self._connected = asyncio.Event()
        await super().init()
        self._client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            protocol=self._protocol,
            client_id=self._client_id,
        )
        if self._user or self._password:
            self._client.username_pw_set(self._user, self._password)
        self._client.on_message = self._on_message
        self._client.on_publish = self._on_publish
        self._client.on_connect = self._on_connect

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        self.loop.call_soon_threadsafe(self._connected.set)
        self.logger.info(f"Connected to {self._host}:{self._port} with result code {reason_code}")

    async def connect(self):
        self._client.connect_async(
            host=self._host,
            port=self._port,
        )
        self._client.loop_start()
        await self._connected.wait()

    async def disconnect(self):
        self._connected.clear()
        self._client.disconnect()

    def _on_message(self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage):
        raise NotImplementedError

    async def _publish(
        self,
        topic: str,
        payload: Any,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
    ):
        if payload not in (None, ""):
            payload = self.encode(payload)
        assert self._connected.is_set()
        mi = self._client.publish(
            topic,
            payload,
            qos=self._qos if qos is None else qos,
            retain=self._retain if retain is None else retain,
        )
        self.logger.debug("Publish mid %s", mi.mid)
        f = self._loop.create_future()
        self._mids[mi.mid] = f
        return await f

    def _on_publish(
        self,
        client,
        userdata,
        mid: int,
        reason_code,
        properties,
    ):
        self.logger.debug("mid: %s, reason_code: %s, properties: %s", mid, reason_code, properties)
        if f := self._mids.pop(mid, None):
            self.loop.call_soon_threadsafe(f.set_result, mid)


class Storage(Base, AbstractStorage):
    _subscriptions: Dict[str, asyncio.Future[mqtt.MQTTMessage]]

    def __init__(
        self,
        *args,
        prefix: Optional[str] = None,
        **kwargs,
    ):
        self._subscriptions = {}
        self._prefix = prefix
        super().__init__(*args, **kwargs)

    def set_config(self, config):
        super().set_config(config)
        self._prefix = self.config.get("prefix") or self._prefix

    def raw_key(self, key):
        return f"{self._prefix}/{key}" if self._prefix else key

    async def set(
        self,
        key: str,
        value: Any,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
    ):
        key = self.raw_key(key)
        return await self._publish(
            key,
            payload=value,
            qos=qos,
            retain=retain,
        )

    def _on_message(
        self,
        client: mqtt.Client,
        userdata,
        msg: mqtt.MQTTMessage,
    ):
        topic = msg.topic
        self.logger.debug("Message from topic %s", topic)
        if f := self._subscriptions.pop(topic, None):
            self.loop.call_soon_threadsafe(f.set_result, msg)

    async def get(self, key: str):
        assert self._connected.is_set()
        f = self._loop.create_future()
        key = self.raw_key(key)
        self._subscriptions[key] = f
        self._client.subscribe(key, qos=self._qos)
        msg: mqtt.MQTTMessage = await f
        result = self.decode(msg.payload)
        self._client.unsubscribe(key)
        return result


class Queue(Base, AbstractQueue):
    _queue: asyncio.Queue[mqtt.MQTTMessage]

    def __init__(self, *args, **kwargs):
        self._topics: Deque = deque()
        super().__init__(*args, **kwargs)

    def set_config(self, config):
        super().set_config(config)

        topics = set(self.config.topics) - set(self._topics)
        self._topics.extend(topics)
        assert self._topics

        self._limit = self.config.get_int("limit", default=0)

    async def init(self):
        self._queue = asyncio.Queue()
        await super().init()

    def _on_connect(self, *args, **kwargs):
        super()._on_connect(*args, **kwargs)
        topics = [(t, self._qos) for t in self._topics]
        self._client.subscribe(topics)

    async def put(
        self,
        value: Any,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
    ):
        topic = self._topics[0]
        self._topics.rotate()

        return await self._publish(
            topic=topic,
            payload=value,
            qos=qos,
            retain=retain,
        )

    def _on_message(
        self,
        client: mqtt.Client,
        userdata,
        msg: mqtt.MQTTMessage,
    ):
        q = self._queue
        if self._limit and q.qsize() >= self._limit:
            self.loop.call_soon_threadsafe(q.get_nowait)
            self.logger.warning("Dropped message")
        self.loop.call_soon_threadsafe(q.put_nowait, msg)

    async def get(self):
        msg: mqtt.MQTTMessage = await self._queue.get()
        result = self.decode(msg.payload)
        return result
