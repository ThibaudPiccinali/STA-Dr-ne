#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <unistd.h>
#include "../include/messagerie.h"

void initmess(Tmessage* message) {
  message->codereq = 0;
  message->drone.battery = 0;
  strcpy(message->drone.droneID, NOM_DRONE);
  message->drone.pos.x = 0;
  message->drone.pos.y = 0;
  message->drone.pos.z = 0;
}

void showmess(Tmessage message) {
  if (message.codereq == DRONE_IDENTIFIER || message.codereq == DRONE_DEMANDE_ACTION || message.codereq == DRONE_STATUS || message.codereq == DRONE_DEMANDE_ACTION) {
    printf("\t| %3d | %10s | %2d%% | (%2d, %2d, %2d) |\n", message.codereq, message.drone.droneID, message.drone.battery, message.drone.pos.x, message.drone.pos.y, message.drone.pos.z);
  } else {
    printf("\t| %3d |", message.codereq);
    if (message.codereq == USER_REQ_STATUS) {
      for (int i = 0; i < message.droneList.quant; i++) {
        afficherDrone(message.droneList.drones[i]);
        printf(" |");
      }
    }
    printf("\n");
  }
}

Tmessage createMess(int codereq, Tdrone* drone, Tens_drone* droneList, Tvector3* position) {
  Tmessage message;
  message.codereq = codereq;
  if (drone != NULL) {
    message.drone = *drone;
  }
  if (droneList != NULL) {
    message.droneList = *droneList;
  }
  if (position != NULL) {
    message.pos = *position;
  }

  return message;
}

int recvmess(int sockfd, Tmessage* reqMessage, struct sockaddr_in* addr, int* lgadr) {
  int status;
  
  status=read(sockfd,(void *)&reqMessage, sizeof(reqMessage));

  return status==sizeof(reqMessage); //On controle que le nombre d'octets emis est equivalent aux octets du message
}

int sendmess(int sockfd, Tmessage* ackMessage, struct sockaddr_in* addr) {
  int status;
  status= write(sockfd, (void*) ackMessage, sizeof(ackMessage));

  if  (status==sizeof(Tmessage)) //On controle que le nombre d'octets recu est equivalent aux octets du message
    return ackMessage->codereq; //On retourne le codereq du message recu pour le traitement du message
  return -1; //signifie un probleme dans le message recu
}