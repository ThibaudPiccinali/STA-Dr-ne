import ctypes as ct

DRONE_IDENTIFIER                = 101
ACK_DRONE_IDENTIFIER            = 201
ERROR_DRONE_IDENTIFIER          = 501
DRONE_STATUS                    = 102
ACK_DRONE_STATUS                = 202
ERROR_DRONE_STATUS              = 502
DRONE_DISCONNECT                = 103
ACK_DRONE_DISCONNECT            = 203
ERROR_DRONE_DISCONNECT          = 503
DRONE_CHECK_SYSTEM_STATUS       = 104
ACK_DRONE_CHECK_SYSTEM_STATUS   = 204
ERROR_DRONE_CHECK_SYSTEM_STATUS = 504
USER_IDENTIFIER                 = 111
ACK_USER_IDENTIFIER             = 211
ERROR_USER_IDENTIFIER           = 511
USER_START_APPLICATION          = 112
ACK_USER_START_APPLICATION      = 212
ERROR_USER_START_APPLICATION    = 512
USER_STOP_APPLICATION           = 113
ACK_USER_STOP_APPLICATION       = 213
ERROR_USER_STOP_APPLICATION     = 513
USER_REQ_STATUS                 = 114
ACK_USER_REQ_STATUS             = 214
ERROR_USER_REQ_STATUS           = 514
TYPE_DRONE_STATUS  = 0
TYPE_GLOBALSTATUS  = 1
TYPE_ACK           = 2

def afficherDrone(drone):
    print(drone.droneID.decode("utf-8")+" - Batterie: "+str(drone.battery)+"% - Pos: ("+str(drone.pos.x)+", "+str(drone.pos.y)+", "+str(drone.pos.z)+")")


class Tposition(ct.Structure):
    _fields_ = (
        ("x", ct.c_int),
        ("y", ct.c_int),
        ("z", ct.c_int),
    )

class Tdrone(ct.Structure):
    _fields_ = (
        ("droneID", ct.c_char * 20),
        ("pos", Tposition),
        ("secteur", ct.c_int * 4 * 2),
        ("battery", ct.c_int),
        ("presenceImage", ct.c_int),
    )

class Tens_drone(ct.Structure):
    _fields_ = (
        ("drones", Tdrone * 2),
        ("secteurs", ct.c_int * 2),
        ("quant", ct.c_int),
    )

class Tmessage(ct.Structure):
    _fields_ = (
        ("codereq", ct.c_int),
        ("type", ct.c_int),
        ("drone", Tdrone),
        ("droneList", Tens_drone),
    )