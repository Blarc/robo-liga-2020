import numpy as np


def areEqual(a, b):
    return a[0] == b[0] and a[1] == b[1]


def manhattan(a: tuple, b: tuple):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean(a: tuple, b: tuple):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
