class Point:

    def __init__(self, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y

    def equals(self, that: 'Point'):
        return self.x == that.x and self.y == that.y
