/*
TODO:   proteger le code en utilisant la programation defensive: traiter
        les arguments de ligne de commande et utiliser check_error() 
        pour verifier les échecs des fonctions

TODO: implementer le checksum
*/

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
    //printf("\t| %3d | %10s | %2d%% | (%2d, %2d, %2d) | %d |\n", message.codereq, message.drone.droneID, message.drone.battery, message.drone.pos.x, message.drone.pos.y, message.drone.pos.z, message.checksum);
    printf("\t| %3d | %10s | %2d%% | (%2d, %2d, %2d) |\n", message.codereq, message.drone.droneID, message.drone.battery, message.drone.pos.x, message.drone.pos.y, message.drone.pos.z);
  } else {
    printf("\t| %3d |", message.codereq);
    if (message.codereq == USER_REQ_STATUS) {
      for (int i = 0; i < message.droneList.quant; i++) {
        afficherDrone(message.droneList.drones[i]);
        printf(" |");
      }
    }
    //printf("| %d |\n", message.checksum);
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
  //message.checksum = checksum(message);
  //printf("checksum calcule: %d\n", message.checksum);
  //printf("message size: %ld\n", sizeof(Tmessage));

  return message;
}

int checksum(Tmessage message) {
  int sum = 0;
  int i, j;

  sum += message.codereq;
  sum += message.drone.battery;
  for (i=0; i < MAXCHAR; i++) {
    sum += message.drone.droneID[i];
  }
  sum += message.drone.isON;
  sum += message.drone.obstacle;
  sum += message.drone.pos.x;
  sum += message.drone.pos.y;
  sum += message.drone.pos.z;
  sum += message.drone.vitesse.x;
  sum += message.drone.vitesse.y;
  sum += message.drone.vitesse.z;
  for (i = 0; i < TAILLE_IMAGE; i++) {
    for (j = 0; j < TAILLE_IMAGE; j++) {
      sum += message.drone.image[i][j];
    }
  }

  return sum;
}