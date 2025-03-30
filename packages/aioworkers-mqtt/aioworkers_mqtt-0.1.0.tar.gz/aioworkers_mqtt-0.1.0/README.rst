aioworkers-mqtt
===============

.. image:: https://img.shields.io/pypi/v/aioworkers-mqtt.svg
  :target: https://pypi.org/project/aioworkers-mqtt

.. image:: https://github.com/aioworkers/aioworkers-mqtt/workflows/Tests/badge.svg
  :target: https://github.com/aioworkers/aioworkers-mqtt/actions?query=workflow%3ATests

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json
  :target: https://github.com/charliermarsh/ruff
  :alt: Code style: ruff

.. image:: https://img.shields.io/badge/types-Mypy-blue.svg
  :target: https://github.com/python/mypy
  :alt: Code style: Mypy

.. image:: https://readthedocs.org/projects/aioworkers-mqtt/badge/?version=latest
  :target: https://github.com/aioworkers/aioworkers-mqtt#readme
  :alt: Documentation Status

.. image:: https://img.shields.io/pypi/pyversions/aioworkers-mqtt.svg
  :target: https://pypi.org/project/aioworkers-mqtt
  :alt: Python versions

.. image:: https://img.shields.io/pypi/dm/aioworkers-mqtt.svg
  :target: https://pypistats.org/packages/aioworkers-mqtt

.. image:: https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg
  :alt: Hatch project
  :target: https://github.com/pypa/hatch


Features
--------

* Queue over mqtt
* Storage over mqtt


Install
-------

Use uv to add to your project (recommend):

.. code-block:: bash

    uv add aioworkers-mqtt[paho]

or install with pip:

.. code-block:: bash

    pip install aioworkers-mqtt[paho]


Usage
-----

Add this to aioworkers config.yaml:

.. code-block:: yaml

    queue:
      cls: aioworkers_mqtt.Queue
      host: localhost
      port: 1883
      user: user
      password: ***
      qos: 1
      format: json
      topics:
        - a
        - b

    storage:
      cls: aioworkers_mqtt.Storage
      host: localhost
      port: 1883
      user: user
      password: ***
      qos: 1
      retain: true
      format: json
      prefix: room/device

You can work with queue like this:

.. code-block:: python

    await context.queue.put({"a": 1})
    d = await context.queue.get()

and work with storage like this:

.. code-block:: python

    await context.storage.set("a", 1)
    one = await context.storage.get("a")


Run:

.. code-block:: bash

    aioworkers -c config.yaml -l debug


Development
-----------

Check code:

.. code-block:: shell

    hatch run lint:all


Format code:

.. code-block:: shell

    hatch run lint:fmt


Run tests:

.. code-block:: shell

    hatch run pytest


Run tests with coverage:

.. code-block:: shell

    hatch run cov
