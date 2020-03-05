import math
from collections import deque

from .Constants import *
from .GameData import GameData
from .HiveTypeEnum import HiveTypeEnum
from .Point import Point
from .Robot import Robot
from .State import State


class Controller:
    def __init__(self, gameData: GameData):
        self.__pos: Point = gameData.homeRobot.pos
        self.__dir: float = gameData.homeRobot.dir

        self.speedRight: int = 0
        self.speedLeft: int = 0

        self.speedRightOld: int = 0
        self.speedLeftOld: int = 0

        self.robotDirHist: deque = deque([180.0] * HIST_QUEUE_LENGTH)
        self.robotDistHist: deque = deque([math.inf] * HIST_QUEUE_LENGTH)

        self.__target: Point = Point(0, 0)
        self.state: State = State.GET_APPLE
        self.stateOld: State = State.GET_APPLE

        self.gameData: GameData = gameData

        self.targetDistance: int = 0
        self.targetAngle: float = 0

        self.stateChanged = False


    def update(self, gameData: GameData, target: Point):

        self.gameData = gameData

        self.__pos = gameData.homeRobot.pos
        self.__dir = gameData.homeRobot.dir

        self.targetDistance = self.distance(target)
        self.targetAngle = self.angle(target)

        self.robotDirHist.popleft()
        self.robotDirHist.append(self.targetDistance)
        self.robotDistHist.popleft()
        self.robotDistHist.append(self.targetAngle)

        self.stateChanged = self.setStateChanged()


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

    def setTarget(self, target: Point):
        self.__target = target

    def atTarget(self):
        return self.targetDistance < DIST_EPS

    def setStateChanged(self):
        return self.state != self.stateOld

    def setStates(self, new: State , old : State):
        self.state = new
        self.stateOld = old

#controller.setStates(State.GET_BAD_APPLE,State.GET_APPLE)
