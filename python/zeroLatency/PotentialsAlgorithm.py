import numpy as np
from enum import Enum

from Entities import GameData


class NodeType(Enum):
    EMPTY = 0
    HIVE = 1


class Potential:
    GAME_HEIGHT = 2000
    GAME_WIDTH = 3500
    NODE_SIZE = 125
    REPULSIVE_FACTOR = 0.7
    ATTRACTIVE_FACTOR = 0.3
    HIVE_RADIUS = 0

    def __init__(self, gameData: GameData):
        super().__init__()
        self.gameData = gameData
        self.mapShape = (self.GAME_HEIGHT // self.NODE_SIZE, self.GAME_WIDTH // self.NODE_SIZE)
        self.nodeMap = self.initNodeMap((1000, 500))

    def initNodeMap(self, end):
        nodeMap = np.zeros(shape=self.mapShape)
        end = self.toMapPoint(end)

        for i in range(self.mapShape[0]):
            for j in range(self.mapShape[1]):
                attractiveForce = self.euclidean((i, j), end)
                nodeMap[i][j] += self.ATTRACTIVE_FACTOR * attractiveForce

                for hive in self.gameData.healthyHives + self.gameData.diseasedHives:
                    hivePosition = self.toMapPoint((hive.pos.x, hive.pos.y))
                    repulsiveForce = 1 / self.euclidean((i, j), hivePosition)
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

    @staticmethod
    def euclidean(a: tuple, b: tuple):
        return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
