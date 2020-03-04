import math
from collections import deque

from Classes import Constants
from Classes.GameData import GameData
from Classes.HiveTypeEnum import HiveTypeEnum
from Classes.Point import Point
from Classes.Robot import Robot
from nabiralec import State


class Controller:
    def __init__(self):
        self.__pos: Point
        self.__dir: float

        self.speedRight: int
        self.speedLeft: int

        self.speedRightOld: int
        self.speedLeftOld: int

        self.robotDirHist: deque = deque([180.0] * Constants.HIST_QUEUE_LENGTH)
        self.robotDistHist: deque = deque([math.inf] * Constants.HIST_QUEUE_LENGTH)

        self.state: State
        self.stateOld: State

        self.gameData: GameData

    def update(self, gameData: GameData, target: Point):

        self.gameData = gameData

        self.__pos = gameData.homeRobot.pos
        self.__dir = gameData.homeRobot.dir

        targetDistance = self.distance(target)
        targetAngle = self.angle(target)

        self.robotDirHist.popleft()
        self.robotDirHist.append(targetDistance)
        self.robotDistHist.popleft()
        self.robotDistHist.append(targetAngle)

    def distance(self, point: Point) -> int:
        return self.__pos.distance(point)

    def angle(self, point: Point) -> float:
        """
        Izračunaj kot, za katerega se mora zavrteti robot, da bo obrnjen proti točki p2.
        Robot se nahaja v točki p1 in ima smer (kot) a1.
        """
        a = math.degrees(math.atan2(point.y - self.__pos.y, point.x - self.__pos.x))
        a_rel = a - self.__dir
        if abs(a_rel) > 180:
            if a_rel > 0:
                a_rel = a_rel - 360
            else:
                a_rel = a_rel + 360

        return a_rel

    def getClosestHive(self, hiveType: HiveTypeEnum):
        if hiveType == HiveTypeEnum.HIVE_HEALTHY:
            return min(self.gameData.healthyHives, key=lambda hive: hive.pos.distance(self.__pos))
        elif hiveType == HiveTypeEnum.HIVE_DISEASED:
            return min(self.gameData.diseasedHives, key=lambda hive: hive.pos.distance(self.__pos))
