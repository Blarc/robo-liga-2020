import numpy as np
from enum import Enum

from Game import Game
from algorithms.RobotAlgorithm import RobotAlgorithm


class NodeType(Enum):
    EMPTY = 0
    HIVE = 1
    VISITED = 2


class GreedyAlgorithm(RobotAlgorithm):

    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.nodeSize = game.BLOCK_SIZE // 5
        self.mapShape = (game.GAME_HEIGHT // self.nodeSize, game.GAME_WIDTH // self.nodeSize)
        self.path = self.run(game.robots[0].position)
        self.index = 0

    def getMotion(self, currentTrajectoryPoint: np.array) -> np.array:
        if self.index < len(self.path):
            tmp = self.path[self.index]
            self.index += 1
            return tmp

        return -1, -1

    def run(self, startPos):
        path = []
        nodeMap = self.initNodeMap()

        currentPos = self.toMapPoint(startPos)
        nodeMap[currentPos[0]][currentPos[1]] = NodeType.VISITED.value
        end = self.toMapPoint((2800, 1000))

        path.append(startPos)
        while currentPos[0] != end[0] or currentPos[1] != end[1]:
            currentPos = self.next(currentPos, end, nodeMap)
            path.append(self.toGamePoint(currentPos))

        return path

    def next(self, pos, endPos, nodeMap) -> tuple:

        startX = pos[0] - 1 if pos[0] - 1 >= 0 else pos[0]
        endX = pos[0] + 1 if pos[0] + 1 < self.mapShape[1] else pos[0]

        startY = pos[1] - 1 if pos[1] - 1 >= 0 else pos[0]
        endY = pos[1] + 1 if pos[1] + 1 < self.mapShape[0] else pos[0]

        minManhattan = float('inf')
        best = -1, -1

        for i in range(startY, endY + 1):
            for j in range(startX, endX + 1):
                manhattan = self.euclidean((j, i), endPos)
                if nodeMap[i][j] == NodeType.EMPTY.value and manhattan < minManhattan:
                    minManhattan = manhattan
                    best = j, i

        nodeMap[best[1]][best[0]] = NodeType.VISITED.value
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

            for i in range(hiveMapPoint[1] - 3, hiveMapPoint[1] + 3):
                for j in range(hiveMapPoint[0] - 3, hiveMapPoint[0] + 3):
                    nodeMap[i][j] = NodeType.HIVE.value

        return nodeMap

    def toMapPoint(self, point):
        return int(point[0]) // self.nodeSize, int(point[1]) // self.nodeSize

    def toGamePoint(self, point):
        return int(point[0]) * self.nodeSize, int(point[1]) * self.nodeSize
