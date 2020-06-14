# spherov2.py

***This library is still in early development&hellip;***

An unofficial library written in Python for [Sphero](https://sphero.com/) toys that supports its Version 2 Bluetooth low energy API described [here](https://sdk.sphero.com/docs/api_spec/general_api/). Toys that are supported includes (implemented ones are checked):

- [ ] Sphero 1.0
- [ ] Sphero 2.0 / SPRK
- [ ] Sphero Ollie
- [ ] Sphero BB-8
- [ ] Sphero BB-9E
- [x] Sphero R2-D2 / R2-Q5
- [ ] Sphero BOLT
- [ ] Sphero SPRK+ / SPRK 2.0
- [ ] Sphero Mini
- [ ] Sphero RVR

The logic is written based on reverse-engineering the official [Sphero Edu for Android](https://play.google.com/store/apps/details?id=com.sphero.sprk), with the help from available documentations and existing libraries such as [igbopie/spherov2.js](https://github.com/igbopie/spherov2.js) and [EnotYoyo/pysphero](https://github.com/EnotYoyo/pysphero).

This project uses the [hbldh/bleak](https://github.com/hbldh/bleak) Bluetooth Low Energy library, which supports all platforms, with some restrictions explained below.

## Usage

To install the library, run `pip install spherov2`. Python version `>= 3.7` are supported.

The library currently has two adapters, `BleakAdapter` and `TCPAdapter`. `BleakAdapter` is used by default when adapter is not specified, which connects to toys using the local Bluetooth adapter. Due to issue mentioned in [hbldh/bleak#206](https://github.com/hbldh/bleak/issues/206), `BleakAdapter` does not yet work on MacOS as the library uses multiple threads to handle events. For example:

```python
from spherov2 import scanner

with scanner.find_toy() as toy:
    ...
```

`TCPAdapter` allows the user to send and receive Bluetooth packets connected to another host via a server running on that host as a relay. To start the server, run `python -m spherov2.adapter.tcp_server [host] [port]`, with `host` and `port` by default being `0.0.0.0` and `50004`. To use the adapter, for example:

```python
from spherov2 import scanner
from spherov2.adapter.tcp_adapter import get_tcp_adapter

with scanner.find_toy(adapter=get_tcp_adapter('localhost')) as toy:
    ...
```

The TCP server is written in asynchronous fashion using `asyncio`, so that it supports `bleak` on all platforms. Therefore, a temporary solution for the library to run solely on MacOS could be to start a TCP server on `localhost` and connects to the server using a `TCPAdapter`. 

On whichever device you decide to connect to the toys, you have to first install the BLE library by `pip install bleak`.

### Scanner

TODO

### APIs

There are two ways you can interact with the toys, one is to use the low-level APIs implemented for each toy with the commands they support. Low-level APIs can be found for each toy under `spherov2.toy.*`, and is not documented.

The other and recommended way is to use the high level API `spherov2.sphero_edu.SpheroEduAPI`, which is an implementation of the official [Sphero Edu APIs](https://sphero.docsapp.io/docs/get-started). Documentations can be found inside the source files with the docstrings, or [here](#TODO) as an HTML rendered version. For example:

```python
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI

toy = scanner.find_R2Q5()
with SpheroEduAPI(toy) as api:
    api.spin(360, 1)
```

## Acknowledgments

This library is made for educational purposes, to assist the use of Sphero robots by students in [CIS 521 - Artificial Intelligence](http://artificial-intelligence-class.org/) at the University of Pennsylvania.

It is published as an open-source library under the [MIT License](LICENSE).

## Authors

* **Hanbang Wang** - [https://www.cis.upenn.edu/~hanbangw/](https://www.cis.upenn.edu/~hanbangw/)