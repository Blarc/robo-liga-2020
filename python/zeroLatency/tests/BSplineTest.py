import numpy as np
import scipy.interpolate as scipy_interpolate
import time


class BSplineAlgorithm:

    def __init__(self):
        super().__init__()
        self.robotPosition = (500, 1000)

    def getControlPoints(self):
        return [
            self.robotPosition,
            (1000, 1000),
            (1000, 1500),
            (1500, 1500),
            (1500, 1000),
            (2000, 1000),
            (2000, 1500),
            (2500, 1500),
            (2500, 250),
            (2000, 250),
            (2000, 750),
            (1500, 750),
            (1500, 250),
            (1000, 250),
            (1000, 750),
            (500, 750)
        ]

    def getPath(self):
        x = [tup[0] for tup in self.getControlPoints()]
        y = [tup[1] for tup in self.getControlPoints()]

        rax, ray = self.approximateBSplinePath(x, y, 50, 2)

        return list(map(tuple, zip(rax, ray)))

    @staticmethod
    def approximateBSplinePath(x: list, y: list, numberOfPoints: int, degree: int = 3) -> tuple:
        t = range(len(x))
        x_tup = scipy_interpolate.splrep(t, x, k=degree)
        y_tup = scipy_interpolate.splrep(t, y, k=degree)

        x_list = list(x_tup)
        x_list[1] = x + [0.0, 0.0, 0.0, 0.0]

        y_list = list(y_tup)
        y_list[1] = y + [0.0, 0.0, 0.0, 0.0]

        ipl_t = np.linspace(0.0, len(x) - 1, numberOfPoints)
        rx = scipy_interpolate.splev(ipl_t, x_list)
        ry = scipy_interpolate.splev(ipl_t, y_list)

        return rx, ry


if __name__ == '__main__':
    print("main")
    bSpline = BSplineAlgorithm()
    print("start")
    startTime = time.time()
    path = bSpline.getPath()
    endTime = time.time()

    for point in path:
        print(point)

    print(endTime - startTime)
