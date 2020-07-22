from typing import Dict, List

from enum import Enum
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def distance(self, point: 'Point') -> float:
        return math.sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2)


class Field:
    def __init__(self, data: Dict):
        self.topLeft = Point(data["topLeft"]["x"], data["topLeft"]["y"])
        self.topRight = Point(data["topRight"]["x"], data["topRight"]["y"])
        self.bottomLeft = Point(data["bottomLeft"]["x"], data["bottomLeft"]["y"])
        self.bottomRight = Point(data["bottomRight"]["x"], data["bottomRight"]["y"])

    def getCenter(self):
        return Point(
            self.topRight.x - self.topLeft.x,
            self.topLeft.y - self.bottomLeft.y
        )


class State(Enum):

    def __str__(self):
        return str(self.name)

    GET_HEALTHY_HIVE = 0
    GET_TURN = 1
    GET_STRAIGHT = 2
    HOME = 3
    HOME_TURN = 4
    HOME_STRAIGHT = 5
    BACK_OFF = 6
    ENEMY_HOME = 7
    ENEMY_HOME_TURN = 8
    ENEMY_HOME_STRAIGHT = 9
    GET_DISEASED_HIVE = 10
    IDLE = 90
    LOAD_NEXT_TARGET = 91
    TURN = 92
    DRIVE_STRAIGHT = 93
    ALGORITHM = 94
    DUMMY = 123


class HiveTypeEnum(Enum):
    HIVE_HEALTHY = 1,
    HIVE_DISEASED = 0


class Hive:
    def __init__(self, hiveId: int, data: Dict):
        self.id = hiveId
        self.pos = Point(data["x"], data["y"])
        self.dir = data["dir"]
        self.type = self.parseType(data["type"])

    @staticmethod
    def parseType(hiveType: str):
        if hiveType == "HIVE_HEALTHY":
            return HiveTypeEnum.HIVE_HEALTHY
        return HiveTypeEnum.HIVE_DISEASED


class Robot:
    def __init__(self, robotId: int, data: Dict):
        self.id = robotId
        self.pos = Point(data["position"]["x"], data["position"]["y"])
        self.dir = data["dir"]


class Team:
    def __init__(self, data: Dict):
        self.id = int(data["id"])
        self.name = data["name"]
        self.score = data["score"]


class GameData:
    def __init__(self, data: Dict, teamTag: str, enemyTag: str):
        self.healthyHives = []
        self.diseasedHives = []
        self.parseHives(data["objects"]["hives"])
        self.homeBasket = Field(data["fields"]["baskets"][teamTag])
        self.enemyBasket = Field(data["fields"]["baskets"][enemyTag])
        self.homeZone = Field(data["fields"]["zones"][teamTag])
        self.neutralZone = Field(data["fields"]["zones"]["neutral"])
        self.enemyZone = Field(data["fields"]["zones"][enemyTag])
        self.field = Field(data["fields"]["field"])
        self.homeTeam = Team(data["teams"][teamTag])
        self.enemyTeam = Team(data["teams"][enemyTag])
        self.timeLeft = data["timeLeft"]
        self.gameOn = data["gameOn"]

        try:
            self.homeRobot = Robot(int(self.homeTeam.id), data["objects"]["robots"][str(self.homeTeam.id)])
        except KeyError:
            self.homeRobot = None

        try:
            self.enemyRobot = Robot(int(self.enemyTeam.id), data["objects"]["robots"][str(self.enemyTeam.id)])
        except KeyError:
            self.enemyRobot = None

    def parseHives(self, data):
        for hiveId, hiveData in data.items():
            tmp = Hive(int(hiveId), hiveData)
            if tmp.type == HiveTypeEnum.HIVE_HEALTHY:
                self.healthyHives.append(tmp)
            else:
                self.diseasedHives.append(tmp)
