=======
Adapter
=======

This library abstracts the Bluetooth communication layer as a single adapter class, to potentially support all platforms and all environments.

BleakAdapter
============
.. class:: spherov2.adapter.bleak_adapter.BleakAdapter

This adapter uses `hbldh/bleak <https://github.com/hbldh/bleak>`_ library directly on the host machine. Make sure there is a low energy Bluetooth adapter (Bluetooth 4.0 or above) on your computer. Then, install the Bluetooth library by ``pip install bleak``.

``BleakAdapter`` is used by default by the scanner::

    from spherov2 import scanner

    with scanner.find_toy() as toy:
        ...

TCPAdapter
==========
.. class:: spherov2.adapter.tcp_adapter.TCPAdapter

This adapter allows the user to send and receive Bluetooth packets connected to another host via a server running on that host as a relay.

To start the server, run ``python -m spherov2.adapter.tcp_server [host] [port]``, with ``host`` and ``port`` are optional and by default being ``0.0.0.0`` and ``50004``.

.. autofunction:: spherov2.adapter.tcp_adapter.get_tcp_adapter

    To use the adapter, for example::

        from spherov2 import scanner
        from spherov2.adapter.tcp_adapter import get_tcp_adapter

        with scanner.find_toy(adapter=get_tcp_adapter('localhost')) as toy:
            ...
