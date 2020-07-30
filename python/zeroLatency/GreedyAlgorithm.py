from typing import List, Tuple

from time import time

import numpy as np
import scipy.interpolate as scipy_interpolate

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
    SPLINE_DEGREE = 2
    SPLINE_NUM_POINTS = 5

    def __init__(self, gameData: GameData):
        super().__init__()
        self.mapShape = (self.GAME_HEIGHT // self.NODE_SIZE, self.GAME_WIDTH // self.NODE_SIZE)
        self.nodeMap = self.initNodeMap(gameData)
        self.printMap()

    def run(self, position: tuple, endPosition: tuple, dirPoint: tuple):

        pos = self.toMapPoint(position)
        end = self.toMapPoint(endPosition)

        if pos[0] == end[0] and pos[1] == end[1]:
            return -1, -1

        self.nodeMap[pos[1]][pos[0]] = NodeType.VISITED.value

        first = self.next(pos, end, dirPoint)
        self.nodeMap[first[1]][first[0]] = NodeType.VISITED.value
        second = self.next(first, end, dirPoint)
        self.nodeMap[second[1]][second[0]] = NodeType.VISITED.value
        third = self.next(second, end, dirPoint)

        self.nodeMap[first[1]][first[0]] = NodeType.EMPTY.value
        self.nodeMap[second[1]][second[0]] = NodeType.EMPTY.value

        return [self.toGamePoint(first), self.toGamePoint(second), self.toGamePoint(third)]

    def next(self, pos, endPos, dirPoint: tuple) -> tuple:

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
        startTime = time()
        nodeMap = np.zeros(shape=self.mapShape)

        for hive in gameData.healthyHives + gameData.diseasedHives:

            hiveMapPoint = self.toMapPoint((hive.pos.x, hive.pos.y))
            startX, startY, endX, endY = self.findBorders(hiveMapPoint, self.HIVE_RADIUS)

            for i in range(startY, endY + 1):
                for j in range(startX, endX + 1):
                    nodeMap[i][j] = NodeType.HIVE.value

        print(time() - startTime)
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

    def calcBSpline(self, points: List[Tuple]):
        t = range(len(points))

        x = [point[0] for point in points]
        y = [point[1] for point in points]

        x_tup = scipy_interpolate.splrep(t, x, k=self.SPLINE_DEGREE)
        y_tup = scipy_interpolate.splrep(t, y, k=self.SPLINE_DEGREE)

        x_list = list(x_tup)
        x_list[1] = x + [0.0, 0.0, 0.0, 0.0]

        y_list = list(y_tup)
        y_list[1] = y + [0.0, 0.0, 0.0, 0.0]

        ipl_t = np.linspace(0.0, len(x) - 1, self.SPLINE_NUM_POINTS)
        rx = scipy_interpolate.splev(ipl_t, x_list)
        ry = scipy_interpolate.splev(ipl_t, y_list)

        return rx, ry

    def toMapPoint(self, point):
        return round(point[0] / self.NODE_SIZE), round(point[1] / self.NODE_SIZE)

    def toGamePoint(self, point):
        return int(point[0]) * self.NODE_SIZE, int(point[1]) * self.NODE_SIZE

    def printMap(self, pos=(31, 10)):
        print(pos)
        for j in range(self.mapShape[0]):
            for i in range(self.mapShape[1]):
                if pos[0] == i and pos[1] == j:
                    print('\033[1m' + "|RR" + '\033[0m', end="")
                elif self.nodeMap[j][i] == NodeType.EMPTY.value:
                    print("|__", end="")
                elif self.nodeMap[j][i] == NodeType.HIVE.value:
                    print('\033[1m' + "|HH" + '\033[0m', end="")

            print("|")
