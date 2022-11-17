#ifndef _MESSAGERIE_
#define _MESSAGERIE_

#include <string.h>
#include "../include/drone.h"

#define NOM_DRONE "DefaultDrone"

#define DRONE_IDENTIFIER                101
#define ACK_DRONE_IDENTIFIER            201
#define ERROR_DRONE_IDENTIFIER          501

#define DRONE_STATUS                    102
#define ACK_DRONE_STATUS                202
#define ERROR_DRONE_STATUS              502

#define DRONE_DISCONNECT                103
#define ACK_DRONE_DISCONNECT            203
#define ERROR_DRONE_DISCONNECT          503

#define DRONE_DEMANDE_ACTION            105
#define ACK_DRONE_DEMANDE_ACTION_NONE   2050
#define ACK_DRONE_DEMANDE_ACTION_START  2051
#define ACK_DRONE_DEMANDE_ACTION_POS    2052
#define ACK_DRONE_DEMANDE_ACTION_FIN    2053
#define ERROR_DRONE_DEMANDE_ACTION      505

#define USER_IDENTIFIER                 111
#define ACK_USER_IDENTIFIER             211
#define ERROR_USER_IDENTIFIER           511

#define USER_START_DRONE                112
#define ACK_USER_START_DRONE            212
#define ERROR_USER_START_DRONE          512

#define USER_STOP_DRONE                 113
#define ACK_USER_STOP_DRONE             213
#define ERROR_USER_STOP_DRONE           513

#define USER_REQ_STATUS                 114
#define ACK_USER_REQ_STATUS             214
#define ERROR_USER_REQ_STATUS           514


typedef struct {
    int codereq;
    Tdrone drone;
    Tvector3 pos;
    Tens_drone droneList;
    //int checksum;
} Tmessage;


void initmess(Tmessage* message);
void showmess(Tmessage message);
Tmessage createMess(int codereq, Tdrone* drone, Tens_drone* droneList, Tvector3* position);
int checksum(Tmessage message);

#endif