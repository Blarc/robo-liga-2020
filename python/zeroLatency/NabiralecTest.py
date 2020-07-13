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
from Constants import SERVER_IP, GAME_ID, ROBOT_ID, TIMER_NEAR_TARGET
from Controller import Controller
from Entities import Team, GameData, HiveTypeEnum, State, Point

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

targetsList = [
    Point(gameState['fields']['baskets']['team1']['bottomRight']),
    Point(gameState['fields']['baskets']['team1']['topRight']),
    Point(gameState['fields']['baskets']['team2']['topLeft']),
    Point(gameState['fields']['baskets']['team2']['bottomLeft'])
]

print('Seznam ciljnih tock:')
for tmpTarget in targetsList:
    print('\t' + str(tmpTarget))

# ------------------------------------------------------------------------------------------------------------------- #
# GLOBAL VARIABLES

gameData = GameData(gameState, homeTeamTag, enemyTeamTag)
controller = Controller(gameData, initialState=State.GET_HEALTHY_HIVE)

robotNearTargetOld = False

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

    # Osveži stanje tekme.
    gameState = conn.request()
    if gameState == -1:
        print('Napaka v paketu, ponovni poskus ...')
    else:
        gameData = GameData(gameState, homeTeamTag, enemyTeamTag)
        controller.update(gameData, targetsList[targetIndex])

        # Če tekma poteka in je oznaka robota vidna na kameri,
        # potem izračunamo novo hitrost na motorjih.
        # Sicer motorje ustavimo.

        # and robotAlive:
        if gameData.gameOn and controller.isRobotAlive():

            # ------------------------------------------------------------------------------------------------------- #
            # IDLE STATE

            if controller.state == State.IDLE:

                controller.setSpeedToZero()

                if not controller.atTargetEPS():
                    controller.state = State.TURN
                    robotNearTargetOld = False
                else:
                    controller.state = State.LOAD_NEXT_TARGET

            # ------------------------------------------------------------------------------------------------------- #
            # LOAD NEXT TARGET STATE

            if controller.state == State.LOAD_NEXT_TARGET:

                targetIndex += 1

                if targetIndex >= len(targetsList):
                    targetIndex = 0

                state = State.IDLE

            # ------------------------------------------------------------------------------------------------------- #
            # TURN STATE

            elif controller.state == State.TURN:

                if controller.stateChanged:
                    controller.resetPIDTurn()

                if controller.isTurned():
                    controller.setSpeedToZero()
                    controller.state = State.DRIVE_STRAIGHT
                else:
                    controller.updatePIDTurn()

            # ------------------------------------------------------------------------------------------------------- #
            # DRIVE STRAIGHT STATE

            elif controller.state == State.DRIVE_STRAIGHT:

                controller.resetPIDStraight()
                timerNearTarget = TIMER_NEAR_TARGET

                if not robotNearTargetOld and controller.atTargetNEAR():
                    timerNearTarget = TIMER_NEAR_TARGET

                if controller.atTargetNEAR():
                    timerNearTarget = timerNearTarget - loopTime

                robotNearTargetOld = controller.atTargetNEAR()

                if controller.atTargetHIST():
                    controller.setSpeedToZero()
                    state = State.LOAD_NEXT_TARGET

                elif timerNearTarget < 0:
                    controller.setSpeedToZero()
                    state = State.TURN

                else:
                    controller.updatePIDStraight()

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


