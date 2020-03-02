from typing import Dict

from Classes.HiveTypeEnum import HiveTypeEnum
from Classes.Point import Point


class Hive:
    def __init__(self, id: int, data: Dict):
        self.id = id
        self.pos = Point(data["x"], data["y"])
        self.dir = data["dir"]
        self.type: HiveTypeEnum = self.parseType(data["type"])

    @staticmethod
    def parseType(type: str):
        if type == "HIVE_HEALTHY":
            return HiveTypeEnum.HIVE_HEALTHY
        return HiveTypeEnum.HIVE_DISEASED
