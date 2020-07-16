from multiprocessing import Value, Array
from typing import List

import numpy as np
from enum import Enum
import time

from Entities import Hive, Point


class NodeType(Enum):
    EMPTY = 0
    HIVE = 1
    VISITED = 2


class GreedyAlgorithm:

    GAME_WIDTH = 3500
    GAME_HEIGHT = 2000
    BLOCK_SIZE = 100

    def __init__(self):
        super().__init__()
        self.nodeSize = self.BLOCK_SIZE
        self.mapShape = (self.GAME_HEIGHT // self.nodeSize, self.GAME_WIDTH // self.nodeSize)
        self.index = 0

    def run(self, startPos: Point, endPos: Point, hives: List[Hive]):
        print("start")
        path = []
        nodeMap = self.initNodeMap(hives)

        currentPos = self.toMapPoint(startPos)
        nodeMap[currentPos.y][currentPos.x] = NodeType.VISITED.value
        end = self.toMapPoint(endPos)

        # TODO do I want start pos in path? path.append(startPos)
        # counter = 0
        # while (currentPos.x != end.x or currentPos.y != end.y) and counter < 5:
        #     currentPos = self.next(currentPos, end, nodeMap)
        #     path.append(self.toGamePoint(currentPos))
        #     counter += 1

        # return path

        return self.toGamePoint(self.next(currentPos, end, nodeMap))

    def next(self, pos: Point, endPos: Point, nodeMap) -> Point:

        startX = pos.x - 1 if pos.x - 1 >= 0 else pos.x
        endX = pos.x + 1 if pos.x + 1 < self.mapShape[1] else pos.x

        startY = pos.y - 1 if pos.y - 1 >= 0 else pos.y
        endY = pos.y + 1 if pos.y + 1 < self.mapShape[0] else pos.y

        minManhattan = float('inf')
        best = -1, -1

        for i in range(startY, endY + 1):
            for j in range(startX, endX + 1):
                manhattan = self.euclidean(Point(j, i), endPos)
                if nodeMap[i][j] == NodeType.EMPTY.value and manhattan < minManhattan:
                    minManhattan = manhattan
                    best = j, i

        nodeMap[best[1]][best[0]] = NodeType.VISITED.value
        return Point(best[0], best[1])

    @staticmethod
    def manhattan(a: tuple, b: tuple):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def euclidean(a: Point, b: Point):
        return np.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

    def initNodeMap(self, hives: List[Hive]):
        nodeMap = np.zeros(shape=self.mapShape)

        for hive in hives:

            hiveMapPoint = self.toMapPoint(hive.pos)

            for i in range(hiveMapPoint.y - 3, hiveMapPoint.y + 3):
                for j in range(hiveMapPoint.x - 3, hiveMapPoint.x + 3):
                    nodeMap[i][j] = NodeType.HIVE.value

        return nodeMap

    def toMapPoint(self, point: Point) -> Point:
        return Point(int(point.x) // self.nodeSize, int(point.y) // self.nodeSize)

    def toGamePoint(self, point: Point) -> Point:
        return Point(int(point.x) * self.nodeSize, int(point.y) * self.nodeSize)

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

    def runProcess(self, startPos: Point, endPos: Point, hives: List[Hive], isLocked: Value, array: Array):
        isLocked.value = True
        array.value = self.run(startPos, endPos, hives)
        isLocked.value = False


if __name__ == '__main__':
    greedy = GreedyAlgorithm()
