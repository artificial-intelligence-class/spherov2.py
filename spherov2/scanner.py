from spherov2.adapter.bleak import BleakAdaptor
from spherov2.toy.r2q5 import R2Q5


def find_toys(timeout=5.0, toy_types=None):
    toys = BleakAdaptor.scan_toys(timeout)
    if toy_types is not None:
        toys = filter(lambda t: t, toys)
    return [R2Q5(t.address) for t in toys]
