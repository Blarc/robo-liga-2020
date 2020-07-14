from tkinter import Tk, Frame

from algorithms.BSplineAlgorithm import BSplineAlgorithm
from Board import Board
from algorithms.DWAAlgorithm import DWAAlgorithm
from Game import Game


class RobotSimulator(Frame):

    def __init__(self, algorithm: int):
        super().__init__()

        self.master.title("Robot simulator 2.0")
        game = Game(3)

        if algorithm == 0:
            self.board = Board(game, BSplineAlgorithm(game))
        elif algorithm == 1:
            self.board = Board(game, DWAAlgorithm(game))

        self.pack()


def main():
    root = Tk()
    RobotSimulator(1)
    root.mainloop()


if __name__ == '__main__':
    main()
