#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <pthread.h>
#include "../include/drone.h"
#include "../include/messagerie.h"

#define portlocal 3000
#define MAXCAR 80
#define MAXCLI 3
#define MAXMESS 10

#define check_error(val,msg)    if (val==-1) { perror(msg); exit(-1);} 

int serverConfig(int port);
int accept_new_connection(int server_socket);
void* handle_connection(void* p_sock);

typedef struct sockaddr_in SA_IN;
typedef struct sockadd SA;

// le tableau avec les drones connectes
Tens_drone ensembleDrones;

int connectedClients;
int systemON;

// TODO: Proteger ces trois variables a chaque ocurrence avec un mutex ou semaphore

int main(int argc, char * argv[])   {

    connectedClients = 0;
    systemON = 0;
    
    pthread_t t;
    
    int listenSocket;
    int clientSocket[MAXCLI];

    if (argc == 1) {
        listenSocket = serverConfig(portlocal);
    } else {
        listenSocket = serverConfig(htons(atoi(argv[1])));
    }


    printf("En attente de connection...\n");
    
    while(clientSocket[connectedClients] = accept(listenSocket, (struct sockaddr* ) NULL, NULL)) {
        if (clientSocket[connectedClients] != 0) {
            printf("\nNouvelle connexion !\n");
            pthread_create(&t, NULL, handle_connection, clientSocket);
        }
    }

    close(listenSocket);

    return 1;
}


int serverConfig(int port) {
    int server_socket, client_socket, addr_size;
    SA_IN server_addr;

    server_socket = socket(AF_INET, SOCK_STREAM, 0);

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(port);
    
    bind(server_socket, (SA*) &server_addr, sizeof(server_addr));
    listen(server_socket, MAXCLI);

    return server_socket;
}

int treat_message(int* clientSockets, int sockfd, int isDrone, int clientID, Tmessage req, Tmessage ack) {
    
    const size_t message_size = sizeof(Tmessage); 

    //Traiter la requete    
    switch (req.codereq) {
    case DRONE_IDENTIFIER :  // CODE 101 : AJOUTE D'UN DRONE
            
        ensembleDrones.drones[ensembleDrones.quant] = req.drone;
        ensembleDrones.quant++;

        isDrone = 1;

        printf("Drone %s ajoute \nDrone list:\n", req.drone.droneID);
        for (int i = 0; i < ensembleDrones.quant; i++) {
            afficherDrone(ensembleDrones.drones[i]);
        }
        printf("\n");


        ack.type = TYPE_ACK;
        ack.codereq = ACK_DRONE_IDENTIFIER;
        write(sockfd, (void*) &ack, message_size);
    
        break;
    /*-----------------------------------------------------------------*/
    case USER_IDENTIFIER:
        printf("Utilisateur connecte\n\n");

        isDrone = 0;

        ack.type = TYPE_ACK;
        ack.codereq = ACK_USER_IDENTIFIER;
        write(sockfd, (void*) &ack, message_size);

        break;
    /*-----------------------------------------------------------------*/
    case DRONE_STATUS:   // CODE 102 : STATUS REPORT
        printf("Drone %s status report: \n", req.drone.droneID);

        ensembleDrones.drones[recherche(req.drone.droneID, ensembleDrones)] = req.drone;
        afficherDrone(ensembleDrones.drones[recherche(req.drone.droneID, ensembleDrones)]);
        printf("\n");
        
        ack.drone = req.drone;
        ack.type = TYPE_ACK;
        ack.codereq = ACK_DRONE_STATUS;
        write(sockfd, (void*) &ack, message_size);

        break;
    /*-----------------------------------------------------------------*/
    case DRONE_CHECK_SYSTEM_STATUS:
        printf("Drone request system status\n");

        ack.type = TYPE_ACK;
        if (systemON) {
            printf("Sytem ON\n\n");
            ack.codereq = 1041;
        } else {
            printf("Sytem OFF\n\n");
            ack.codereq = 1040;
        }
        write(sockfd, (void*) &ack, message_size);
        
        break;    
    /*-----------------------------------------------------------------*/
    case DRONE_DISCONNECT:   // CODE 103 : SUPPRESION D'UN DRONE
        printf("Supression du drone %s \n", req.drone.droneID);

        if (recherche(req.drone.droneID, ensembleDrones) == -1) {
            printf("Le drone n'est pas dans la liste\n");
            break;
        }
        printf("\n");
        ensembleDrones.quant--;

        ack.drone = req.drone;
        ack.type = TYPE_ACK;
        ack.codereq = ACK_DRONE_DISCONNECT;
        write(sockfd, (void*) &ack, message_size);

        break;
    /*-----------------------------------------------------------------*/
    case USER_START_APPLICATION:
        printf("Initialisation du systeme \n\n");

        // Retransmission du message a tous les clients sauf l'utilisateur
        /*for (int i = 0; i < connectedClients; i++) {
            if (sockfd != clientSockets[i]) {
                showmess(req);
                write(clientSockets[i], (void*) &req, message_size);
                // TODO: attendre un ack de chaque drone pour envoyer un ack au utilisateur
            }
        }*/
        systemON = 1;
        // Envoi du ack au utilisateur
        ack.type = TYPE_ACK;
        ack.codereq = ACK_USER_START_APPLICATION;
        write(sockfd, (void*)&ack, message_size);

        break;
    /*-----------------------------------------------------------------*/
    case USER_STOP_APPLICATION:
        printf("Fin de l'application \n\n");

        // Retransmission du message a tous les clients sauf l'utilisateur                
        for (int i = 0; i < connectedClients; i++) {
            if (sockfd != clientSockets[i]) {
                write(clientSockets[i], (void*) &req, message_size);
            }
        }
        // Envoi du ack au utilisateur
        ack.type = TYPE_ACK;
        ack.codereq = ACK_USER_STOP_APPLICATION;
        write(sockfd, (void*)&ack, message_size);

        break;
    /*-----------------------------------------------------------------*/
    case USER_REQ_STATUS:
        printf ("Status report au utilisateur\n\n");

        ack.codereq = ACK_USER_REQ_STATUS;
        ack.type = TYPE_GLOBALSTATUS;
        ack.droneList = ensembleDrones;
        write(sockfd, (void*)&ack, message_size);

        break;
    /*-----------------------------------------------------------------*/
    case 555:
        printf("Drone %s deconnecte\n", req.drone.droneID);
        close(sockfd);
        return 1;
        break;
    /*-----------------------------------------------------------------*/
    default : 
        printf("Cas imprevu !!!! \n");
    }
    return 0;
}

void* handle_connection(void* p_sock) {
    int clientID = connectedClients;
    connectedClients++;

    int* clientSockets = (int*) p_sock;
    int sockfd = clientSockets[clientID];
    
    int isDrone = -1;

    int readSize;

    Tmessage req, ack;
    initmess(&req);
    initmess(&ack);

    const size_t message_size = sizeof(Tmessage); 

    printf("Connect sockets: ");
    for (int i = 0; i  < connectedClients-1; i++) {
        printf("%d, ", clientSockets[i]);
    }
    printf("%d\n", clientSockets[connectedClients-1]);

    printf("Connection avec clientID %d etablie, socket n: %d\n\n", clientID, sockfd);

    while ( (readSize = recv(sockfd, (void*) &req, message_size, 0) > 0) ) {
        //showmess(req);

        treat_message(clientSockets, sockfd, isDrone, clientID, req, ack);
    }
    printf("Connection avec client %d, dans le socket %d termine\n\n", clientID, sockfd);
    connectedClients--;
    return NULL;
}