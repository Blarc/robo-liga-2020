from typing import Dict

from .Point import Point


class Field:
    def __init__(self, data: Dict):
        self.topLeft = Point(data["topLeft"]["x"], data["topLeft"]["y"])
        self.topRight = Point(data["topRight"]["x"], data["topRight"]["y"])
        self.bottomLeft = Point(data["bottomLeft"]["x"], data["bottomLeft"]["y"])
        self.bottomRight = Point(data["bottomRight"]["x"], data["bottomRight"]["y"])

