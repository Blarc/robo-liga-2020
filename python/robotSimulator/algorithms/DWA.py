import math
from enum import Enum
from typing import List

import numpy as np

from Game import Game
from algorithms.RobotAlgorithm import RobotAlgorithm


class RobotType(Enum):
    circle = 0
    rectangle = 1


class RobotConfig:
    """
    everything is in millimeters
    robot has a transmission 36:12 == 3:1
    160-170 rpm -> 2,75 rps
    wheel diameter is 56 mm
    with transmission we get max speed = 426 mm / s
    """

    def __init__(self, robotType: RobotType):
        self.maxSpeed = 150.0  # 426.0  # [mm/s]
        self.minSpeed = -50.0  # -426.0  # [m/s]
        # TODO calculate max yaw rate
        self.maxYawRate = 60.0 * math.pi / 180.0  # [rad/s]
        # TODO calculate max acceleration
        self.maxAccel = 50.0  # 100.0  # [mm/ss]
        # TODO calculate max delta yaw rate
        self.maxDeltaYawRate = 60.0 * math.pi / 180.0  # [rad/ss]

        self.vResolution = 4.9  # 5.0  # [mm/s]
        self.yawRateResolution = 0.5 * math.pi / 180.0  # [rad/s]

        self.dt = 0.25  # 0.2  # [s] Time tick for motion prediction
        self.predictTime = 4.0  # 2.0  # [s]

        self.angleCostGain = 0.15  # alpha
        self.speedCostGain = 1.0  # beta
        self.obstacleCostGain = 1.0  # gama

        self.robotType = robotType

        # if robot_type == RobotType.circle
        # Also used to check if goal is reached in both types
        self.robotRadius = 125.0  # 300.0  # [mm] for collision check

        # if robot_type == RobotType.rectangle
        # TODO measure robot width and length
        self.robotWidth = 250  # [mm] for collision check
        self.robotLength = 300  # [mm] for collision check

    # @property
    # def robot_type(self):
    #     return self._robot_type
    #
    # @robot_type.setter
    # def robot_type(self, value):
    #     if not isinstance(value, RobotType):
    #         raise TypeError("robot_type must be an instance of RobotType")
    #     self._robot_type = value


