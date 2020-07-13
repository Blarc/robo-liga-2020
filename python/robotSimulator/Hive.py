from enum import Enum


class HiveType(Enum):
    HEALTHY = 1
    DISEASED = 2


class Hive:

    def __init__(self, position: tuple, hiveType: HiveType):
        super().__init__()
        self.position = position
        self.type = hiveType
