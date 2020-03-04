from Classes.PID import PID

ROBOT_ID = 18
# Naslov IP igralnega streĹľnika.
SERVER_IP = "192.168.1.130:8088/game/"
# Datoteka na igralnem streĹľniku s podatki o tekmi.
GAME_ID = "3b08"

# Priklop motorjev na izhode.
MOTOR_LEFT_PORT = 'outA'
MOTOR_RIGHT_PORT = 'outD'

# NajviĹˇja dovoljena hitrost motorjev (teoretiÄŤno je to 1000).
SPEED_MAX = 800
# NajviĹˇja dovoljena nazivna hitrost motorjev pri voĹľnji naravnost.
# Naj bo manjĹˇa kot SPEED_MAX, da ima robot Ĺˇe moĹľnost zavijati.
SPEED_BASE_MAX = 600

# Parametri za PID
# ObraÄŤanje na mestu in zavijanje med voĹľnjo naravnost
PID_TURN_KP = 1.0
PID_TURN_KI = 0.0
PID_TURN_KD = 0.0
PID_TURN_INT_MAX = 100
# Nazivna hitrost pri voĹľnji naravnost.
PID_STRAIGHT_KP = 1.0
PID_STRAIGHT_KI = 0.0
PID_STRAIGHT_KD = 0.0
PID_STRAIGHT_INT_MAX = 100

# DolĹľina FIFO vrste za hranjenje meritev (oddaljenost in kot do cilja).
HIST_QUEUE_LENGTH = 3

# Razdalje - tolerance
# Dovoljena napaka v oddaljenosti do cilja [mm].
DIST_EPS = 50
# Dovoljena napaka pri obraÄŤanju [stopinje].
DIR_EPS = 30
# BliĹľina cilja [mm].
DIST_NEAR = 500
# Koliko sekund je robot lahko stanju voĹľnje naravnost v bliĹľini cilja
# (oddaljen manj kot DIST_NEAR), preden sproĹľimo varnostni mehanizem
# in ga damo v stanje obraÄŤanja na mestu.
TIMER_NEAR_TARGET = 3


# Regulator PID za obracanje na mestu.
# setpoint=0 pomeni, da naj bo kot med robotom in ciljem (target_angle) enak 0.
# Nasa regulirana velicina je torej kar napaka kota, ki mora biti 0.
# To velja tudi za regulacijo voznje naravnost.
PID_turn = PID(
    setpoint=0,
    kp=PID_TURN_KP,
    ki=PID_TURN_KI,
    kd=PID_TURN_KD,
    integral_limit=PID_TURN_INT_MAX)

# PID za voznjo naravnost - regulira nazivno hitrost za oba motorja,
# ki je odvisna od oddaljenosti od cilja.
# setpoint=0 pomeni, da mora biti razdalja med robotom in ciljem enaka 0.
PID_frwd_base = PID(
    setpoint=0,
    kp=PID_STRAIGHT_KP,
    ki=PID_STRAIGHT_KI,
    kd=PID_STRAIGHT_KD,
    integral_limit=PID_STRAIGHT_INT_MAX)

# PID za obracanje med voznjo naravnost.
# setpoint=0 pomeni, da naj bo kot med robotom in ciljem (target_angle) enak 0.
PID_frwd_turn = PID(
    setpoint=0,
    kp=PID_TURN_KP,
    ki=PID_TURN_KI,
    kd=PID_TURN_KD,
    integral_limit=PID_TURN_INT_MAX)