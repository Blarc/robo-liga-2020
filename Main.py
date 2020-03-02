#!/usr/bin/env python3

"""
Program za vodenje robota EV3
[Robo liga FRI 2019: Sadovnjak]
@Copyright: TrijeMaliKlinci
"""

from ev3dev.ev3 import TouchSensor, Button, LargeMotor, MediumMotor, Sound
import math
from time import time, sleep
from collections import deque
from io import BytesIO
import pycurl
import ujson
from enum import Enum
import sys

from Classes.GameData import GameData
from Classes.PID import PID
from Classes.State import State
from Classes.Team import Team
from UtiltyFunctions import init_large_motor, robot_die

# ------------------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------------------
# Nastavitev najpomembnjĹˇih parametrov
# ID robota. Spremenite, da ustreza Ĺˇtevilki oznaÄŤbe, ki je doloÄŤena vaĹˇi ekipi.
from nabiralec import Connection




# -----------------------------------------------------------------------------
# NASTAVITVE TIPAL, MOTORJEV IN POVEZAVE S STREŽNIKOM
# -----------------------------------------------------------------------------
# Nastavimo tipala in gumbe.
print('Priprava tipal ... ', end='', flush=True)
btn = Button()
# sensor_touch = init_sensor_touch()
print('OK!')

# Nastavimo velika motorja. Priklopljena naj bosta na izhoda A in D.
print('Priprava motorjev ... ', end='')
motor_left = init_large_motor(MOTOR_LEFT_PORT)
motor_right = init_large_motor(MOTOR_RIGHT_PORT)
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
    robot_die(motor_left, motor_right)
print('Robot tekmuje in ima interno oznako "' + homeTeamTag + '"')

# -----------------------------------------------------------------------------
# PIDi
# -----------------------------------------------------------------------------

# Regulator PID za obraÄŤanje na mestu.
# setpoint=0 pomeni, da naj bo kot med robotom in ciljem (target_angle) enak 0.
# NaĹˇa regulirana veliÄŤina je torej kar napaka kota, ki mora biti 0.
# To velja tudi za regulacijo voĹľnje naravnost.
PID_turn = PID(
    setpoint=0,
    kp=PID_TURN_KP,
    ki=PID_TURN_KI,
    kd=PID_TURN_KD,
    integral_limit=PID_TURN_INT_MAX)

# PID za voĹľnjo naravnost - regulira nazivno hitrost za oba motorja,
# ki je odvisna od oddaljenosti od cilja.
# setpoint=0 pomeni, da mora biti razdalja med robotom in ciljem enaka 0.
PID_frwd_base = PID(
    setpoint=0,
    kp=PID_STRAIGHT_KP,
    ki=PID_STRAIGHT_KI,
    kd=PID_STRAIGHT_KD,
    integral_limit=PID_STRAIGHT_INT_MAX)

# PID za obraÄŤanje med voĹľnjo naravnost.
# setpoint=0 pomeni, da naj bo kot med robotom in ciljem (target_angle) enak 0.
PID_frwd_turn = PID(
    setpoint=0,
    kp=PID_TURN_KP,
    ki=PID_TURN_KI,
    kd=PID_TURN_KD,
    integral_limit=PID_TURN_INT_MAX)

# -----------------------------------------------------------------------------
# GLOBALNE SPREMENLJIVKE
# -----------------------------------------------------------------------------
gameData = GameData(game_state, homeTeamTag, enemyTeamTag)
# Hitrost na obeh motorjih.
speed_right = 0
speed_left = 0
# Stara hitrost
speed_right_old = 0
speed_left_old = 0
# Zgodovina (okno) zadnjih nekaj vrednosti meritev,
# implementirana kot vrsta FIFO.
robot_dir_hist = deque([180.0] * HIST_QUEUE_LENGTH)
robot_dist_hist = deque([math.inf] * HIST_QUEUE_LENGTH)
# Meritve direction
robot_dir_data_id = 0
# Merimo čas obhoda zanke. Za visoko odzivnost robota je zelo pomembno,
# da je ta čas čim krajši.
t_old = time()
# Začetno stanje.
state = State.GET_APPLE
# Prejšnje stanje.
stateOld = -1
# Id prejšnjega najbližjega jabolka
picked_up_apples_id = []
# Trenutno jabolko
current_apple = None
# Trenutni target
target = None
# Razdalja med robotom in ciljem.
target_dist = 0
# Kot med robotom in ciljem.
target_angle = 0
# Datoteke za zapis podatkov za graf
file = open('pid_data' + str(robot_dir_data_id) + '.txt', 'w')
# Če se zatakne timer
timeTimeout = 0
# Pospešek
get_straight_accel_factor = 0.05

