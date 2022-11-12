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

#define DRONE_CHECK_SYSTEM_STATUS       104
#define ACK_DRONE_CHECK_SYSTEM_STATUS   204
#define ERROR_DRONE_CHECK_SYSTEM_STATUS 504

#define USER_IDENTIFIER                 111
#define ACK_USER_IDENTIFIER             211
#define ERROR_USER_IDENTIFIER           511

#define USER_START_APPLICATION          112
#define ACK_USER_START_APPLICATION      212
#define ERROR_USER_START_APPLICATION    512

#define USER_STOP_APPLICATION           113
#define ACK_USER_STOP_APPLICATION       213
#define ERROR_USER_STOP_APPLICATION     513

#define USER_REQ_STATUS                 114
#define ACK_USER_REQ_STATUS             214
#define ERROR_USER_REQ_STATUS           514

#define TYPE_DRONE_STATUS   0
#define TYPE_GLOBALSTATUS   1
#define TYPE_ACK            2

typedef struct {
    int codereq;
    int type;
    Tdrone drone;
    Tens_drone droneList;
} Tmessage;


void initmess(Tmessage* message);
void showmess(Tmessage message);
int recvmess(int sockfd, Tmessage* reqMessage, struct sockaddr_in* addr, int* lgadr);
int sendmess(int sockfd, Tmessage* ackMessage, struct sockaddr_in* addr);

#endif