import numpy as np
from enum import Enum

from Entities import GameData


class NodeType(Enum):
    EMPTY = 0
    HIVE = 1
    VISITED = 2


class GreedyAlgorithm:
    GAME_HEIGHT = 2000
    GAME_WIDTH = 3500

    NODE_SIZE = 100
    HIVE_RADIUS = 2

    LOOK_AHEAD = 3

    def __init__(self, gameData: GameData):
        super().__init__()
        self.mapShape = (self.GAME_HEIGHT // self.NODE_SIZE, self.GAME_WIDTH // self.NODE_SIZE)
        self.nodeMap = self.initNodeMap(gameData)

    def run(self, position: tuple, endPosition: tuple, gameData: GameData):

        pos = self.toMapPoint(position)
        end = self.toMapPoint(endPosition)

        if pos[0] == end[0] and pos[1] == end[1]:
            return -1, -1

        points = []
        temp = pos
        for _ in range(0, 3):
            self.nodeMap[temp[1]][temp[0]] = NodeType.VISITED.value
            temp = self.next(temp, end)
            points.append(temp)

        for point in points[1:]:
            self.nodeMap[point[1]][point[0]] = NodeType.EMPTY.value

        dx = np.diff([point[0] for point in points])
        dy = np.diff([point[1] for point in points])

        dx = np.array([abs(i) + 1 for i in dx])
        dy = np.array([abs(i) for i in dy])

        derivative = sum(dy / dx)

        print(derivative)

        return self.toGamePoint(points[0])

    def next(self, pos, endPos) -> tuple:

        startX, startY, endX, endY = self.findBorders(pos, 1)

        minManhattan = float('inf')
        best = -1, -1

        for j in range(startY, endY + 1):
            for i in range(startX, endX + 1):
                manhattan = self.euclidean((j, i), endPos)
                if self.nodeMap[j][i] == NodeType.EMPTY.value and manhattan < minManhattan:
                    minManhattan = manhattan
                    best = i, j

        return best

    @staticmethod
    def manhattan(a: tuple, b: tuple):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def euclidean(a: tuple, b: tuple):
        return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def initNodeMap(self, gameData: GameData):
        nodeMap = np.zeros(shape=self.mapShape)

        for hive in gameData.healthyHives + gameData.diseasedHives:

            hiveMapPoint = self.toMapPoint((hive.pos.x, hive.pos.y))
            startX, startY, endX, endY = self.findBorders(hiveMapPoint, self.HIVE_RADIUS)

            for i in range(startY, endY + 1):
                for j in range(startX, endX + 1):
                    nodeMap[i][j] = NodeType.HIVE.value

        return nodeMap

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
