from typing import NamedTuple, Union


class ToyType(NamedTuple):
    display_name: str
    prefix: Union[str, None]
    filter_prefix: str
    cmd_safe_interval: float

# TODO fill all toys implementation
# NONE = ToyType(Toy, 'Robot', None, 'Sphero', .06)
# SPHERO = ToyType(Sphero, 'SPRK/2.0',  None, 'Sphero', .06)
# OLLIE = ToyType(Ollie, 'Ollie', '2B-', '2B', .06)
# BB8 = ToyType(BB8, 'BB-8', 'BB-', 'BB', .06)
# SPRK2 = ToyType(Sprk2, 'Sphero SPRK+', 'SK-', 'SK', .06)
# R2D2 = ToyType(R2D2, 'R2-D2', 'D2-', 'D2'), .12)
# R2Q5 = ToyType(R2Q5, 'R2-Q5', 'Q5-', 'Q5', .12)
# BB9E = ToyType(BB9E, 'BB-9E', 'GB-', 'GB', .12)
# MINI = ToyType(Mini, 'Sphero Mini', 'SM-', 'SM', .12)
# BOLT = ToyType(Bolt, 'Sphero BOLT', 'SB-', 'SB', .075)
# RVR = ToyType(RVR, 'Sphero RVR', 'RV-', 'RV', .075)
