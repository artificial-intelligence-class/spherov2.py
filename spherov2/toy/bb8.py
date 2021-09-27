from enum import IntEnum
from enum import IntEnum
from functools import lru_cache

from spherov2.commands.core import Core
from spherov2.commands.sphero import Sphero
from spherov2.controls.v1 import FirmwareUpdateControl
from spherov2.toy.sphero import Sphero as SPHERO
from spherov2.types import ToyType


class BB8(SPHERO):
    toy_type = ToyType('BB-8', 'BB-', 'BB', .06)

    # _send_uuid = '22bb746f-2ba1-7554-2d6f-726568705327'
    # _response_uuid = '22bb746f-2ba6-7554-2d6f-726568705327'
    # _handshake = [('22bb746f-2bbd-7554-2d6f-726568705327', bytearray(b'011i3')),
    #              ('22bb746f-2bb2-7554-2d6f-726568705327', bytearray([7]))]

    class LEDs(IntEnum):
        BODY_RED = 0
        BODY_GREEN = 1
        BODY_BLUE = 2
        AIMING = 3
        HEAD = 4

    class Animations(IntEnum):
        EMOTE_ALARM = 0
        EMOTE_NO = 1
        EMOTE_SCAN_SWEEP = 2
        EMOTE_SCARED = 3
        EMOTE_YES = 4
        EMOTE_AFFIRMATIVE = 5
        EMOTE_AGITATED = 6
        EMOTE_ANGRY = 7
        EMOTE_CONTENT = 8
        EMOTE_EXCITED = 9
        EMOTE_FIERY = 10
        EMOTE_GREETINGS = 11
        EMOTE_NERVOUS = 12
        EMOTE_SLEEP = 14
        EMOTE_SURPRISED = 15
        EMOTE_UNDERSTOOD = 16
        HIT = 17
        WWM_ANGRY = 18
        WWM_ANXIOUS = 19
        WWM_BOW = 20
        WWM_CURIOUS = 22
        WWM_DOUBLE_TAKE = 23
        WWM_EXCITED = 24
        WWM_FIERY = 25
        WWM_HAPPY = 26
        WWM_JITTERY = 27
        WWM_LAUGH = 28
        WWM_LONG_SHAKE = 29
        WWM_NO = 30
        WWM_OMINOUS = 31
        WWM_RELIEVED = 32
        WWM_SAD = 33
        WWM_SCARED = 34
        WWM_SHAKE = 35
        WWM_SURPRISED = 36
        WWM_TAUNTING = 37
        WWM_WHISPER = 38
        WWM_YELLING = 39
        WWM_YOOHOO = 40
        WWM_FRUSTRATED = 41
        IDLE_1 = 42
        IDLE_2 = 43
        IDLE_3 = 44
        EYE_1 = 45
        EYE_2 = 46
        EYE_3 = 47
        EYE_4 = 48

    # Async - Sphero
    # Bootloader - Sphero
    # Core
    get_factory_config_block_crc = Core.get_factory_config_block_crc  # GetFactorConfigBlockCrcCommand

    # Sphero
    get_sku = Sphero.get_sku  # GetSkuCommand

    # Controls - Sphero
    @property
    @lru_cache(None)
    def firmware_update_control(self):
        return FirmwareUpdateControl(self)
