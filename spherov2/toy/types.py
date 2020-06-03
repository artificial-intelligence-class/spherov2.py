from enum import Enum


class ServicesUUID(Enum):
    api_v2_control = '00010001-574f-4f20-5370-6865726f2121'
    nordic_dfu = '00020001-574f-4f20-5370-6865726f2121'


class CharacteristicUUID(Enum):
    api_v2 = '00010002-574f-4f20-5370-6865726f2121'
    dfu_control = '00020002-574f-4f20-5370-6865726f2121'
    subs = '00020003-574f-4f20-5370-6865726f2121'
    dfu_info = '00020004-574f-4f20-5370-6865726f2121'
    anti_dos = '00020005-574f-4f20-5370-6865726f2121'
