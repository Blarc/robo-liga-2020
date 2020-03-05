from typing import Dict, List

from .Field import Field
from .Hive import Hive
from .HiveTypeEnum import HiveTypeEnum
from .Point import Point
from .Robot import Robot
from .Team import Team


class GameData:
    def __init__(self, data: Dict, teamTag: str, enemyTag: str):
        self.healthyHives: List[Hive] = []
        self.diseasedHives: List[Hive] = []
        self.parseHives(data["objects"]["hives"])
        self.homeBasket: Field = Field(data["fields"]["baskets"][teamTag])
        self.enemyBasket: Field = Field(data["fields"]["baskets"][enemyTag])
        self.homeZone: Field = Field(data["fields"]["zones"][teamTag])
        self.neutralZone: Field = Field(data["fields"]["zones"]["neutral"])
        self.enemyZone: Field = Field(data["fields"]["zones"][enemyTag])
        self.field: Field = Field(data["fields"]["field"])
        self.homeTeam: Team = Team(data["teams"][teamTag])
        self.enemyTeam: Team = Team(data["teams"][enemyTag])
        self.timeLeft: float = data["timeLeft"]
        self.gameOn: bool = data["gameOn"]
        self.homeRobot = Robot(int(self.homeTeam.id), data["objects"]["robots"][str(self.homeTeam.id)])
        self.enemyRobot = Robot(int(self.enemyTeam.id), data["objects"]["robots"][str(self.enemyTeam.id)])

    def parseHives(self, data):
        for id, hiveData in data.items():
            tmp = Hive(int(id), hiveData)
            if tmp.type == HiveTypeEnum.HIVE_HEALTHY:
                self.healthyHives.append(tmp)
            else:
                self.diseasedHives.append(tmp)