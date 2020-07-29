#!/usr/bin/env python3

"""
Program za vodenje robota EV3
[Robo liga FRI 2020: Čebelnjak]
@Copyright: ZeroLatency
"""

import sys
from time import time

from ev3dev.ev3 import Button

from Connection import Connection
from Constants import SERVER_IP, GAME_ID, ROBOT_ID
from Controller import Controller
from Entities import Team, GameData, State, Point
from GreedyAlgorithm import GreedyAlgorithm

# ------------------------------------------------------------------------------------------------------------------- #

print('Priprava tipal ... ', end='', flush=True)
btn = Button()
print('OK!')

url = SERVER_IP + GAME_ID
print('Vspostavljanje povezave z naslovom ' + url + ' ... ', end='', flush=True)
conn = Connection(url)
print('OK!')

print('Zakasnitev v komunikaciji s streznikom ... ', end='', flush=True)
print('%.4f s' % (conn.testDelay(numOfIterations=10)))

# ------------------------------------------------------------------------------------------------------------------- #

gameState = conn.request()

homeTeamTag = 'undefined'
enemyTeamTag = 'undefined'

team1 = Team(gameState["teams"]["team1"])
team2 = Team(gameState["teams"]["team2"])

if ROBOT_ID == team1.id:
    homeTeamTag = 'team1'
    enemyTeamTag = 'team2'
elif ROBOT_ID == team2.id:
    homeTeamTag = 'team2'
    enemyTeamTag = 'team1'
else:
    print('Robot ne tekmuje.')
    sys.exit(0)

print('Robot tekmuje in ima interno oznako "' + homeTeamTag + '"')

# ------------------------------------------------------------------------------------------------------------------- #

bottomLeft2 = gameState['fields']['baskets']['team1']['bottomRight']
topLeft2 = gameState['fields']['baskets']['team1']['topRight']
topRight2 = gameState['fields']['baskets']['team2']['topLeft']
bottomRight2 = gameState['fields']['baskets']['team2']['bottomLeft']

targetList = [
    Point(bottomLeft2['x'], bottomLeft2['y']),
    Point(bottomLeft2['x'], bottomLeft2['y'] + 100),
    Point(bottomLeft2['x'], bottomLeft2['y'] + 200),
    Point(bottomLeft2['x'], bottomLeft2['y'] + 300),
    Point(bottomLeft2['x'], bottomLeft2['y'] + 400),
    Point(topLeft2['x'], topLeft2['y']),
    Point(1300, 1500),
    Point(1400, 1500),
    Point(1600, 900),
    Point(1750, 1000),
    Point(1800, 1100),
    Point(2100, 1500),
    Point(2200, 1500),
    Point(topRight2['x'], topRight2['y']),
    Point(topRight2['x'], topRight2['y'] - 100),
    Point(topRight2['x'], topRight2['y'] - 200),
    Point(topRight2['x'], topRight2['y'] - 300),
    Point(topRight2['x'], topRight2['y'] - 400),
    Point(bottomRight2['x'], bottomRight2['y']),
    Point(2200, 500),
    Point(2100, 500),
    Point(1900, 900),
    Point(1750, 1000),
    Point(1600, 900),
    Point(1400, 500),
    Point(1300, 500)
]

print('Seznam ciljnih tock:')
for tmpGoal in targetList:
    print('\t' + str(tmpGoal))

# ------------------------------------------------------------------------------------------------------------------- #
# GLOBAL VARIABLES

gameData = GameData(gameState, homeTeamTag, enemyTeamTag)
controller = Controller(initialState=State.IDLE)
endPosition = (1000, 500)

algorithm = GreedyAlgorithm(gameData)


targetTuple = algorithm.run((gameData.homeRobot.pos.x, gameData.homeRobot.pos.y), endPosition, (1, 0))

target = Point(targetTuple[0], targetTuple[1])

targetIndex = 0
timeOld = time()

# ------------------------------------------------------------------------------------------------------------------- #
# MAIN LOOP

print('Izvajam glavno zanko. Prekini jo s pritiskom na tipko DOL.')
print('Cakam na zacetek tekme ...')

doMainLoop = True
while doMainLoop and not btn.down:

    timeNow = time()
    loopTime = timeNow - timeOld
    timeOld = timeNow

    gameState = conn.request()
    if gameState == -1:
        print('Napaka v paketu, ponovni poskus ...')
    else:
        gameData = GameData(gameState, homeTeamTag, enemyTeamTag)
        controller.update(gameData, target)

        if gameData.gameOn and controller.isRobotAlive():

            # ------------------------------------------------------------------------------------------------------- #
            # IDLE STATE

            if controller.state == State.IDLE:
                print(State.IDLE)

                # controller.setSpeedToZero()

                if not controller.atTargetEPS():
                    controller.state = State.DRIVE_STRAIGHT
                    robotNearTargetOld = False
                else:
                    controller.state = State.LOAD_NEXT_TARGET

            # ------------------------------------------------------------------------------------------------------- #
            # LOAD NEXT TARGET STATE

            elif controller.state == State.LOAD_NEXT_TARGET:
                print(State.LOAD_NEXT_TARGET)

                targetTuple = algorithm.run((target.x, target.y), endPosition, controller.getAngleApprox())

                if targetTuple[0] == -1:
                    controller.robotDie()

                target = Point(targetTuple[0], targetTuple[1])
                controller.state = State.DRIVE_STRAIGHT

            # ------------------------------------------------------------------------------------------------------- #
            # DRIVE STRAIGHT STATE

            elif controller.state == State.DRIVE_STRAIGHT:
                # print(State.DRIVE_STRAIGHT)

                if controller.stateChanged:
                    controller.resetPIDStraight()

                if controller.atTargetHIST():
                    # controller.setSpeedToZero()
                    controller.state = State.LOAD_NEXT_TARGET

                else:
                    controller.updatePIDStraight()
                    controller.state = State.DRIVE_STRAIGHT

            # ------------------------------------------------------------------------------------------------------- #
            # SPIN MOTORS

            controller.runMotors()

        # ----------------------------------------------------------------------------------------------------------- #
        # BREAK MOTORS
        else:
            controller.breakMotors()

# ------------------------------------------------------------------------------------------------------- #
# END
controller.robotDie()
