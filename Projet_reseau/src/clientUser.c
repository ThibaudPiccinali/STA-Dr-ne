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

int connectToServer(char* ip, int port) {
    int socket_fd;
    struct sockaddr_in server_address;

    socket_fd = socket(AF_INET, SOCK_STREAM, 0);

    memset(&server_address, 0, sizeof server_address);
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(port);
    inet_pton(AF_INET, ip, &server_address.sin_addr);

    connect(socket_fd, (struct sockaddr *)&server_address, sizeof server_address);

    return socket_fd;
}

int menu() {
    int option;

    printf("\nAction:\n");
    printf("\t1 - Start drone\n");
    printf("\t2 - Stop drone\n");
    printf("\t3 - Get status\n");
    printf("\t0 - Close\n");
    printf("Action: ");
    scanf("%d", &option);

    if (option != 1 && option != 2 && option != 3 && option != 0) {
        return menu();
    }
    return option;
}

int main(int argc, char** argv) {

    int action;
    Tdrone_id droneID;
    Tens_drone ensembleDrones;
    Tdrone droneAux;

    int socket_fd = connectToServer(SERVER_IP, PORT);

    Tmessage req, ack;
    initmess(&req);
    initmess(&ack);

    //----------------------------------------------------//
    printf("Identify User\n");
    req = createMess(USER_IDENTIFIER, NULL, NULL, NULL);
    
    write(socket_fd, (void*)&req, sizeof(Tmessage));
    recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
    
    if (ack.codereq = ACK_USER_IDENTIFIER) {
        printf("User identified\n\n");
    } else if (ack.codereq = ERROR_USER_IDENTIFIER) {
        printf("Error to identify user\n\n");
    }
    //----------------------------------------------------//
    while(1) {
        action = menu();
        if (action == 1) {
            //----------------------------------------------------//
            printf("\tDroneID: ");
            scanf("%s", droneID);
            printf("\nStarting Drone...\n");
            
            strcpy(ensembleDrones.drones[recherche(droneID, ensembleDrones)].droneID, droneID);
            req = createMess(USER_START_DRONE, &(ensembleDrones.drones[recherche(droneID, ensembleDrones)]), NULL, NULL);
            
            write(socket_fd, (void*)&req, sizeof(Tmessage));
            recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
            
            if (ack.codereq = ACK_USER_START_DRONE) {
                printf("Drone started\n\n");
                ensembleDrones.drones[recherche(droneID, ensembleDrones)].isON = 1;
            } else if (ack.codereq = ERROR_USER_START_DRONE) {
                printf("Failed to start drone\n\n");
            }
            //----------------------------------------------------//
        } else if (action == 2) {
            //----------------------------------------------------//
            printf("\tDroneID: ");
            scanf("%s", droneID);
            printf("\nStopping Drone...\n");
            
            strcpy(ensembleDrones.drones[recherche(droneID, ensembleDrones)].droneID, droneID);
            req = createMess(USER_STOP_DRONE, &(ensembleDrones.drones[recherche(droneID, ensembleDrones)]), NULL, NULL);

            write(socket_fd, (void*)&req, sizeof(Tmessage));
            recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
            
            if (ack.codereq = ACK_USER_STOP_DRONE) {
                printf("Drone stopped\n\n");
                ensembleDrones.drones[recherche(droneID, ensembleDrones)].isON = 0;
            } else if (ack.codereq = ERROR_USER_STOP_DRONE) {
                printf("Failed to stop drone\n\n");
            }
            //----------------------------------------------------//
        } else if (action  == 3) {
            //----------------------------------------------------//
            req = createMess(USER_REQ_STATUS, NULL, NULL, NULL);
            
            printf("Getting global status\n");
            
            write(socket_fd, (void*)&req, sizeof(Tmessage));
            showmess(req);
            recv(socket_fd, (void*) &ack, sizeof(Tmessage), 0);
            

            if (ack.codereq = ACK_DRONE_STATUS) {
                printf("Global status received\n");
                ensembleDrones = req.droneList;
                printf("Liste de drones connectes:\n");
                for (int i = 0; i < ack.droneList.quant; i++) {
                    afficherDrone(ack.droneList.drones[i]);
                }
                printf("\n");
            } else if (ack.codereq = ERROR_DRONE_IDENTIFIER) {
                printf("Failed to get global status\n\n");
            }
            //----------------------------------------------------//
        } else if (action == 0) {
            req = createMess(555, NULL, NULL, NULL);
            write(socket_fd, (void*)&req, sizeof(Tmessage));

            close(socket_fd);
            return 0;
        }
    }
}