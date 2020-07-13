import math
from collections import deque

from Chassis import Chassis
from Constants import HIST_QUEUE_LENGTH, DIST_EPS, DIST_NEAR, DIR_EPS, SPEED_BASE_MAX, SPEED_MAX
from Entities import GameData, Point, State, HiveTypeEnum, Hive
from PidController import PidController


class Controller:
    def __init__(self, gameData: GameData, initialState: State = State.GET_HEALTHY_HIVE):
        self.__pos: Point = gameData.homeRobot.pos
        self.__dir: float = gameData.homeRobot.dir

        self.speedRight: int = 0
        self.speedLeft: int = 0

        self.speedRightOld: int = 0
        self.speedLeftOld: int = 0

        self.robotDirHist: deque = deque([180.0] * HIST_QUEUE_LENGTH)
        self.robotDistHist: deque = deque([math.inf] * HIST_QUEUE_LENGTH)

        self.__target: Point = Point(0, 0)
        self.state: State = initialState
        self.stateOld: State = initialState

        self.gameData: GameData = gameData

        self.targetDistance: int = 0
        self.targetAngle: float = 0

        self.stateChanged = False

        self.pidController: PidController = PidController()
        self.chassis: Chassis = Chassis()

    def update(self, gameData: GameData, target: Point):

        print(self.state)
        if self.state != self.stateOld:
            self.stateChanged = True
        else:
            self.stateChanged = False
        self.stateOld = self.state

        self.gameData = gameData

        self.__pos = gameData.homeRobot.pos
        self.__dir = gameData.homeRobot.dir

        if target is not None:
            self.targetDistance = self.distance(target)
            self.targetAngle = self.angle(target)

            self.robotDirHist.popleft()
            self.robotDirHist.append(self.targetDistance)
            self.robotDistHist.popleft()
            self.robotDistHist.append(self.targetAngle)

        # TODO remove this?
        # self.stateChanged = self.hasStateChanged()

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

    def setTarget(self, target: Point) -> None:
        print("Target coords: " + str(target.x) + " " + str(target.y))
        self.__target = target

    def atTargetEPS(self) -> bool:
        return self.targetDistance < DIST_EPS

    def atTargetNEAR(self) -> bool:
        return self.targetDistance < DIST_NEAR

    def atTargetHist(self) -> bool:
        err = [d > DIST_EPS for d in self.robotDistHist]
        return sum(err) == 0

    def isTurned(self) -> bool:
        err = [abs(a) > DIR_EPS for a in self.robotDirHist]
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
        return (self.gameData.homeRobot.pos is not None) and (self.gameData.homeRobot.dir is not None)

    def updatePIDTurn(self) -> None:
        u = self.pidController.PIDTurn.update(self.targetAngle)
        self.speedRight = -u
        self.speedLeft = u

    def resetPIDTurn(self) -> None:
        self.pidController.PIDTurn.reset()

    def updatePIDStraight(self) -> None:

        turn = self.pidController.PIDForwardTurn.update(self.targetAngle)
        base = self.pidController.PIDForwardTurn.update(self.targetDistance)

        base = min(max(base, -SPEED_BASE_MAX), SPEED_BASE_MAX)
        self.speedRight = -base - turn
        self.speedLeft = -base + turn

    def resetPIDStraight(self) -> None:
        self.pidController.PIDForwardBase.reset()
        self.pidController.PIDForwardTurn.reset()


# controller.setStates(State.GET_BAD_APPLE,State.GET_APPLE)