# -----------------------------------------------------------------------------
# GLAVNA ZANKA
# -----------------------------------------------------------------------------
print('Izvajam glavno zanko. Prekini jo s pritiskon na tipko DOL.')
print('Cakam na zacetek tekme ...')

do_main_loop = True
while do_main_loop and not btn.down:

    time_now = time()
    loop_time = time_now - t_old
    t_old = time_now

    # Osveži stanje tekme.
    game_state = conn.request()
    if game_state == -1:
        print('Napaka v paketu, ponovni poskus ...')
    else:
        gameData = GameData(game_state)

        # Pridobi pozicijo in orientacijo svojega robota;
        # najprej pa ga poišči v tabeli vseh robotov na poligonu.
        robotPos = gameData.homeRobot.pos
        robotDir = gameData.homeRobot.dir
        # Ali so podatki o robotu veljavni? Če niso, je zelo verjetno,
        # da sistem ne zazna oznake na robotu.
        robotAlive = (robotPos is not None) and (robotDir is not None)

        # Če tekma poteka in je oznaka robota vidna na kameri,
        # potem izračunamo novo hitrost na motorjih.
        # Sicer motorje ustavimo.
        if gameData.gameOn and robotAlive:

            # Zaznaj spremembo stanja.
            if state != stateOld:
                timeTimeout = time()
                stateChanged = True
            else:
                stateChanged = False

            stateOld = state

            # Spremljaj zgodovino meritev kota in oddaljenosti.
            # Odstrani najstarejši element in dodaj novega - princip FIFO.
            robot_dir_hist.popleft()
            robot_dir_hist.append(target_angle)
            robot_dist_hist.popleft()
            robot_dist_hist.append(target_dist)

            if state == State.GET_APPLE:
                # Nastavi target na najbližje jabolko
                print("State GET_APPLE")

                current_apple = get_closest_good_apple()
                if current_apple is None:
                    state = State.GET_BAD_APPLE
                    continue

                target = get_apple_pos(current_apple)
                print(str(target.x) + " " + str(target.y))

                target_dist = get_distance(robot_pos, target)
                target_angle = get_angle(robot_pos, robot_dir, target)

                speed_right = 0
                speed_left = 0

                # Preverimo, ali je robot na ciljni točki.
                # Če ni, ga tja pošljemo.
                if target_dist > DIST_EPS:
                    state = State.GET_TURN
                    robot_near_target_old = False
                else:
                    state = State.HOME

            elif state == State.GET_BAD_APPLE:
                # Nastavi target na najbližje jabolko
                print("State GET_BAD_APPLE")

                current_apple = get_closest_bad_apple()
                if current_apple is None:
                    robot_die()

                target = get_apple_pos(current_apple)
                print(str(target.x) + " " + str(target.y))

                target_dist = get_distance(robot_pos, target)
                target_angle = get_angle(robot_pos, robot_dir, target)

                speed_right = 0
                speed_left = 0

                # Preverimo, ali je robot na ciljni točki.
                # Če ni, ga tja pošljemo.
                if target_dist > DIST_EPS:
                    state = State.GET_TURN
                    robot_near_target_old = False
                else:
                    state = State.ENEMY_HOME

            elif state == State.HOME:
                # Nastavi target na home
                print("State HOME")

                target = home
                print("Target coords: " + str(target.x) + " " + str(target.y))

                target_dist = get_distance(robot_pos, target)
                target_angle = get_angle(robot_pos, robot_dir, target)

                speed_right = 0
                speed_left = 0

                # Preverimo, ali je robot na ciljni točki.
                # Če ni, ga tja pošljemo.
                if target_dist > DIST_EPS:
                    state = State.HOME_TURN
                    robot_near_target_old = False
                else:
                    state = State.GET_APPLE

            elif state == State.ENEMY_HOME:
                # Nastavi target na home
                print("State ENEMY_HOME")

                target = enemy_home
                print("Target coords: " + str(target.x) + " " + str(target.y))

                target_dist = get_distance(robot_pos, target)
                target_angle = get_angle(robot_pos, robot_dir, target)

                speed_right = 0
                speed_left = 0

                # Preverimo, ali je robot na ciljni točki.
                # Če ni, ga tja pošljemo.
                if target_dist > DIST_EPS:
                    state = State.ENEMY_HOME_TURN
                    robot_near_target_old = False
                else:
                    state = State.GET_APPLE

            elif state == State.GET_TURN:
                # Obračanje robota na mestu, da bo obrnjen proti cilju.
                print("State GET_TURN")

                # Pogledamo če smo na poti pobrali kakšno jabolko po nesreči
                # Če smo, gremo v home/enemy home, in ga odpeljemo
                # temp = False
                # for apple_iter in get_apples():
                #     if apple_in_claws(get_apple_id(apple_iter)):
                #         print("Pobrali smo jabolko na poti do tarče")
                #         print(apple_iter)
                #        current_apple = apple_iter
                #         claws_close()
                #        if get_apple_type(apple_iter) == "appleGood":
                #            state = State.HOME
                #        else:
                #            state = State.ENEMY_HOME
                #        temp = True

                # if temp:
                #    continue

                target_dist = get_distance(robot_pos, target)
                target_angle = get_angle(robot_pos, robot_dir, target)

                # beleženje za izris grafa
                # file.write(str(target_angle) + ',' + str(time_now) + '\n')

                if stateChanged:
                    # Če smo ravno prišli v to stanje, najprej ponastavimo PID.
                    PID_turn.reset()

                # Ali smo že dosegli ciljni kot?
                # Zadnjih nekaj obhodov zanke mora biti absolutna vrednost
                # napake kota manjša od DIR_EPS.
                err = [abs(a) > DIR_EPS for a in robot_dir_hist]

                if sum(err) == 0:
                    # Vse vrednosti so znotraj tolerance, zamenjamo stanje.
                    speed_right = 0
                    speed_left = 0
                    # print(apples_on_path(1000, 100))
                    # if apples_on_path(1000, 100).__len__() > 0:
                    #     robot_die()
                    state = State.GET_STRAIGHT

                else:
                    u = PID_turn.update(measurement=target_angle)
                    speed_right = -u
                    speed_left = u

            elif state == State.GET_STRAIGHT:
                # Vožnja robota naravnost proti ciljni točki.
                print("State GET_STRAIGHT")

                # Pogledamo če smo na poti pobrali kakšno jabolko po nesreči
                # Če smo, gremo v home/enemy home, in ga odpeljemo
                temp = False
                for apple_iter in get_apples():
                    if apple_in_claws(get_apple_id(apple_iter)):
                        print("Pobrali smo jabolko na poti do tarče")
                        print(apple_iter)
                        current_apple = apple_iter
                        claws_close()
                        if get_apple_type(apple_iter) == "appleGood":
                            state = State.HOME
                        else:
                            state = State.ENEMY_HOME
                        # temp = True
                        continue

                # if temp:
                #   continue

                target_dist = get_distance(robot_pos, target)
                target_angle = get_angle(robot_pos, robot_dir, target)

                # beleženje za izris grafa
                # file.write(str(target_angle) + ',' + str(time_now) + '\n')

                # Vmes bi radi tudi zavijali, zato uporabimo dva regulatorja.
                if stateChanged:
                    # Ponastavi regulatorja PID.
                    get_straight_accel = 0.05
                    PID_frwd_base.reset()
                    PID_frwd_turn.reset()
                    timer_near_target = TIMER_NEAR_TARGET
                else:
                    if get_straight_accel < 1:
                        get_straight_accel += get_straight_accel_factor

                # Ali smo blizu cilja?
                robot_near_target = target_dist < DIST_NEAR
                if not robot_near_target_old and robot_near_target:
                    # Vstopili smo v bližino cilja.
                    # Začnimo odštevati varnostno budilko.
                    pid_frwd_base_multiplier = 0.5
                    timer_near_target = TIMER_NEAR_TARGET
                if robot_near_target:
                    timer_near_target = timer_near_target - loop_time
                robot_near_target_old = robot_near_target

                # Ali smo že na cilju?
                # Zadnjih nekaj obhodov zanke mora biti razdalja do cilja
                # manjša ali enaka DIST_EPS.
                err_eps = [d > DIST_EPS for d in robot_dist_hist]
                if sum(err_eps) == 0:
                    # Razdalja do cilja je znotraj tolerance, zamenjamo stanje.
                    claws_close()
                    print("Pobrali smo jabolko")
                    state = State.HOME

                elif timer_near_target < 0:
                    # Smo morda blizu cilja, in je varnostna budilka potekla?
                    speed_right = 0
                    speed_left = 0
                    state = State.GET_TURN

                else:
                    # multiplier v bližini cilja zmanjša PID, ker se tudi hitrost zmanjša
                    u_turn = PID_frwd_turn.update(
                        measurement=target_angle) * pid_frwd_base_multiplier * get_straight_accel
                    u_base = PID_frwd_base.update(measurement=target_dist) * get_straight_accel
                    # Omejimo nazivno hitrost, ki je enaka za obe kolesi,
                    # da imamo še manevrski prostor za zavijanje.
                    u_base = min(max(u_base, -SPEED_BASE_MAX), SPEED_BASE_MAX)
                    speed_right = (-u_base - u_turn)
                    speed_left = (-u_base + u_turn)

            elif state == State.HOME_TURN:
                # Obračanje robota na mestu, da bo obrnjen proti cilju.
                print("State HOME_TURN")

                target_dist = get_distance(robot_pos, target)
                target_angle = get_angle(robot_pos, robot_dir, target)

                # beleženje za izris grafa
                file.write(str(target_angle) + ',' + str(time_now) + '\n')

                if stateChanged:
                    # Če smo ravno prišli v to stanje, najprej ponastavimo PID.
                    PID_turn_apple.reset()

                print("robot: " + str(robot_pos.x) + " " + str(robot_pos.y))
                if not apple_in_claws(get_apple_id(current_apple)):
                    state = State.GET_APPLE
                    claws_open()
                    continue
                # Ali smo že dosegli ciljni kot?
                # Zadnjih nekaj obhodov zanke mora biti absolutna vrednost
                # napake kota manjša od DIR_EPS.
                err = [abs(a) > DIR_EPS for a in robot_dir_hist]

                if sum(err) == 0 or at_home(robot_pos):
                    # Vse vrednosti so znotraj tolerance, zamenjamo stanje.
                    speed_right = 0
                    speed_left = 0
                    state = State.HOME_STRAIGHT
                else:
                    u = PID_turn_apple.update(measurement=target_angle)
                    speed_right = -u
                    speed_left = u

            elif state == State.HOME_STRAIGHT:
                # Vožnja robota naravnost proti ciljni točki.
                print("State HOME_STRAIGHT")

                if at_home(robot_pos):
                    print("Smo že doma")
                    claws_open()
                    state = State.BACK_OFF
                    continue

                target_dist = get_distance(robot_pos, target)
                target_angle = get_angle(robot_pos, robot_dir, target)

                # Vmes bi radi tudi zavijali, zato uporabimo dva regulatorja.
                if stateChanged:
                    # Ponastavi regulatorja PID.
                    PID_frwd_base_apple.reset()
                    PID_frwd_turn_apple.reset()
                    timer_near_target = TIMER_NEAR_TARGET
                    pid_frwd_base_apple_multiplier = 1

                # Ali smo blizu cilja?
                robot_near_target = target_dist < DIST_NEAR
                if not robot_near_target_old and robot_near_target:
                    # Vstopili smo v bližino cilja.
                    # Začnimo odštevati varnostno budilko.
                    pid_frwd_base_apple_multiplier = 0.1
                    timer_near_target = TIMER_NEAR_TARGET
                if robot_near_target:
                    timer_near_target = timer_near_target - loop_time
                robot_near_target_old = robot_near_target

                # Ali smo že na cilju?
                # Zadnjih nekaj obhodov zanke mora biti razdalja do cilja
                # manjša ali enaka DIST_EPS.
                err_eps = [d > DIST_EPS for d in robot_dist_hist]
                if sum(err_eps) == 0 or at_home(robot_pos):
                    # Razdalja do cilja je znotraj tolerance, zamenjamo stanje.
                    speed_right = 0
                    speed_left = 0
                    claws_open()
                    print("Prišli smo domov")
                    state = State.BACK_OFF

                elif timer_near_target < 0:
                    # Smo morda blizu cilja, in je varnostna budilka potekla?
                    speed_right = 0
                    speed_left = 0
                    state = State.HOME_TURN

                else:
                    # multiplier v bližini cilja zmanjša PID, ker se tudi hitrost zmanjša
                    u_turn = PID_frwd_turn_apple.update(measurement=target_angle) * pid_frwd_base_apple_multiplier
                    u_base = PID_frwd_base_apple.update(measurement=target_dist)
                    # Omejimo nazivno hitrost, ki je enaka za obe kolesi,
                    # da imamo še manevrski prostor za zavijanje.
                    u_base = min(max(u_base, -SPEED_BASE_MAX), SPEED_BASE_MAX)
                    speed_right = -u_base - u_turn
                    speed_left = -u_base + u_turn

            elif state == State.ENEMY_HOME_TURN:
                # Obračanje robota na mestu, da bo obrnjen proti cilju.
                print("State ENEMY_HOME_TURN")

                target_dist = get_distance(robot_pos, target)
                target_angle = get_angle(robot_pos, robot_dir, target)

                if stateChanged:
                    # Če smo ravno prišli v to stanje, najprej ponastavimo PID.
                    PID_turn_apple.reset()

                print("robot: " + str(robot_pos.x) + " " + str(robot_pos.y))
                if not apple_in_claws(get_apple_id(current_apple)):
                    state = State.GET_APPLE
                    claws_open()
                    continue
                # Ali smo že dosegli ciljni kot?
                # Zadnjih nekaj obhodov zanke mora biti absolutna vrednost
                # napake kota manjša od DIR_EPS.
                err = [abs(a) > DIR_EPS for a in robot_dir_hist]

                if sum(err) == 0 or at_home_enemy(robot_pos):
                    # Vse vrednosti so znotraj tolerance, zamenjamo stanje.
                    speed_right = 0
                    speed_left = 0
                    state = State.ENEMY_HOME_STRAIGHT
                else:
                    u = PID_turn_apple.update(measurement=target_angle)
                    speed_right = -u
                    speed_left = u

            elif state == State.ENEMY_HOME_STRAIGHT:
                # Vožnja robota naravnost proti ciljni točki.
                print("State ENEMY_HOME_STRAIGHT")

                target_dist = get_distance(robot_pos, target)
                target_angle = get_angle(robot_pos, robot_dir, target)

                # Vmes bi radi tudi zavijali, zato uporabimo dva regulatorja.
                if stateChanged:
                    # Ponastavi regulatorja PID.
                    PID_frwd_base_apple.reset()
                    PID_frwd_turn_apple.reset()
                    timer_near_target = TIMER_NEAR_TARGET
                    pid_frwd_base_apple_multiplier = 1

                # Ali smo blizu cilja?
                robot_near_target = target_dist < DIST_NEAR
                if not robot_near_target_old and robot_near_target:
                    # Vstopili smo v bližino cilja.
                    # Začnimo odštevati varnostno budilko.
                    pid_frwd_base_apple_multiplier = 0.1
                    timer_near_target = TIMER_NEAR_TARGET
                if robot_near_target:
                    timer_near_target = timer_near_target - loop_time
                robot_near_target_old = robot_near_target

                # Ali smo že na cilju?
                # Zadnjih nekaj obhodov zanke mora biti razdalja do cilja
                # manjša ali enaka DIST_EPS.
                err_eps = [d > DIST_EPS for d in robot_dist_hist]
                if sum(err_eps) == 0 or at_home_enemy(robot_pos):
                    # Razdalja do cilja je znotraj tolerance, zamenjamo stanje.
                    speed_right = 0
                    speed_left = 0
                    claws_open()
                    print("Prišli smo v nasprotnikov dom")
                    state = State.BACK_OFF

                elif timer_near_target < 0:
                    # Smo morda blizu cilja, in je varnostna budilka potekla?
                    speed_right = 0
                    speed_left = 0
                    state = State.ENEMY_HOME_TURN

                else:
                    # multiplier v bližini cilja zmanjša PID, ker se tudi hitrost zmanjša
                    u_turn = PID_frwd_turn_apple.update(measurement=target_angle) * pid_frwd_base_apple_multiplier
                    u_base = PID_frwd_base_apple.update(measurement=target_dist)
                    # Omejimo nazivno hitrost, ki je enaka za obe kolesi,
                    # da imamo še manevrski prostor za zavijanje.
                    u_base = min(max(u_base, -SPEED_BASE_MAX), SPEED_BASE_MAX)
                    speed_right = -u_base - u_turn
                    speed_left = -u_base + u_turn

            elif state == State.BACK_OFF:
                print("State BACK_OFF")
                decelerate_both_motors_to(0, -500)
                state = State.GET_APPLE

            # Omejimo vrednosti za hitrosti na motorjih.
            speed_right = round(
                min(
                    max(speed_right, -SPEED_MAX),
                    SPEED_MAX)
            )
            speed_left = round(
                min(
                    max(speed_left, -SPEED_MAX),
                    SPEED_MAX)
            )

            # Vrtimo motorje.

            motor_right.run_forever(speed_sp=speed_right)
            motor_left.run_forever(speed_sp=speed_left)
            # accelerate_motors(speed_right_old, speed_right, speed_left_old, speed_left)

            speed_right_old = speed_right
            speed_left_old = speed_left

        else:
            # Robot bodisi ni viden na kameri bodisi tema ne teče.
            motor_left.stop(stop_action='brake')
            motor_right.stop(stop_action='brake')

# Konec programa
robot_die()
