from typing import List

import numpy as np


class RobotAlgorithm:

    def getPath(self) -> List[tuple]:
        pass

    def getControlPoints(self) -> List[tuple]:
        pass

    def getMotion(self, currentTrajectoryPoint: np.array) -> np.array:
        pass

    def getHivePositions(self):
        return []

    def getBSpline(self):
        return []
