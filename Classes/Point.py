import math
"""
    Točka na poligonu.
"""


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    """
        Evklidska razdalja med dvema točkama na poligonu.
    """

    def distance(self, point: 'Point') -> float:
        return math.sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2)
