import math
from tkinter import Canvas

import numpy as np

from Game import Game
from Hive import HiveType
from algorithms import RobotAlgorithm


class BoardCons:
    B_WIDTH = 875
    B_HEIGHT = 500
    B_PADDING = 30
    BLOCK_SIZE = 25
    W_WIDTH = B_WIDTH + 2 * B_PADDING
    W_HEIGHT = B_HEIGHT + 2 * B_PADDING
    DELAY = 50


class Board(Canvas):

    def __init__(self, game: Game, algorithm: RobotAlgorithm):
        super().__init__(width=BoardCons.W_WIDTH, height=BoardCons.W_HEIGHT, background="gray98",
                         highlightthickness=0)
        self.game = game
        self.algorithm = algorithm
        self.robotTrajectoryPoint: np.array = np.array(
            [game.robots[0].position[0], game.robots[0].position[1], math.pi / 8.0, 0.0, 0.0]
        )
        self.arrow2 = None
        self.initUI()
        self.pack()

    def initUI(self):

        self.drawBoard()
        self.drawBlocks()

        self.drawBlock(self.gamePointToBoardPoint((2800, 1000)), "gold")

        # self.drawPath(self.algorithm.getControlPoints(), canvas, "blue")
        # self.drawPath(self.algorithm.getPath(), canvas, "red")

        self.after(BoardCons.DELAY, self.onTimer)

    @staticmethod
    def translateToBoardPoint(point: tuple) -> tuple:
        return point[0] + BoardCons.B_PADDING, point[1] + BoardCons.B_PADDING

    def gamePointToBoardPoint(self, point: tuple) -> tuple:
        ratio = Game.BLOCK_SIZE / BoardCons.BLOCK_SIZE
        return self.translateToBoardPoint((point[0] / ratio, point[1] / ratio))

    def drawBoard(self):

        # draw grid
        gridSize = (BoardCons.BLOCK_SIZE / 5)
        for i in range(1, int(BoardCons.B_WIDTH / gridSize)):
            self.drawLine(
                self.translateToBoardPoint((i * gridSize, 0)),
                self.translateToBoardPoint((i * gridSize, BoardCons.B_HEIGHT)),
                "gray90"
            )

        for i in range(1, int(BoardCons.B_HEIGHT / gridSize)):
            self.drawLine(
                self.translateToBoardPoint((0, i * gridSize)),
                self.translateToBoardPoint((BoardCons.B_WIDTH, i * gridSize)),
                "gray90"
            )

        # draw borders
        self.drawRect(
            self.translateToBoardPoint((0, 0)),
            self.translateToBoardPoint((BoardCons.B_WIDTH, BoardCons.B_HEIGHT))
        )

        # draw storages
        self.drawRect(
            self.gamePointToBoardPoint(Game.storages[0].upperLeft),
            self.gamePointToBoardPoint(Game.storages[0].bottomRight),
            fill="blue")

        self.drawRect(
            self.gamePointToBoardPoint(Game.storages[1].upperLeft),
            self.gamePointToBoardPoint(Game.storages[1].bottomRight),
            fill="red")

    def drawBlocks(self):
        for hive in self.game.hives:
            point = self.gamePointToBoardPoint(hive.position)

            if hive.type == HiveType.HEALTHY:
                self.drawBlock(point, "green")
            else:
                self.drawBlock(point, "brown")

        point = self.gamePointToBoardPoint((self.robotTrajectoryPoint[0], self.robotTrajectoryPoint[1]))
        self.drawArrow2()

        self.drawBlock(point, "cyan", "robot")

    def drawBlock(self, a: tuple, color: str, tag: str = ""):
        self.drawRect(
            (a[0] - BoardCons.BLOCK_SIZE / 2, a[1] - BoardCons.BLOCK_SIZE / 2),
            (a[0] + BoardCons.BLOCK_SIZE / 2, a[1] + BoardCons.BLOCK_SIZE / 2),
            fill=color,
            tag=tag
        )

    def drawLine(self, a: tuple, b: tuple, color: str = "black"):
        self.create_line(a[0], a[1], b[0], b[1], fill=color)

    def drawRect(self, a: tuple, b: tuple, outline: str = "black", fill: str = "", tag: str = ""):
        self.create_rectangle(a[0], a[1], b[0], b[1], outline=outline, fill=fill, tag=tag)

    def drawArrow(self, a: tuple, b: tuple, color: str, tag: str = ""):
        return self.create_line(a[0], a[1], b[0], b[1], arrow="last", fill=color, tag=tag)

    def drawArrow2(self, length=0.1):
        point = self.gamePointToBoardPoint((self.robotTrajectoryPoint[0], self.robotTrajectoryPoint[1]))
        self.arrow2 = self.drawArrow(
            point,
            (
                point[0] + length * point[0] * math.cos(self.robotTrajectoryPoint[2]),
                point[1] + length * point[1] * math.sin(self.robotTrajectoryPoint[2])
            ),
            "black",
            "arrow2"
        )

    def drawPath(self, points: np.array, color: str):
        for previous, current in zip(points, points[1:]):
            self.drawArrow(
                self.gamePointToBoardPoint(previous),
                self.gamePointToBoardPoint(current),
                color)

    def onTimer(self):

        self.robotTrajectoryPoint: np.array = self.algorithm.getMotion(self.robotTrajectoryPoint)

        if self.robotTrajectoryPoint[0] == -1:
            return

        robotPoint: tuple = (self.robotTrajectoryPoint[0], self.robotTrajectoryPoint[1])

        boardPoint = self.gamePointToBoardPoint(robotPoint)

        self.drawRect((boardPoint[0] - 2, boardPoint[1] - 2), (boardPoint[0] + 2, boardPoint[1] + 2), fill="red")

        tag = self.find_withtag("robot")
        self.moveto(tag, boardPoint[0] - BoardCons.BLOCK_SIZE / 2, boardPoint[1] - BoardCons.BLOCK_SIZE / 2)

        self.delete(self.arrow2)
        self.drawArrow2()

        self.after(BoardCons.DELAY, self.onTimer)
