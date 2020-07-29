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
    Point(500, 1000),
    Point(3000, 1000)
]

print('Seznam ciljnih tock:')
for tmpGoal in targetList:
    print('\t' + str(tmpGoal))

# ------------------------------------------------------------------------------------------------------------------- #
# GLOBAL VARIABLES

gameData = GameData(gameState, homeTeamTag, enemyTeamTag)
controller = Controller(initialState=State.IDLE)

targetIndex = 0
target = targetList[targetIndex]

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
        controller.getClosesObstacleOnPath()

        if gameData.gameOn and controller.isRobotAlive():

            # ------------------------------------------------------------------------------------------------------- #
            # IDLE STATE

            if controller.state == State.IDLE:
                print(State.IDLE)

                if not controller.atTargetEPS():
                    controller.state = State.CHECK_OBSTACLES
                    robotNearTargetOld = False
                else:
                    controller.state = State.LOAD_NEXT_TARGET

            # ------------------------------------------------------------------------------------------------------- #
            # LOAD NEXT TARGET STATE

            elif controller.state == State.LOAD_NEXT_TARGET:
                print(State.LOAD_NEXT_TARGET)

                if targetIndex < len(targetList):
                    targetIndex += 1
                else:
                    targetIndex = 0

                controller.state = State.CHECK_OBSTACLES

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
                    controller.state = State.CHECK_OBSTACLES

            # ------------------------------------------------------------------------------------------------------- #
            # CHECK OBSTACLES STATE

            elif controller.state == State.CHECK_OBSTACLES:
                print(State.CHECK_OBSTACLES)
                if controller.getClosesObstacleOnPath():
                    controller.robotDie()

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
