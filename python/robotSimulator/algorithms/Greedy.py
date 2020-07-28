import numpy as np
import scipy.interpolate as scipy_interpolate
from enum import Enum

from Game import Game
from algorithms.RobotAlgorithm import RobotAlgorithm



class NodeType(Enum):
    EMPTY = 0
    HIVE = 1
    VISITED = 2


class Greedy(RobotAlgorithm):

    HIVE_RADIUS = 2
    SPLINE_DEGREE = 2
    SPLINE_NUM_POINTS = 5

    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.nodeSize = 100
        self.mapShape = (game.GAME_HEIGHT // self.nodeSize, game.GAME_WIDTH // self.nodeSize)
        self.nodeMap = self.initNodeMap()
        self.end = self.toMapPoint((2800, 1000))
        self.path = []

    def getMotion(self, currentTrajectoryPoint: np.array) -> np.array:

        pos = self.toMapPoint(currentTrajectoryPoint)
        self.nodeMap[pos[1]][pos[0]] = NodeType.VISITED.value

        result = self.next(pos)

        if result[0] == self.end[0] and result[1] == self.end[1]:
            return -1, -1

        return self.toGamePoint(self.next(pos))

    def getBSplineOld(self):
        t = range(len(self.path))

        x = [point[0] for point in self.path]
        y = [point[1] for point in self.path]

        x_tup = scipy_interpolate.splrep(t, x, k=self.SPLINE_DEGREE)
        y_tup = scipy_interpolate.splrep(t, y, k=self.SPLINE_DEGREE)

        x_list = list(x_tup)
        x_list[1] = x + [0.0, 0.0, 0.0, 0.0]

        y_list = list(y_tup)
        y_list[1] = y + [0.0, 0.0, 0.0, 0.0]

        ipl_t = np.linspace(0.0, len(x) - 1, self.SPLINE_NUM_POINTS)
        rx = scipy_interpolate.splev(ipl_t, x_list)
        ry = scipy_interpolate.splev(ipl_t, y_list)

        return list(zip(rx, ry))

    def next(self, pos) -> tuple:

        startX, startY, endX, endY = self.findBorders(pos, 1)

        minManhattan = float('inf')
        best = -1, -1

        for i in range(startY, endY + 1):
            for j in range(startX, endX + 1):
                manhattan = self.euclidean((j, i), self.end)
                if self.nodeMap[i][j] == NodeType.EMPTY.value and manhattan < minManhattan:
                    minManhattan = manhattan
                    best = j, i

        return best

    @staticmethod
    def manhattan(a: tuple, b: tuple):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def euclidean(a: tuple, b: tuple):
        return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def initNodeMap(self):
        nodeMap = np.zeros(shape=self.mapShape)

        for hive in self.game.hives:

            hiveMapPoint = self.toMapPoint(hive.position)
            startX, startY, endX, endY = self.findBorders(hiveMapPoint, self.HIVE_RADIUS)

            for y in range(startY, endY + 1):
                for x in range(startX, endX + 1):
                    nodeMap[y][x] = NodeType.HIVE.value

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

    def toMapPoint(self, point: tuple):
        return round(point[0] / self.nodeSize), round(point[1] / self.nodeSize)

    def toGamePoint(self, point: tuple):
        return int(point[0]) * self.nodeSize, int(point[1]) * self.nodeSize

    def getHivePositions(self):
        hives = []
        for y in range(self.mapShape[0]):
            for x in range(self.mapShape[1]):
                if self.nodeMap[y][x] == NodeType.HIVE.value:
                    hives.append(self.toGamePoint((x, y)))

        return hives

