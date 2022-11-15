#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include "../include/drone.h"
#include "../include/messagerie.h"

#define SERVER_IP "127.0.0.1"
#define PORT 3000

int main(int argc, char** argv) {
    int socket_fd;
    struct sockaddr_in server_address;

    int action = 0;

    Tmessage req, ack;
    initmess(&req);
    initmess(&ack);

    Tdrone drone;
    strcpy(drone.droneID, argv[1]);
    drone.battery = rand() % 100;
    drone.pos.x = rand() % 100;
    drone.pos.y = rand() % 100;
    drone.pos.z = rand() % 100;
    drone.isON = 0;

    socket_fd = socket(AF_INET, SOCK_STREAM, 0);

    memset(&server_address, 0, sizeof server_address);
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(PORT);
    inet_pton(AF_INET, SERVER_IP, &server_address.sin_addr);

    connect(socket_fd, (struct sockaddr *)&server_address, sizeof server_address);
    
// -------------------IDENTIFY---------------------//
    printf("Drone identification request\n");
    strcpy(req.drone.droneID, drone.droneID);
    
    req = createMess(DRONE_IDENTIFIER, &drone, NULL, NULL);
    
    write(socket_fd, (void*)&req, sizeof(Tmessage));
    
    recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
    if (ack.codereq = ACK_DRONE_IDENTIFIER) {
        printf("Drone identified\n\n");
    } else if (ack.codereq = ERROR_DRONE_IDENTIFIER) {
        printf("Error to identify drone\n\n");
    }
// -------------------END-IDENTIFY---------------------//
    while(ack.codereq != ACK_DRONE_DISCONNECT) {
// -------------------DRONE-STATUS--------------------//
        req = createMess(DRONE_STATUS, &drone, NULL, NULL);
        printf("Sending drone status\n");
        afficherDrone(drone);

        write(socket_fd, (void*)&req, sizeof(Tmessage));
        recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
        
        if (ack.codereq = ACK_DRONE_STATUS) {
            printf("Drone status sent\n\n");
        } else if (ack.codereq = ERROR_DRONE_IDENTIFIER) {
            printf("Error to send drone status\n\n");
        }
// -------------------END-STATUS---------------------//
        req =  createMess(DRONE_DEMANDE_ACTION, &drone, NULL, NULL);
        printf("Waiting for action...\n");

        write(socket_fd, (void*)&req, sizeof(Tmessage));
        recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
        
        if (ack.codereq == ACK_DRONE_DEMANDE_ACTION_NONE) {
            printf("Drone ne fait rien\n\n");
        } else if (ack.codereq == ACK_DRONE_DEMANDE_ACTION_START) {
            printf("Drone demarre\n\n");
            drone.isON = 1;
        } else if (ack.codereq == ACK_DRONE_DEMANDE_ACTION_POS) {
            printf("Drone va à la position (%d, %d, %d)\n\n", ack.pos.x, ack.pos.y, ack.pos.z);
            drone.pos = ack.pos;
        } else if (ack.codereq == ACK_DRONE_DEMANDE_ACTION_FIN) {
            printf("Drone arrete\n\n");
            drone.isON = 0;
        }
        sleep(1);
    }    

// -------------------DRONE-DISCONNECT---------------//
    printf("Drone disconnect request\n");

    req = createMess(DRONE_DISCONNECT, &drone, NULL, NULL);

    write(socket_fd, (void*)&req, sizeof(Tmessage));
    recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);

    if (ack.codereq = ACK_DRONE_DISCONNECT) {
        printf("Drone disconnected\n\n");
    } else if (ack.codereq = ERROR_DRONE_DISCONNECT) {
        printf("Error to disconnect drone\n\n");
    }

    req = createMess(555, &drone, NULL, NULL);
    
    write(socket_fd, (void*)&req, sizeof(Tmessage));
// -------------------END-DISCONNECT---------------//

    close(socket_fd);
    return 0;
}