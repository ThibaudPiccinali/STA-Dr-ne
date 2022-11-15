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

    Tmessage req, ack;
    initmess(&req);
    initmess(&ack);

    socket_fd = socket(AF_INET, SOCK_STREAM, 0);

    memset(&server_address, 0, sizeof server_address);
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(PORT);
    inet_pton(AF_INET, SERVER_IP, &server_address.sin_addr);

    connect(socket_fd, (struct sockaddr *)&server_address, sizeof server_address);
    
    int opt = -1;
    while(opt != 0) {
        printf("Codigo: ");
        scanf("%d", &opt);

        if (opt == DRONE_IDENTIFIER) {
            strcpy(req.drone.droneID, argv[1]);
            req.codereq = DRONE_IDENTIFIER;
            req.type = TYPE_DRONE_STATUS;
            
            showmess(req);
            write(socket_fd, (void*)&req, sizeof(Tmessage));
            recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
            showmess(ack);
        }
        if (opt == DRONE_STATUS) {
            req.codereq = DRONE_STATUS;
            req.type = TYPE_DRONE_STATUS;
            req.drone.battery = 80;
            req.drone.pos.x = 15;
            req.drone.pos.y = 35;
            req.drone.pos.z = 40;
            
            showmess(req);
            write(socket_fd, (void*)&req, sizeof(Tmessage));
            recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
            showmess(ack);    
        }
        if (opt == DRONE_DISCONNECT) {
            strcpy(req.drone.droneID, argv[1]);
            req.codereq = DRONE_DISCONNECT;
            req.type = TYPE_ACK;
            
            showmess(req);
            write(socket_fd, (void*)&req, sizeof(Tmessage));
            recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
            showmess(ack);
            
            req.codereq = 555;
            req.type = TYPE_ACK;
            showmess(req);
        }
        if (opt == USER_IDENTIFIER) {
            req.type = TYPE_ACK;
            req.codereq = USER_IDENTIFIER;
            
            showmess(req);
            write(socket_fd, (void*)&req, sizeof(Tmessage));
            recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
            showmess(ack);
        }
        if (opt == USER_START_APPLICATION) {
            req.type = TYPE_ACK;
            req.codereq = USER_START_APPLICATION;
            
            showmess(req);
            write(socket_fd, (void*)&req, sizeof(Tmessage));
            recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
            showmess(ack);
        }
        if (opt == USER_REQ_STATUS) {
            req.codereq = USER_REQ_STATUS;
            req.type = TYPE_GLOBALSTATUS;

            showmess(req);
            write(socket_fd, (void*)&req, sizeof(Tmessage));
            recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
            showmess(ack);

            for (int i = 0; i < ack.droneList.quant; i++) {
                afficherDrone(ack.droneList.drones[i]);
            }
        }
    }

    req.codereq = 555;
    req.type = TYPE_ACK;

    showmess(req);
    write(socket_fd, (void*)&req, sizeof(Tmessage));

    close(socket_fd);
    return 0;
}