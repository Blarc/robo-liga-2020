class Field:

    def __init__(self, upperLeft: tuple, upperRight: tuple, bottomRight: tuple, bottomLeft: tuple):
        super().__init__()
        self.upperLeft = upperLeft
        self.upperRight = upperRight
        self.bottomRight = bottomRight
        self.bottomLeft = bottomLeft
