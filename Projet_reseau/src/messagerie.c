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
  message->drone.presenceImage = 0;
}

void showmess(Tmessage message) {
  printf("\t| %3d | %10s | %2d%% | (%2d, %2d, %2d) | %d |\n", message.codereq, message.drone.droneID, message.drone.battery, message.drone.pos.x, message.drone.pos.y, message.drone.pos.z, message.drone.presenceImage);
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