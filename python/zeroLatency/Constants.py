ROBOT_ID = 18
# Naslov IP igralnega streĹľnika.
SERVER_IP = "192.168.2.3:8088/game/"
# Datoteka na igralnem streĹľniku s podatki o tekmi.
GAME_ID = "d198"

# Priklop motorjev na izhode.
MOTOR_LEFT_PORT = 'outA'
MOTOR_RIGHT_PORT = 'outD'

# NajviĹˇja dovoljena hitrost motorjev (teoretiÄŤno je to 1000).
SPEED_MAX = 500
# NajviĹˇja dovoljena nazivna hitrost motorjev pri voĹľnji naravnost.
# Naj bo manjĹˇa kot SPEED_MAX, da ima robot Ĺˇe moĹľnost zavijati.
SPEED_BASE_MAX = 400

# Parametri za PID
# ObraÄŤanje na mestu in zavijanje med voĹľnjo naravnost
PID_TURN_KP = 1.0
PID_TURN_KI = 0.0
PID_TURN_KD = 0.0
PID_TURN_INT_MAX = 100
# Nazivna hitrost pri voĹľnji naravnost.
PID_STRAIGHT_KP = 4.0
PID_STRAIGHT_KI = 0.0
PID_STRAIGHT_KD = 0.0
PID_STRAIGHT_INT_MAX = 100

# DolĹľina FIFO vrste za hranjenje meritev (oddaljenost in kot do cilja).
HIST_QUEUE_LENGTH = 1  # TODO removed?

# Razdalje - tolerance
# Dovoljena napaka v oddaljenosti do cilja [mm].
DIST_EPS = 250
# Dovoljena napaka pri obraÄŤanju [stopinje].
DIR_EPS = 25
# BliĹľina cilja [mm].
DIST_NEAR = 250
# Koliko sekund je robot lahko stanju voĹľnje naravnost v bliĹľini cilja
# (oddaljen manj kot DIST_NEAR), preden sproĹľimo varnostni mehanizem
# in ga damo v stanje obraÄŤanja na mestu.
TIMER_NEAR_TARGET = 3

OBSTACLE_CHECK_WIDTH = 100
OBSTACLE_CHECK_LENGTH = 1500

# Mora biti vsaj večji od "OBSTACLE_CHECK_WIDTH"
OBSTACLE_DODGE_SIZE = 300
