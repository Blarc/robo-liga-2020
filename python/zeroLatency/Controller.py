import math
from collections import deque
from typing import List

from Chassis import Chassis
from Constants import HIST_QUEUE_LENGTH, DIST_EPS, DIST_NEAR, DIR_EPS, SPEED_BASE_MAX, SPEED_MAX
from Entities import GameData, Point, State, HiveTypeEnum, Hive
from PidController import PidController


class Controller:
    def __init__(self, initialState: State = State.GET_HEALTHY_HIVE):
        self.__pos = None
        self.__dir = None

        self.speedRight = 0
        self.speedLeft = 0

        self.speedRightOld = 0
        self.speedLeftOld = 0

        self.target = Point(0, 0)
        self.targets = []

        self.robotDirTargetHist = deque([180.0] * HIST_QUEUE_LENGTH)
        self.robotDistTargetHist = deque([math.inf] * HIST_QUEUE_LENGTH)

        self.targetDistance = 9999
        self.targetAngle = 9999

        self.state = initialState
        self.stateOld = initialState

        self.gameData = None

        self.stateChanged = False

        self.pidController = PidController()
        self.chassis = Chassis()

    def update(self, gameData: GameData, targets: List[Point]):

        if self.state != self.stateOld:
            self.stateChanged = True
        else:
            self.stateChanged = False
        self.stateOld = self.state

        self.gameData = gameData
        self.target = targets[0]
        self.targets = targets

        if gameData.homeRobot is not None:
            self.__pos = gameData.homeRobot.pos
            self.__dir = gameData.homeRobot.dir

            if self.target is not None:
                self.targetDistance = self.distance(self.target)
                self.targetAngle = self.angle(self.target)

                self.robotDirTargetHist.popleft()
                self.robotDirTargetHist.append(self.targetAngle)
                self.robotDistTargetHist.popleft()
                self.robotDistTargetHist.append(self.targetDistance)

    def distance(self, point: Point) -> float:
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

    def getClosestHive(self, hiveType: HiveTypeEnum) -> Hive:
        if hiveType == HiveTypeEnum.HIVE_HEALTHY:
            return min(self.gameData.healthyHives, key=lambda hive: hive.pos.distance(self.__pos))
        elif hiveType == HiveTypeEnum.HIVE_DISEASED:
            return min(self.gameData.diseasedHives, key=lambda hive: hive.pos.distance(self.__pos))

    def atTargetEPS(self) -> bool:
        return self.targetDistance < DIST_EPS

    def atTargetNEAR(self) -> bool:
        return self.targetDistance < DIST_NEAR

    def atTargetHIST(self) -> bool:
        err = [d > DIST_EPS for d in self.robotDistTargetHist]
        return sum(err) == 0

    def isTurned(self) -> bool:
        err = [abs(a) > DIR_EPS for a in self.robotDirTargetHist]

        if sum(err) == 0:
            self.speedRight = 0
            self.speedLeft = 0
            return True

        return False

    def hasStateChanged(self) -> bool:
        return self.state != self.stateOld

    def setStates(self, new: State, old: State) -> None:
        self.state = new
        self.stateOld = old

    def setSpeedToZero(self) -> None:
        self.chassis.runMotors(0, 0)

    def runMotors(self) -> None:
        self.speedRight = round(min(max(self.speedRight, -SPEED_MAX), SPEED_MAX))
        self.speedLeft = round(min(max(self.speedLeft, -SPEED_MAX), SPEED_MAX))

        self.chassis.runMotors(self.speedRight, self.speedLeft)

        self.speedRightOld = self.speedRight
        self.speedLeftOld = self.speedLeft

    def breakMotors(self) -> None:
        self.chassis.breakMotors()

    def robotDie(self) -> None:
        self.chassis.robotDie()

    def isRobotAlive(self) -> bool:
        return (self.__pos is not None) and (self.__dir is not None)

    def updatePIDTurn(self) -> None:
        u = self.pidController.PIDTurn.update(self.targetAngle)
        self.speedRight = -u
        self.speedLeft = u

    def resetPIDTurn(self) -> None:
        self.pidController.PIDTurn.reset()

    def updatePIDStraight(self) -> None:

        secondAngle = sum([abs(self.angle(target)) for target in self.targets[1:]])

        if secondAngle < 15:
            base = -200
        elif secondAngle < 40:
            base = -150
        elif secondAngle < 90:
            base = -100
        else:
            base = -50

        # base = self.pidController.PIDForwardBase.update(1 / abs(self.targetAngle))
        turn = self.pidController.PIDForwardTurn.update(self.targetAngle)


        base = min(max(base, -SPEED_BASE_MAX), SPEED_BASE_MAX)
        # base += self.targetAngle * 1.0

        print("base: ", base, "turn: ", turn, "targetDistance: ", self.targetDistance, "targetAngle: ", self.targetAngle, "secondAngle: ", secondAngle)

        self.speedRight = -base - turn
        self.speedLeft = -base + turn

    def resetPIDStraight(self) -> None:
        self.pidController.PIDForwardBase.reset()
        self.pidController.PIDForwardTurn.reset()

    def getAngleApprox(self):
        x = 0
        y = 0

        if 22.5 <= self.__dir < 67.5:
            x -= 1
            y -= 1
        elif 67.5 <= self.__dir < 112.5:
            x -= 1
        elif 112.5 <= self.__dir < 157.5:
            x += 1
            y -= 1
        elif 157.5 <= self.__dir or self.__dir < -157.5:
            x += 1
        elif -157.5 <= self.__dir < -112.5:
            x += 1
            y += 1
        elif -112.5 <= self.__dir < -67.5:
            y += 1
        elif -67.5 <= self.__dir < -22.5:
            x -= 1
            y += 1
        elif -22.5 <= self.__dir or self.__dir < 22.5:
            y -= 1

        return x, y