import sys

from ev3dev.ev3 import TouchSensor, LargeMotor, MediumMotor, Sound
from Constants import MOTOR_LEFT_PORT, MOTOR_RIGHT_PORT


class Chassis:

    def __init__(self):
        self.motorLeft = self.initLargeMotor(MOTOR_LEFT_PORT)
        self.motorRight = self.initLargeMotor(MOTOR_RIGHT_PORT)

    def initLargeMotor(self, port: str) -> LargeMotor:
        """
        Preveri, ali je motor priklopljen na izhod `port`.
        Vrne objekt za motor (LargeMotor).
        """
        motor = LargeMotor(port)
        while not motor.connected:
            print('\nPriklopi motor na izhod ' + port +
                  ' in pritisni + spusti gumb DOL.')
            self.waitForButton('down')
            motor = LargeMotor(port)
        return motor

    def initMediumMotor(self, port: str) -> MediumMotor:
        """
        Preveri, ali je motor priklopljen na izhod `port`.
        Vrne objekt za motor (LargeMotor).
        """
        motor = MediumMotor(port)
        while not motor.connected:
            print('\nPriklopi motor na izhod ' + port +
                  ' in pritisni + spusti gumb DOL.')
            self.waitForButton('down')
            motor = MediumMotor(port)
        return motor

    def initSensorTouch(self) -> TouchSensor:
        """
        Preveri, ali je tipalo za dotik priklopljeno na katerikoli vhod.
        Vrne objekt za tipalo.
        """
        sensor = TouchSensor()
        while not sensor.connected:
            print('\nPriklopi tipalo za dotik in pritisni + spusti gumb DOL.')
            self.waitForButton('down')
            sensor = TouchSensor()
        return sensor

    @staticmethod
    def waitForButton(button, buttonName: str = 'down'):
        """
        Čakaj v zanki dokler ni gumb z imenom `btn_name` pritisnjen in nato sproščen.
        """
        while not getattr(button, buttonName):
            pass
        flag = False
        while getattr(button, buttonName):
            if not flag:
                flag = True

    def runMotors(self, speedRight, speedLeft):
        self.motorRight.run_forever(speed_sp=speedRight)
        self.motorLeft.run_forever(speed_sp=speedLeft)

    def breakMotors(self):
        self.motorRight.stop(stop_action='brake')
        self.motorLeft.stop(stop_action='brake')

    def beep(self, duration=1000, freq=440):
        """
        Potrobi s frekvenco `freq` za čas `duration`. Klic ne blokira.
        """
        Sound.tone(freq, duration)
        # Če želimo, da blokira, dokler se pisk ne konča.
        # Sound.tone(freq, duration).wait()

    def robotDie(self):
        """
        Končaj s programom na robotu. Ustavi motorje.
        """
        print('KONEC')
        self.motorLeft.stop(stop_action='brake')
        self.motorRight.stop(stop_action='brake')
        Sound.play_song((
            ('D4', 'e'),
            ('C4', 'e'),
            ('A3', 'h')))
        sys.exit(0)
