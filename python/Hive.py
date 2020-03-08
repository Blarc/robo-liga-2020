from typing import Dict

from HiveTypeEnum import HiveTypeEnum
from Point import Point


class Hive:
    def __init__(self, id: int, data: Dict):
        self.id: int = id
        self.pos: Point = Point(data["x"], data["y"])
        self.dir: float = data["dir"]
        self.type: HiveTypeEnum = self.parseType(data["type"])

    @staticmethod
    def parseType(type: str):
        if type == "HIVE_HEALTHY":
            return HiveTypeEnum.HIVE_HEALTHY
        return HiveTypeEnum.HIVE_DISEASED
