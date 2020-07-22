import heapq
import time
from enum import Enum

import numpy as np

from Game import Game
from algorithms.RobotAlgorithm import RobotAlgorithm
from algorithms.Utils import euclidean


class NodeType(Enum):
    EMPTY = 0
    HIVE = 1
    CLOSED = 2


class Node:

    def __init__(self, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y

        self.gCost = 0
        self.hCost = 0

        self.type = NodeType.EMPTY
        self.parent = None

    def getFCost(self):
        return self.gCost + self.hCost

    def hasParent(self) -> bool:
        return self.parent is not None

    def isClosed(self):
        return self.type == NodeType.CLOSED

    def setClosed(self):
        self.type = NodeType.CLOSED

    def cost(self, other: 'Node'):
        return euclidean((self.x, self.y), (other.x, other.y))

    def __lt__(self, other: 'Node'):
        return self.getFCost() < other.getFCost()

    def __eq__(self, other: 'Node'):
        return self.x == other.x and self.y == other.y


class AStar(RobotAlgorithm):

    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.nodeSize = game.BLOCK_SIZE
        self.mapShape = (game.GAME_WIDTH // self.nodeSize, game.GAME_HEIGHT // self.nodeSize)

        # A STAR
        self.openNodes = []
        self.nodeMap = None
        self.start = None
        self.end = None

        # PATH
        self.index = 0
        startTime = time.time()
        self.path = self.run(game.robots[0].position, (2800, 1000))
        endTime = time.time()
        print(endTime - startTime)

    def getMotion(self, currentTrajectoryPoint: np.array) -> np.array:

        if len(self.path) != 0:
            return self.path.pop()

        else:
            return -1, -1


    def run(self, startPos, endPos):

        self.openNodes = []
        self.initNodeMap()

        startPos = self.toMapPoint(startPos)
        endPos = self.toMapPoint(endPos)

        self.start = self.nodeMap[startPos[0]][startPos[1]]
        self.end = self.nodeMap[endPos[0]][endPos[1]]

        heapq.heappush(self.openNodes, self.start)

        while len(self.openNodes) != 0:
            current = heapq.heappop(self.openNodes)
            current.setClosed()

            if current.__eq__(self.end):
                return self.getPathA(current)
            else:
                self.checkNeighbours(current)

    def checkNeighbours(self, current: Node):

        startX = current.x - 1 if current.x - 1 >= 0 else current.x
        endX = current.x + 1 if current.x + 1 < self.mapShape[0] else current.x

        startY = current.y - 1 if current.y - 1 >= 0 else current.y
        endY = current.y + 1 if current.y + 1 < self.mapShape[1] else current.y

        for i in range(startX, endX + 1):
            for j in range(startY, endY + 1):

                node = self.nodeMap[i][j]
                # print(i, j, node.type)
                if not node.type == NodeType.HIVE and not node.isClosed() and (not node.hasParent() or node.parent.gCost > current.gCost):
                    node.parent = current
                    node.gCost = current.cost(node) + current.gCost
                    node.hCost = node.cost(self.end)
                    heapq.heappush(self.openNodes, node)

    def initNodeMap(self):

        self.nodeMap = [[Node(j, i) for i in range(self.mapShape[1])] for j in range(self.mapShape[0])]

        for hive in self.game.hives:
            hiveMapPoint = self.toMapPoint(hive.position)

            for i in range(hiveMapPoint[0] - 1, hiveMapPoint[0] + 2):
                for j in range(hiveMapPoint[1] - 1, hiveMapPoint[1] + 2):
                    self.nodeMap[i][j].type = NodeType.HIVE

    def getPathA(self, current: Node):
        path = []
        while current.parent is not None:
            path.append(self.toGamePoint((current.x, current.y)))
            current = current.parent

        return path

    def toMapPoint(self, point) -> tuple:
        return int(point[0]) // self.nodeSize, int(point[1]) // self.nodeSize

    def toGamePoint(self, point) -> tuple:
        return int(point[0]) * self.nodeSize, int(point[1]) * self.nodeSize
