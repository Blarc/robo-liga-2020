#!/usr/bin/env python3

"""
Program za vodenje robota EV3
[Robo liga FRI 2019: Sadovnjak]
@Copyright: TrijeMaliKlinci
"""
import sys
from time import time

from ev3dev.ev3 import Button

from .Classes.Connection import Connection
from .Classes.Constants import *
from .Classes.Controller import Controller
from .Classes.GameData import GameData
from .Classes.HiveTypeEnum import HiveTypeEnum
from .Classes.State import State
from .Classes.Team import Team

# ------------------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------------------
# Nastavitev najpomembnjĹˇih parametrov
# ID robota. Spremenite, da ustreza Ĺˇtevilki oznaÄŤbe, ki je doloÄŤena vaĹˇi ekipi.


# -----------------------------------------------------------------------------
# NASTAVITVE TIPAL, MOTORJEV IN POVEZAVE S STREŽNIKOM
# -----------------------------------------------------------------------------
# Nastavimo tipala in gumbe.


print('Priprava tipal ... ', end='', flush=True)
btn = Button()
print('OK!')

# Nastavimo povezavo s strežnikom.
url = SERVER_IP + GAME_ID
print('Vspostavljanje povezave z naslovom ' + url + ' ... ', end='', flush=True)
conn = Connection(url)
print('OK!')

# Izmerimo zakasnitev pri pridobivanju podatkov (povprečje num_iters meritev)
print('Zakasnitev v komunikaciji s streznikom ... ', end='', flush=True)
print('%.4f s' % (conn.test_delay(num_iters=10)))

# -----------------------------------------------------------------------------
# PRIPRAVA NA TEKMO
# -----------------------------------------------------------------------------
# Pridobimo podatke o tekmi.
game_state = conn.request()
# Ali naš robot sploh tekmuje? Če tekmuje, ali je team1 ali team2?
homeTeamTag = 'undefined'
enemyTeamTag = 'undefined'

team1 = Team(game_state["teams"]["team1"])
team2 = Team(game_state["teams"]["team2"])

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

# -----------------------------------------------------------------------------
# GLOBALNE SPREMENLJIVKE
# -----------------------------------------------------------------------------
gameData = GameData(game_state, homeTeamTag, enemyTeamTag)
controller = Controller(gameData)
# -----------------------------------------------------------------------------
# GLAVNA ZANKA
# -----------------------------------------------------------------------------
print('Izvajam glavno zanko. Prekini jo s pritiskom na tipko DOL.')
print('Cakam na zacetek tekme ...')

do_main_loop = True
while do_main_loop and not btn.down:

    time_now = time()
    loop_time = time_now - t_old
    t_old = time_now  # todo odstrani ali dodaj

    # Osveži stanje tekme.
    game_state = conn.request()
    if game_state == -1:
        print('Napaka v paketu, ponovni poskus ...')
    else:
        gameData = GameData(game_state, homeTeamTag, enemyTeamTag)
        controller.update(gameData)

        # todo robotAlive = (robotPos is not None) and (robotDir is not None)
        # todo dodej v controler

        # Če tekma poteka in je oznaka robota vidna na kameri,
        # potem izračunamo novo hitrost na motorjih.
        # Sicer motorje ustavimo.

        # and robotAlive:
        if gameData.gameOn:

            # GET HEALTHY HIVE STATE
            # -----------------------------------------------------------
            if controller.state == State.GET_APPLE:

                currentHive = controller.getClosestHive(HiveTypeEnum.HIVE_HEALTHY)

                if currentHive is None:
                    controller.state = State.GET_BAD_APPLE
                    continue

                controller.setTarget(currentHive)

                if not controller.atTarget():
                    controller.state = State.GET_TURN
                    robot_near_target_old = False
                else:
                    controller.state = State.HOME

            # GET DISEASED HIVE STATE
            # -----------------------------------------------------------
            elif controller.state == State.GET_BAD_APPLE:

                currentHive = controller.getClosestHive(HiveTypeEnum.HIVE_DISEASED)
                if currentHive is None:
                    # TODO tole ni uredu
                    controller.chassis.robotDie()
                else:
                    controller.setTarget(currentHive)

                if not controller.atTarget():
                    controller.state = State.GET_TURN
                    robot_near_target_old = False
                else:
                    controller.state = State.ENEMY_HOME

            # HOME STATE
            # -----------------------------------------------------------
            elif controller.state == State.HOME:

                target = gameData.homeBasket.topLeft
                target.x += 270
                target.y -= 515

                controller.setTarget(target)

                if not controller.atTarget():
                    controller.state = State.HOME_TURN
                    robot_near_target_old = False
                else:
                    controller.state = State.GET_APPLE

            # ENEMY HOME STATE
            # -----------------------------------------------------------
            elif controller.state == State.ENEMY_HOME:
                # Nastavi target na home
                print("State ENEMY_HOME")

                target = gameData.enemyBasket.topLeft
                target.x += 270
                target.y -= 515

                controller.setTarget(target)

                if not controller.atTarget():
                    controller.state = State.ENEMY_HOME_TURN
                    robot_near_target_old = False
                else:
                    controller.state = State.GET_APPLE

            # TURN STATE
            # -----------------------------------------------------------
            elif controller.state == State.GET_TURN:
                # Obračanje robota na mestu, da bo obrnjen proti cilju.

                if controller.stateChanged:
                    # Če smo ravno prišli v to stanje, najprej ponastavimo PID.
                    controller.pidController.PID_turn.reset()

                if controller.isTurned():
                    controller.state = State.GET_STRAIGHT

                else:
                    u = controller.pidController\
                        .PID_turn.update(measurement=controller.targetAngle)
                    controller.speed_right = -u
                    controller.speed_left = u

            # STRAIGHT STATE
            # -----------------------------------------------------------
            elif controller.state == State.GET_STRAIGHT:
                # Vožnja robota naravnost proti ciljni točki.
                print("State GET_STRAIGHT")

                # Vmes bi radi tudi zavijali, zato uporabimo dva regulatorja.
                if controller.stateChanged:
                    # Ponastavi regulatorja PID.
                    controller.pidController.PID_frwd_base.reset()
                    controller.pidController.PID_frwd_turn.reset()
                    timer_near_target = TIMER_NEAR_TARGET

                # Ali smo blizu cilja?
                robot_near_target = target_dist < DIST_NEAR
                if not robot_near_target_old and robot_near_target:
                    # Vstopili smo v bližino cilja.
                    # Začnimo odštevati varnostno budilko.
                    timer_near_target = TIMER_NEAR_TARGET
                if robot_near_target:
                    timer_near_target = timer_near_target - loop_time
                robot_near_target_old = robot_near_target

                # Ali smo že na cilju?
                if controller.atTargetHist():
                    state = State.HOME

                elif timer_near_target < 0:
                    # Smo morda blizu cilja, in je varnostna budilka potekla?
                    controller.setSpeedToZero()
                    state = State.GET_TURN

                else:
                    #  TODO multiplier v bližini cilja zmanjša PID, ker se tudi hitrost zmanjša
                    controller.updatePidStraight()

            # SPIN MOTORS
            # -----------------------------------------------------------
            controller.runMotors()

        else:
            # BREAK MOTORS
            # -----------------------------------------------------------
            # Robot bodisi ni viden na kameri bodisi tema ne teče.
            controller.breakMotors()

# Konec programa
controller.chassis.robotDie()
