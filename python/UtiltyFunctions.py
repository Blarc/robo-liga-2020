import math
import sys

from Classes.Point import Point
from ev3dev.ev3 import TouchSensor, Button, LargeMotor, MediumMotor, Sound


def initLargeMotor(port: str) -> LargeMotor:
    """
    Preveri, ali je motor priklopljen na izhod `port`.
    Vrne objekt za motor (LargeMotor).
    """
    motor = LargeMotor(port)
    while not motor.connected:
        print('\nPriklopi motor na izhod ' + port +
              ' in pritisni + spusti gumb DOL.')
        waitForButton('down')
        motor = LargeMotor(port)
    return motor


def initMediumMotor(port: str) -> MediumMotor:
    """
    Preveri, ali je motor priklopljen na izhod `port`.
    Vrne objekt za motor (LargeMotor).
    """
    motor = MediumMotor(port)
    while not motor.connected:
        print('\nPriklopi motor na izhod ' + port +
              ' in pritisni + spusti gumb DOL.')
        waitForButton('down')
        motor = MediumMotor(port)
    return motor


def initSensorTouch() -> TouchSensor:
    """
    Preveri, ali je tipalo za dotik priklopljeno na katerikoli vhod.
    Vrne objekt za tipalo.
    """
    sensor = TouchSensor()
    while not sensor.connected:
        print('\nPriklopi tipalo za dotik in pritisni + spusti gumb DOL.')
        waitForButton('down')
        sensor = TouchSensor()
    return sensor


def waitForButton(btn, btn_name: str = 'down'):
    """
    Čakaj v zanki dokler ni gumb z imenom `btn_name` pritisnjen in nato sproščen.
    """
    while not getattr(btn, btn_name):
        pass
    flag = False
    while getattr(btn, btn_name):
        if not flag:
            flag = True


def beep(duration=1000, freq=440):
    """
    Potrobi s frekvenco `freq` za čas `duration`. Klic ne blokira.
    """
    Sound.tone(freq, duration)
    # Če želimo, da blokira, dokler se pisk ne konča.
    # Sound.tone(freq, duration).wait()


def robotDie(motor_left, motor_right):
    """
    Končaj s programom na robotu. Ustavi motorje.
    """
    print('KONEC')
    motor_left.stop(stop_action='brake')
    motor_right.stop(stop_action='brake')
    Sound.play_song((
        ('D4', 'e'),
        ('C4', 'e'),
        ('A3', 'h')))
    sys.exit(0)