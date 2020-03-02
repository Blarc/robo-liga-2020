from typing import Dict

from Classes.Point import Point


class Robot:
    def __init__(self, id: int, data: Dict):
        self.id = id
        self.pos = Point(data["x"], data["y"])
        self.dir = data["dir"]
