import numpy as np
from enum import Enum

from Game import Game
from algorithms.RobotAlgorithm import RobotAlgorithm
from algorithms.Utils import euclidean


class NodeType(Enum):
    EMPTY = 0
    HIVE = 1


class Potential(RobotAlgorithm):
    NODE_SIZE = 50
    REPULSIVE_FACTOR = 1.0
    ATTRACTIVE_FACTOR = 1.2

    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.mapShape = (game.GAME_HEIGHT // self.NODE_SIZE, game.GAME_WIDTH // self.NODE_SIZE)
        self.nodeMap = self.initNodeMap((1000, 2800))

    def getMotion(self, currentTrajectoryPoint):
        return self.next(currentTrajectoryPoint)

    def initNodeMap(self, end):
        nodeMap = np.zeros(shape=self.mapShape)
        end = self.toMapPoint(end)

        for i in range(self.mapShape[0]):
            for j in range(self.mapShape[1]):
                attractiveForce = euclidean((i, j), end)
                nodeMap[i][j] += self.ATTRACTIVE_FACTOR * attractiveForce

                for hive in self.game.hives:
                    hivePosition = self.toMapPoint(hive.position)
                    repulsiveForce = 1 / euclidean((j, i), hivePosition)
                    nodeMap[i][j] += self.REPULSIVE_FACTOR * repulsiveForce

        return nodeMap

    def next(self, pos) -> tuple:
        pos = self.toMapPoint(pos)
        startX, startY, endX, endY = self.findBorders(pos, 1)

        minCost = float('inf')
        best = -1, -1

        for j in range(startY, endY + 1):
            for i in range(startX, endX + 1):
                if self.nodeMap[j][i] < minCost:
                    minCost = self.nodeMap[j][i]
                    best = i, j

        return self.toGamePoint(best)

    def findBorders(self, point: tuple, radius: int):
        startX = point[0]
        startY = point[1]
        endX = point[0]
        endY = point[1]

        for _ in range(radius):
            if startX - 1 >= 0:
                startX -= 1
            if startY - 1 >= 0:
                startY -= 1
            if endX + 1 < self.mapShape[1]:
                endX += 1
            if endY + 1 < self.mapShape[0]:
                endY += 1

        return startX, startY, endX, endY

    def toMapPoint(self, point):
        return round(point[0] / self.NODE_SIZE), round(point[1] / self.NODE_SIZE)

    def toGamePoint(self, point):
        return int(point[0]) * self.NODE_SIZE, int(point[1]) * self.NODE_SIZE
