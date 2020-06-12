from functools import partial

from bleak import discover, BleakClient

from spherov2.toy.consts import ServicesUUID


class BleakAdapter(BleakClient):
    scan_toys = partial(discover, filters={'UUIDs': [e.value for e in ServicesUUID]})

    async def write(self, uuid, data):
        await self.write_gatt_char(uuid, bytearray(data), True)
