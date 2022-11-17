import ctypes as ct

DRONE_IDENTIFIER               = 101
ACK_DRONE_IDENTIFIER           = 201
ERROR_DRONE_IDENTIFIER         = 501
DRONE_STATUS                   = 102
ACK_DRONE_STATUS               = 202
ERROR_DRONE_STATUS             = 502
DRONE_DISCONNECT               = 103
ACK_DRONE_DISCONNECT           = 203
ERROR_DRONE_DISCONNECT         = 503
DRONE_DEMANDE_ACTION           = 105
ACK_DRONE_DEMANDE_ACTION_NONE  = 2050
ACK_DRONE_DEMANDE_ACTION_START = 2051
ACK_DRONE_DEMANDE_ACTION_POS   = 2052
ACK_DRONE_DEMANDE_ACTION_FIN   = 2053
ERROR_DRONE_DEMANDE_ACTION     = 505
USER_IDENTIFIER                = 111
ACK_USER_IDENTIFIER            = 211
ERROR_USER_IDENTIFIER          = 511
USER_START_DRONE               = 112
ACK_USER_START_DRONE           = 212
ERROR_USER_START_DRONE         = 512
USER_STOP_DRONE                = 113
ACK_USER_STOP_DRONE            = 213
ERROR_USER_STOP_DRONE          = 513
USER_REQ_STATUS                = 114
ACK_USER_REQ_STATUS            = 214
ERROR_USER_REQ_STATUS          = 514


MAXCHAR = 20
TAILLE_IMAGE = 1
MAXDRONES = 2
MAXPOS = 100


def afficherDrone(drone):
    if(drone.isON):
        print(drone.droneID.decode("utf-8")+" - Batterie: "+str(drone.battery)+"% - Pos: ("+str(drone.pos.x)+", "+str(drone.pos.y)+", "+str(drone.pos.z)+") - ON")
    else:
        print(drone.droneID.decode("utf-8")+" - Batterie: "+str(drone.battery)+"% - Pos: ("+str(drone.pos.x)+", "+str(drone.pos.y)+", "+str(drone.pos.z)+") - OFF")

class Tvector3(ct.Structure):
    _fields_ = (
        ("x", ct.c_int),
        ("y", ct.c_int),
        ("z", ct.c_int),
    )

class Tdrone(ct.Structure):
    _fields_ = (
        ("droneID", ct.c_char * MAXCHAR),
        ("isON", ct.c_int),
        ("battery", ct.c_int),
        ("obstacle", ct.c_int),
        ("pos", Tvector3),
        ("vitesse", Tvector3),
        ("Timage", ct.c_ubyte * TAILLE_IMAGE * TAILLE_IMAGE),
    )

class Tens_drone(ct.Structure):
    _fields_ = (
        ("drones", Tdrone * MAXDRONES),
        ("quant", ct.c_int),
    )

class Tmessage(ct.Structure):
    _fields_ = (
        ("codereq", ct.c_int),
        ("drone", Tdrone),
        ("pos", Tvector3),
        ("droneList", Tens_drone),
    )