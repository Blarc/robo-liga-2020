from tkinter import Tk, Frame

from BSplineAlgorithm import BSplineAlgorithm
from Board import Board
from DynamicWindowApproachAlgorithm import DynamicWindowApproachAlgorithm
from Game import Game


class RobotSimulator(Frame):

    def __init__(self, algorithm: int):
        super().__init__()

        self.master.title("Robot simulator 2.0")
        game = Game(4)

        if algorithm == 0:
            self.board = Board(game, BSplineAlgorithm(game))
        elif algorithm == 1:
            self.board = Board(game, DynamicWindowApproachAlgorithm(game))

        self.pack()


def main():
    root = Tk()
    RobotSimulator(0)
    root.mainloop()


if __name__ == '__main__':
    main()
