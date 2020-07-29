from tkinter import Tk, Frame

from algorithms.AStar import AStar
from algorithms.BSpline import BSpline
from algorithms.DAS import DAS
from algorithms.DWA import DWA
from algorithms.Greedy import Greedy
from algorithms.DGA import DGA
from Board import Board
from Game import Game
from algorithms.Potential import Potential


class RobotSimulator(Frame):

    def __init__(self, algorithm: int):
        super().__init__()

        self.master.title("Robot simulator 2.0")
        game = Game(23)

        if algorithm == 0:
            self.board = Board(game, BSpline(game))
        elif algorithm == 1:
            self.board = Board(game, DWA(game))
        elif algorithm == 2:
            self.board = Board(game, Greedy(game))
        elif algorithm == 3:
            self.board = Board(game, DGA(game, (500, 1000)))
        elif algorithm == 4:
            self.board = Board(game, AStar(game))
        elif algorithm == 5:
            self.board = Board(game, DAS(game))
        elif algorithm == 6:
            self.board = Board(game, Potential(game))

        self.pack()


def main():
    root = Tk()
    RobotSimulator(6)
    root.mainloop()


if __name__ == '__main__':
    main()
