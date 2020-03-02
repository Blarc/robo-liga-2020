from enum import Enum


class State(Enum):
    """
    Stanja robota.
    """

    def __str__(self):
        return str(self.name)

    GET_APPLE = 0
    GET_TURN = 1
    GET_STRAIGHT = 2
    HOME = 3
    HOME_TURN = 4
    HOME_STRAIGHT = 5
    BACK_OFF = 6
    ENEMY_HOME = 7
    ENEMY_HOME_TURN = 8
    ENEMY_HOME_STRAIGHT = 9
    GET_BAD_APPLE = 10