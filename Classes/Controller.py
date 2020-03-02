import math
from collections import deque

from Classes import Constants
from nabiralec import State


class Controller:
    def __init__(self):
        self.speedRight: int = 0
        self.speedLeft: int = 0

        self.speedRightOld: int = 0
        self.speedLeftOld: int = 0

        self.robotDirHist: deque = deque([180.0] * Constants.HIST_QUEUE_LENGTH)
        self.robotDistHist: deque = deque([math.inf] * Constants.HIST_QUEUE_LENGTH)

        self.state: State = -1
        self.stateOld: State = -1

    

