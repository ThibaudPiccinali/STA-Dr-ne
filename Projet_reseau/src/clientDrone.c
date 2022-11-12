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

    int systemON = 0;

    Tmessage req, ack;
    initmess(&req);
    initmess(&ack);

    Tdrone drone;
    strcpy(drone.droneID, argv[1]);
    drone.battery = atoi(argv[2]);
    drone.pos.x = atoi(argv[3]);
    drone.pos.y = atoi(argv[4]);
    drone.pos.z = atoi(argv[5]);

    socket_fd = socket(AF_INET, SOCK_STREAM, 0);

    memset(&server_address, 0, sizeof server_address);
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(PORT);
    inet_pton(AF_INET, SERVER_IP, &server_address.sin_addr);

    connect(socket_fd, (struct sockaddr *)&server_address, sizeof server_address);
    
    // -------------------IDENTIFY---------------------//
    printf("Drone identification request\n");
    strcpy(req.drone.droneID, drone.droneID);
    req.codereq = DRONE_IDENTIFIER;
    req.type = TYPE_DRONE_STATUS;
    
    //showmess(req);
    write(socket_fd, (void*)&req, sizeof(Tmessage));
    recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
    if (ack.codereq = ACK_DRONE_IDENTIFIER) {
        printf("Drone identified\n\n");
    } else if (ack.codereq = ERROR_DRONE_IDENTIFIER) {
        printf("Error to identify drone\n\n");
    }
    //showmess(ack);
    // -------------------END-IDENTIFY---------------------//
    //---------------------CHECK-SYSTEM---------------------//
    req.codereq = DRONE_CHECK_SYSTEM_STATUS;
    req.type = TYPE_ACK;

    printf("System is OFF\n");    
    while (!systemON)    {
        //showmess(req);
        write(socket_fd, (void*)&req, sizeof(Tmessage));
        recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
        //showmess(ack);

        if (ack.codereq == 1041) {
            printf("System is ON\n\n");
            systemON = 1;
        }
        sleep(1);
    }
    //------------------END-CHECK-SYSTEM-------------------//
    // -------------------DRONE-STATUS--------------------//
    req.codereq = DRONE_STATUS;
    req.type = TYPE_DRONE_STATUS;
    
    for (; drone.battery > 0; drone.battery -= rand()%10) {
        drone.pos.x += rand() % 19 + (-9);
        drone.pos.y += rand() % 19 + (-9);
        drone.pos.z += rand() % 19 + (-9);
        req.drone = drone;

        printf("Sending drone status\n");
        afficherDrone(drone);
        //showmess(req);
        write(socket_fd, (void*)&req, sizeof(Tmessage));
        recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
        //showmess(ack);
        if (ack.codereq = ACK_DRONE_STATUS) {
            printf("Drone status sent\n\n");
        } else if (ack.codereq = ERROR_DRONE_IDENTIFIER) {
            printf("Error to send drone status\n\n");
        }

        sleep(5);
    }       
    // -------------------END-STATUS---------------------//
    // -------------------DRONE-DISCONNECT---------------//
    printf("Drone disconnect request\n");

    req.codereq = DRONE_DISCONNECT;
    req.type = TYPE_ACK;
    
    //showmess(req);
    write(socket_fd, (void*)&req, sizeof(Tmessage));
    recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
    //showmess(ack);
    if (ack.codereq = ACK_DRONE_DISCONNECT) {
        printf("Drone disconnected\n\n");
    } else if (ack.codereq = ERROR_DRONE_DISCONNECT) {
        printf("Error to disconnect drone\n\n");
    }
    req.codereq = 555;
    req.type = TYPE_ACK;
    //showmess(req);

    write(socket_fd, (void*)&req, sizeof(Tmessage));
    // -------------------END-DISCONNECT---------------//

    close(socket_fd);
    return 0;
}