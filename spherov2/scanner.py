from typing import List, Type
from spherov2.adapter.bleak import BleakAdaptor
from spherov2.toy.core import Toy
from spherov2.toy.r2q5 import R2Q5


def find_toys(timeout=5.0, toy_types: List[Type[Toy]] = None):
    toys = BleakAdaptor.scan_toys(timeout)
    if toy_types is None:
        toy_types = [R2Q5]
    ret = []
    for toy in toys:
        for toy_cls in toy_types:
            toy_type = toy_cls.toy_type
            if toy.name.startswith(toy_type.filter_prefix) and \
                    (toy_type.prefix is None or toy.name.startswith(toy_type.prefix)):
                ret.append(toy_cls(toy.address))
                break
    return ret