class DWA(RobotAlgorithm):

    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.robotConfig = RobotConfig(RobotType.rectangle)

    def getControlPoints(self) -> np.array:
        return []

    def getMotion(self, currentTrajectoryPoint: np.array) -> np.array:

        # start
        # currentTrajectoryPoint: np.array = np.array([0.0, 0.0, math.pi / 8.0, 0.0, 0.0])

        # goal
        goal = np.array([2800.0, 1000.0])

        # obstacles
        obstacles = np.array([(hive.position[0], hive.position[1]) for hive in self.game.hives])

        v, y, predictedTrajectory = self.dwaControl(currentTrajectoryPoint, goal, obstacles)

        # simulate robot
        nextTrajectoryPoint = self.motion(currentTrajectoryPoint, v, y)

        # check reaching goal
        distToGoal = math.hypot(currentTrajectoryPoint[0] - goal[0], currentTrajectoryPoint[1] - goal[1])
        if distToGoal <= self.robotConfig.robotRadius:
            print("Goal!")
            return np.array([-1, -1, -1, -1, -1])
        # store history
        # trajectory = np.vstack((trajectory, currentTrajectoryPoint))

        return nextTrajectoryPoint

    def dwaControl(self, trajectoryPoint: np.array, goal, obstacles: np.array) -> (
            float, float, np.vstack):

        # get the dynamic window for current position
        dynamicWindow = self.calcDynamicWindow(trajectoryPoint)

        # returns v, y, trajectory
        return self.calcControlAndTrajectory(trajectoryPoint, dynamicWindow, goal, obstacles)

    def motion(self, trajectoryPoint: np.array, speed, omega) -> np.array:
        """

        :param trajectoryPoint: reference trajectory point
        :param speed: robot's speed
        :param omega: robot's rotational speed
        """

        trajectoryPoint[2] += omega * self.robotConfig.dt
        trajectoryPoint[0] += speed * math.cos(trajectoryPoint[2]) * self.robotConfig.dt
        trajectoryPoint[1] += speed * math.sin(trajectoryPoint[2]) * self.robotConfig.dt
        trajectoryPoint[3] = speed
        trajectoryPoint[4] = omega

        return trajectoryPoint

    def calcDynamicWindow(self, trajectoryPoint: np.array) -> List:
        """
        calculate dynamic window based on current state
        """

        # Dynamic window from robot specification
        # [speed_min, speed_max, yaw_rate_min, yaw_rate_max]
        windowSpecification = [self.robotConfig.minSpeed, self.robotConfig.maxSpeed,
                               -self.robotConfig.maxYawRate, self.robotConfig.maxYawRate]

        # Dynamic window from motion model
        # [speed_min, speed_max, yaw_rate_min, yaw_rate_max]
        windowModel = [
            trajectoryPoint[3] - self.robotConfig.maxAccel * self.robotConfig.dt,
            trajectoryPoint[3] + self.robotConfig.maxAccel * self.robotConfig.dt,
            trajectoryPoint[4] - self.robotConfig.maxDeltaYawRate * self.robotConfig.dt,
            trajectoryPoint[4] + self.robotConfig.maxDeltaYawRate * self.robotConfig.dt
        ]

        # return the best of both
        return [
            max(windowSpecification[0], windowModel[0]), min(windowSpecification[1], windowModel[1]),
            max(windowSpecification[2], windowModel[2]), min(windowSpecification[3], windowModel[3])
        ]

    def predictTrajectory(self, initTrajectoryPoint: np.array, v, y) -> np.vstack:

        temp = np.array(initTrajectoryPoint)
        trajectory = np.array(initTrajectoryPoint)
        time = 0

        while time <= self.robotConfig.predictTime:
            temp = self.motion(temp, v, y)
            trajectory = np.vstack((trajectory, temp))
            time += self.robotConfig.dt

        return trajectory

    def calcControlAndTrajectory(self, trajectoryPoint: np.array, dynamicWindow: List, goal: List,
                                 obstacles: np.array) -> (float, float, np.vstack):

        initTrajectoryPoint = trajectoryPoint[:]
        minCost = float("inf")
        bestV = 0.0
        bestY = 0.0
        bestTrajectory = np.array([trajectoryPoint])

        # evaluate all trajectory with sampled input in dynamic window
        for v in np.arange(dynamicWindow[0], dynamicWindow[1], self.robotConfig.vResolution):
            for y in np.arange(dynamicWindow[2], dynamicWindow[3], self.robotConfig.yawRateResolution):

                # Get predicted trajectory with v and y speeds
                trajectory: np.vstack = self.predictTrajectory(initTrajectoryPoint, v, y)

                # Target heading - how good is the trajectory based on angle difference to goal
                angleCost = self.robotConfig.angleCostGain * self.calcAngleCost(trajectory, goal)

                # Velocity - how good is the trajectory based on the speed
                speedCost = self.robotConfig.speedCostGain * (self.robotConfig.maxSpeed - trajectory[-1, 3])

                # Clearance - how good is the trajectory based on the distance to obstacles
                obstacleCost = self.robotConfig.obstacleCostGain * self.calcObstacleCost(trajectory, obstacles)

                finalCost = angleCost + speedCost + obstacleCost

                # search minimum trajectory
                if minCost >= finalCost:
                    minCost = finalCost
                    bestV = v
                    bestY = y
                    bestTrajectory = trajectory

        return bestV, bestY, bestTrajectory

    def calcObstacleCost(self, trajectory: np.vstack, obstacles: np.array):
        """
            calc obstacle cost inf: collision
        """

        # all obstacles' xs
        obstacleX = obstacles[:, 0]

        # all obstacles' ys
        obstacleY = obstacles[:, 1]

        dx = trajectory[:, 0] - obstacleX[:, None]
        dy = trajectory[:, 1] - obstacleY[:, None]

        # calculate distances to all obstacles for each trajectory point
        r = np.hypot(dx, dy)

        if self.robotConfig.robotType == RobotType.rectangle:

            yaw = trajectory[:, 2]

            # TODO check what this does
            rot = np.array([[np.cos(yaw), -np.sin(yaw)], [np.sin(yaw), np.cos(yaw)]])
            rot = np.transpose(rot, [2, 0, 1])

            # TODO check what this does
            localObstacle = obstacles[:, None] - trajectory[:, 0:2]
            localObstacle = localObstacle.reshape(-1, localObstacle.shape[-1])
            localObstacle = np.array([localObstacle @ x for x in rot])
            localObstacle = localObstacle.reshape(-1, localObstacle.shape[-1])

            # Check if obstacle is too close
            upperCheck = localObstacle[:, 0] <= self.robotConfig.robotLength / 2
            rightCheck = localObstacle[:, 1] <= self.robotConfig.robotWidth / 2
            bottomCheck = localObstacle[:, 0] >= -self.robotConfig.robotLength / 2
            leftCheck = localObstacle[:, 1] >= -self.robotConfig.robotWidth / 2

            # If obstacle is too close return Inf
            if (np.logical_and(np.logical_and(upperCheck, rightCheck), np.logical_and(bottomCheck, leftCheck))).any():
                return float("Inf")

        # Just check if any of the obstacles is in the radius
        elif self.robotConfig.robotType == RobotType.circle:
            if np.array(r <= self.robotConfig.robotRadius).any():
                return float("Inf")

        # If obstacles are not in the way, take the trajectory that's farthest from obstacles
        minR = np.min(r)
        return 1.0 / minR

    @staticmethod
    def calcAngleCost(trajectory: np.vstack, goal):

        # trajectory is stack of TrajectoryPoints
        # get the top trajectory point and calc delta
        dx = goal[0] - trajectory[-1, 0]
        dy = goal[1] - trajectory[-1, 1]

        errorAngle = math.atan2(dy, dx)
        costAngle = errorAngle - trajectory[-1, 2]
        # the best if the robot moves directly towards the target
        cost = abs(math.atan2(math.sin(costAngle), math.cos(costAngle)))

        return cost
