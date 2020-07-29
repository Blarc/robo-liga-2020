from typing import List

from Connection import Connection
from Field import Field
from Hive import Hive, HiveType
from Robot import Robot


class Game:
    GAME_WIDTH = 3500
    GAME_HEIGHT = 2000
    BLOCK_SIZE = 100

    storages = [
        Field((0, 500), (500, 500), (500, 1500), (0, 1500)),
        Field((3000, 500), (3500, 500), (3500, 1500), (3000, 1500))
    ]

    def __init__(self, setup: int):
        super().__init__()

        self.hives: List[Hive] = []
        self.robots: List[Robot] = []

        if setup == 0:
            self.setupZero()
        elif setup == 1:
            self.setupOne()
        elif setup == 2:
            self.setupTwo()
        elif setup == 3:
            self.setupThree()
        elif setup == 4:
            self.setupFour()
        elif setup == 5:
            self.setupFive()
        elif setup == 6:
            self.setupSix()
        elif setup == 23:
            self.setupLive()

    def setupLive(self):
        SERVER_IP = "192.168.2.3:8088/game/"
        GAME_ID = "5f44"

        url = SERVER_IP + GAME_ID
        print('Vspostavljanje povezave z naslovom ' + url + ' ... ', end='', flush=True)
        conn = Connection(url)
        print('OK!')

        gameState = conn.request()
        if gameState == -1:
            print('Napaka v paketu')
        else:
            self.robots.append(Robot((500, 1000), 90))

            for hiveId, hiveData in gameState['objects']['hives'].items():
                x = hiveData["position"]["x"]
                y = hiveData["position"]["y"]

                x = abs(Game.GAME_WIDTH - x)

                hivePos = (x, y)
                hiveType = HiveType.HEALTHY if hiveData["type"] == "HIVE_HEALTHY" else HiveType.DISEASED
                self.hives.append(Hive(hivePos, hiveType))

    def setupZero(self):
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 0 + Game.BLOCK_SIZE / 2),
                               HiveType.HEALTHY))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 1 + Game.BLOCK_SIZE / 2),
                               HiveType.HEALTHY))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 2 + Game.BLOCK_SIZE / 2),
                               HiveType.HEALTHY))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 3 + Game.BLOCK_SIZE / 2),
                               HiveType.HEALTHY))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 4 + Game.BLOCK_SIZE / 2),
                               HiveType.HEALTHY))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 5 + Game.BLOCK_SIZE / 2),
                               HiveType.HEALTHY))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 6 + Game.BLOCK_SIZE / 2),
                               HiveType.HEALTHY))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 7 + Game.BLOCK_SIZE / 2),
                               HiveType.HEALTHY))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 8 + Game.BLOCK_SIZE / 2),
                               HiveType.HEALTHY))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 9 + Game.BLOCK_SIZE / 2),
                               HiveType.HEALTHY))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 10 + Game.BLOCK_SIZE / 2),
                               HiveType.DISEASED))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 11 + Game.BLOCK_SIZE / 2),
                               HiveType.DISEASED))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 12 + Game.BLOCK_SIZE / 2),
                               HiveType.DISEASED))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 13 + Game.BLOCK_SIZE / 2),
                               HiveType.DISEASED))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 14 + Game.BLOCK_SIZE / 2),
                               HiveType.DISEASED))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 15 + Game.BLOCK_SIZE / 2),
                               HiveType.DISEASED))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 16 + Game.BLOCK_SIZE / 2),
                               HiveType.DISEASED))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 17 + Game.BLOCK_SIZE / 2),
                               HiveType.DISEASED))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 18 + Game.BLOCK_SIZE / 2),
                               HiveType.DISEASED))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE * 19 + Game.BLOCK_SIZE / 2),
                               HiveType.DISEASED))

        self.hives.append(Hive((Game.BLOCK_SIZE * 0 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 1 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 2 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 3 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 4 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 5 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 6 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 7 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 8 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 9 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 10 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 11 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 12 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 13 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 14 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 15 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 16 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 17 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 18 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 19 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 20 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 21 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 22 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 23 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 24 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 25 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 26 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 27 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 28 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 29 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 30 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 31 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 32 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 33 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))
        self.hives.append(Hive((Game.BLOCK_SIZE * 34 + Game.BLOCK_SIZE / 2, Game.BLOCK_SIZE / 2), HiveType.HEALTHY))

        self.robots.append(Robot((500, 1000), 90))

    def setupOne(self):
        self.robots.append(Robot((500, 1000), 90))

        self.hives.append(Hive(
            (Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 + 7 * Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 + 5 * Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 + 3 * Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 + Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 - Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 - 3 * Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 - 5 * Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 - 7 * Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

    def setupTwo(self):
        self.robots.append(Robot((500, 1000), 90))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 4 - Game.BLOCK_SIZE / 2),
                               HiveType.HEALTHY))
        self.hives.append(Hive(
            (Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT - Game.GAME_HEIGHT / 4 + Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

    def setupThree(self):
        self.robots.append(Robot((500, 1000), 90))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 4 - Game.BLOCK_SIZE / 2),
                               HiveType.HEALTHY))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 4 + Game.BLOCK_SIZE / 2),
                               HiveType.HEALTHY))
        self.hives.append(
            Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 4 + 3 * Game.BLOCK_SIZE / 2),
                 HiveType.HEALTHY))
        self.hives.append(
            Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 4 + 5 * Game.BLOCK_SIZE / 2),
                 HiveType.HEALTHY))
        self.hives.append(
            Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 4 + 7 * Game.BLOCK_SIZE / 2),
                 HiveType.HEALTHY))
        self.hives.append(
            Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 4 + 9 * Game.BLOCK_SIZE / 2),
                 HiveType.HEALTHY))
        self.hives.append(
            Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 4 + 11 * Game.BLOCK_SIZE / 2),
                 HiveType.HEALTHY))
        self.hives.append(
            Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 4 + 13 * Game.BLOCK_SIZE / 2),
                 HiveType.HEALTHY))
        self.hives.append(
            Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 4 + 15 * Game.BLOCK_SIZE / 2),
                 HiveType.HEALTHY))

    def setupFour(self):
        self.robots.append(Robot((500, 1000), 90))
        self.hives.append(Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 4 - Game.BLOCK_SIZE / 2),
                               HiveType.HEALTHY))
        self.hives.append(Hive(
            (Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT - Game.GAME_HEIGHT / 4 + Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive((Game.GAME_WIDTH / 3 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2),
                               HiveType.HEALTHY))

        self.hives.append(Hive((Game.GAME_WIDTH - Game.GAME_WIDTH / 3 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2),
                               HiveType.HEALTHY))

    def setupFive(self):
        self.robots.append(Robot((500, 1000), 90))
        self.hives.append(Hive(
            (Game.GAME_WIDTH / 4 + 100 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 + 7 * Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (Game.GAME_WIDTH / 4 + 100 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 + 5 * Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (Game.GAME_WIDTH / 4 + 100 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 + 3 * Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (Game.GAME_WIDTH / 4 + 100 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 + Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (Game.GAME_WIDTH / 4 + 100 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 - Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (Game.GAME_WIDTH / 4 + 100 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 - 3 * Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (Game.GAME_WIDTH / 4 + 100 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 - 5 * Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (Game.GAME_WIDTH / 4 + 100 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 - 7 * Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        # ------------------------------------------------------------------------------------------------------------#

        self.hives.append(Hive(
            (3 * Game.GAME_WIDTH / 4 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 + 7 * Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (3 * Game.GAME_WIDTH / 4 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 + 5 * Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (3 * Game.GAME_WIDTH / 4 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 + 3 * Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (3 * Game.GAME_WIDTH / 4 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 + Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (3 * Game.GAME_WIDTH / 4 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 - Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (3 * Game.GAME_WIDTH / 4 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 - 3 * Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (3 * Game.GAME_WIDTH / 4 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 - 5 * Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

        self.hives.append(Hive(
            (3 * Game.GAME_WIDTH / 4 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2 - 7 * Game.BLOCK_SIZE / 2),
            HiveType.HEALTHY))

    def setupSix(self):
        self.robots.append(Robot((500, 1000), 90))
        self.hives.append(
            Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 4 - Game.BLOCK_SIZE / 2),
                 HiveType.HEALTHY))
        self.hives.append(
            Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, Game.GAME_HEIGHT / 2),
                 HiveType.HEALTHY))
        self.hives.append(
            Hive((Game.GAME_WIDTH / 2 - Game.BLOCK_SIZE / 2, (3 * Game.GAME_HEIGHT) / 4 + Game.BLOCK_SIZE / 2),
                 HiveType.HEALTHY))
