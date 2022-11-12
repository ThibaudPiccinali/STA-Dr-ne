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
    //----------------------------------------------------//
    printf("Identify User\n");
    req.type = TYPE_ACK;
    req.codereq = USER_IDENTIFIER;
    
    //showmess(req);
    write(socket_fd, (void*)&req, sizeof(Tmessage));
    recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
    //showmess(ack);
    if (ack.codereq = ACK_USER_IDENTIFIER) {
        printf("User identified\n\n");
    } else if (ack.codereq = ERROR_USER_IDENTIFIER) {
        printf("Error to identify user\n\n");
    }
    //----------------------------------------------------//
    //---------------------------------------------------//
    printf("Starting application\n");
    req.type = TYPE_ACK;
    req.codereq = USER_START_APPLICATION;
    
    //showmess(req);
    write(socket_fd, (void*)&req, sizeof(Tmessage));
    recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
    //showmess(ack);
    if (ack.codereq = ACK_USER_START_APPLICATION) {
        printf("Application started\n\n");
    } else if (ack.codereq = ERROR_USER_START_APPLICATION) {
        printf("Failed to start application\n\n");
    }
    //-------------------------------------------------//
    //------------------------------------------------//
        req.codereq = USER_REQ_STATUS;
    req.type = TYPE_GLOBALSTATUS;

    while(1) {
        //showmess(req);
        printf("Getting global status\n");
        write(socket_fd, (void*)&req, sizeof(Tmessage));
        recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
        //showmess(ack);
        if (ack.codereq = ACK_DRONE_STATUS) {
            printf("Global status received\n");
            printf("Liste de drones connectes:\n");
            for (int i = 0; i < ack.droneList.quant; i++) {
                afficherDrone(ack.droneList.drones[i]);
            }
            printf("\n");
        } else if (ack.codereq = ERROR_DRONE_IDENTIFIER) {
            printf("Failed to get global status\n\n");
        }

        sleep(5);
    }
    //-----------------------------------------------//
    req.codereq = 555;
    req.type = TYPE_ACK;

    showmess(req);
    write(socket_fd, (void*)&req, sizeof(Tmessage));

    close(socket_fd);
    return 0;
}