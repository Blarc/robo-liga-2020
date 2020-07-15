import numpy as np
from enum import Enum
import time


class NodeType(Enum):
    EMPTY = 0
    HIVE = 1
    VISITED = 2


class GreedyAlgorithm:

    GAME_WIDTH = 3500
    GAME_HEIGHT = 2000
    BLOCK_SIZE = 100
    MAX_FUTURE = 5

    def __init__(self):
        super().__init__()
        self.nodeSize = self.BLOCK_SIZE
        self.mapShape = (self.GAME_HEIGHT // self.nodeSize, self.GAME_WIDTH // self.nodeSize)
        self.hives = self.initHives()
        self.path = self.run((500, 1000))
        self.index = 0

    def run(self, startPos):
        print("start")
        startTime = time.time()
        path = []
        nodeMap = self.initNodeMap()

        currentPos = self.toMapPoint(startPos)
        nodeMap[currentPos[0]][currentPos[1]] = NodeType.VISITED.value
        end = self.toMapPoint((2800, 1000))

        path.append(startPos)
        counter = 0
        while (currentPos[0] != end[0] or currentPos[1] != end[1]) and counter < self.MAX_FUTURE:
            currentPos = self.next(currentPos, end, nodeMap)
            path.append(self.toGamePoint(currentPos))
            counter += 1

        endTime = time.time()
        print(endTime - startTime)

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

        for hive in self.hives:

            hiveMapPoint = self.toMapPoint(hive)

            for i in range(hiveMapPoint[1] - 3, hiveMapPoint[1] + 3):
                for j in range(hiveMapPoint[0] - 3, hiveMapPoint[0] + 3):
                    nodeMap[i][j] = NodeType.HIVE.value

        return nodeMap

    def toMapPoint(self, point):
        return int(point[0]) // self.nodeSize, int(point[1]) // self.nodeSize

    def toGamePoint(self, point):
        return int(point[0]) * self.nodeSize, int(point[1]) * self.nodeSize

    def initHives(self):
        hives = [(self.GAME_WIDTH / 2 - self.BLOCK_SIZE / 2, self.GAME_HEIGHT / 2 + 7 * self.BLOCK_SIZE / 2),
                 (self.GAME_WIDTH / 2 - self.BLOCK_SIZE / 2, self.GAME_HEIGHT / 2 + 5 * self.BLOCK_SIZE / 2),
                 (self.GAME_WIDTH / 2 - self.BLOCK_SIZE / 2, self.GAME_HEIGHT / 2 + 3 * self.BLOCK_SIZE / 2),
                 (self.GAME_WIDTH / 2 - self.BLOCK_SIZE / 2, self.GAME_HEIGHT / 2 + self.BLOCK_SIZE / 2),
                 (self.GAME_WIDTH / 2 - self.BLOCK_SIZE / 2, self.GAME_HEIGHT / 2 - self.BLOCK_SIZE / 2),
                 (self.GAME_WIDTH / 2 - self.BLOCK_SIZE / 2, self.GAME_HEIGHT / 2 - 3 * self.BLOCK_SIZE / 2),
                 (self.GAME_WIDTH / 2 - self.BLOCK_SIZE / 2, self.GAME_HEIGHT / 2 - 5 * self.BLOCK_SIZE / 2),
                 (self.GAME_WIDTH / 2 - self.BLOCK_SIZE / 2, self.GAME_HEIGHT / 2 - 7 * self.BLOCK_SIZE / 2)]

        return hives


if __name__ == '__main__':
    greedy = GreedyAlgorithm()
