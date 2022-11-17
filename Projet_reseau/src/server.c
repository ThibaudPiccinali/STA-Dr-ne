/*
TODO:   ajouter les mutex pour proteger ensembleDrones

TODO:   proteger le code en utilisant la programation defensive: traiter
        les arguments de ligne de commande et utiliser check_error() 
        pour verifier les échecs des fonctions

TODO:   traiter les echecs et envoyer les code d'erreur aux clients (codereq: 5XX)

TODO:   corriger le bug de connexion
*/

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

#define check_error(val,msg)    if (val==-1) { perror(msg); exit(-1);} 

int serverConfig(int port);
int accept_new_connection(int server_socket);
void* handle_connection(void* p_sock);

int getNextAction(Tdrone drone, Tvector3* pos);
int detecterObstacle(Tdrone drone);

typedef struct sockaddr_in SA_IN;
typedef struct sockadd SA;

// le tableau avec les drones connectes
Tens_drone ensembleDrones;
int connectedClients;
pthread_mutex_t lockEnsemle;
pthread_mutex_t lockCompteur;

int main(int argc, char * argv[])   {

    pthread_mutex_lock(&lockCompteur);
    connectedClients = 0;
    pthread_mutex_unlock(&lockCompteur);
    
    pthread_t t;
    
    int listenSocket;
    int clientSocket[MAXCLI];

    // Configuration du serveur
    if (argc == 1) {
        listenSocket = serverConfig(portlocal);
    } else {
        listenSocket = serverConfig(htons(atoi(argv[1])));
    }


    printf("En attente de connection...\n");
    
    // Connexion avec des clients et creation d'un thread pour gérer connexions 
    pthread_mutex_lock(&lockCompteur);
    while(clientSocket[connectedClients] = accept(listenSocket, (struct sockaddr* ) NULL, NULL)) {
        if (clientSocket[connectedClients] != 0) {
            printf("\nNouvelle connexion !\n");
            pthread_create(&t, NULL, handle_connection, clientSocket);
        }
        pthread_mutex_unlock(&lockCompteur);
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
    Tvector3 pos;
    int index;
    int action;
    showmess(req);
    /*if (req.checksum != checksum(req)) {
        return -1;
    }*/
  
    switch (req.codereq) {
    /*-----------------------------------------------------------------*/
    /*-----------------------------------------------------------------*/
    /*------------------------------DRONE------------------------------*/
    /*-----------------------------------------------------------------*/
    /*-----------------------------------------------------------------*/
    case DRONE_IDENTIFIER :  // CODE 101 : AJOUTE D'UN DRONE
        
        ensembleDrones.drones[ensembleDrones.quant] = req.drone;
        ensembleDrones.quant++;

        isDrone = 1;

        printf("Drone %s ajoute \nDrone list:\n", req.drone.droneID);
        for (int i = 0; i < ensembleDrones.quant; i++) {
            afficherDrone(ensembleDrones.drones[i]);
        }

        printf("\n");

        ack = createMess(ACK_DRONE_IDENTIFIER, &(req.drone), NULL, NULL);
        write(sockfd, (void*) &ack, message_size);
    
        break;
    /*-----------------------------------------------------------------*/
    case DRONE_STATUS:   // CODE 102 : STATUS REPORT
        printf("Drone %s status report: \n", req.drone.droneID);
        int aux;
        
        index = recherche(req.drone.droneID, ensembleDrones);
        aux = ensembleDrones.drones[index].isON; 
        ensembleDrones.drones[index] = req.drone;
        ensembleDrones.drones[index].isON = aux;
        afficherDrone(ensembleDrones.drones[index]);
        saveImage(ensembleDrones.drones[index].image, "IMGserver.pbm");

        printf("\n");
        
        ack = createMess(ACK_DRONE_STATUS, &(req.drone), NULL, NULL);
        write(sockfd, (void*) &ack, message_size);

        break;
    /*-----------------------------------------------------------------*/
    case DRONE_DEMANDE_ACTION:
        printf("Drone request action\n");
        
        action = getNextAction(req.drone, &pos);
        
        if (action == 0) {
            printf("\tNo action sent\n\n");
            ack = createMess(ACK_DRONE_DEMANDE_ACTION_NONE, &(req.drone), NULL, NULL);
        } else if (action == 1) {
            printf("\tDrone %s start\n\n", req.drone.droneID);
            ack = createMess(ACK_DRONE_DEMANDE_ACTION_START, &(req.drone), NULL, NULL);
        } else if (action == 2) {
            printf("\tDrone %s envoye a la position (%d, %d, %d)\n\n", req.drone.droneID, pos.x, pos.y, pos.z);
            ack = createMess(ACK_DRONE_DEMANDE_ACTION_POS, &(req.drone), NULL, &pos);
        } else if (action == 3) {
            printf("\tDrone %s stop\n\n", req.drone.droneID);
            ack = createMess(ACK_DRONE_DEMANDE_ACTION_FIN, &(req.drone), NULL, NULL);
        }

        write(sockfd, (void*) &ack, message_size);
        
        break;    
    /*-----------------------------------------------------------------*/
    case DRONE_DISCONNECT:   // CODE 103 : SUPPRESION D'UN DRONE
        printf("Supression du drone %s \n", req.drone.droneID);


        index = recherche(req.drone.droneID, ensembleDrones); 

        if (index == -1) {
            printf("Le drone n'est pas dans la liste\n");
            break;
        }
        for(int i = index; i < ensembleDrones.quant-1; i++) {
            ensembleDrones.drones[i] = ensembleDrones.drones[i+1];
        }
        ensembleDrones.quant--;

        printf("\n");
        
        ack = createMess(ACK_DRONE_DISCONNECT, &(req.drone), NULL, NULL);
        write(sockfd, (void*) &ack, message_size);

        break;
    /*-----------------------------------------------------------------*/
    /*-----------------------------------------------------------------*/
    /*-------------------------------USER------------------------------*/
    /*-----------------------------------------------------------------*/
    /*-----------------------------------------------------------------*/
    case USER_IDENTIFIER:
        printf("Utilisateur connecte\n\n");

        isDrone = 0;

        ack = createMess(ACK_USER_IDENTIFIER, NULL, NULL, NULL);
        write(sockfd, (void*) &ack, message_size);

        break;
    /*-----------------------------------------------------------------*/
    case USER_START_DRONE:
        printf("Initialisation du drone \n\n");

        index = recherche(req.drone.droneID, ensembleDrones);

        ensembleDrones.drones[index].isON = 1;
        afficherDrone(ensembleDrones.drones[index]);
        
        ack = createMess(ACK_USER_START_DRONE, &(ensembleDrones.drones[index]), &ensembleDrones, NULL);

        write(sockfd, (void*)&ack, message_size);

        break;
    /*-----------------------------------------------------------------*/
    case USER_STOP_DRONE:
        printf("Fin de l'application \n\n");

        index = recherche(req.drone.droneID, ensembleDrones);

        ensembleDrones.drones[index].isON = 0;

        ack = createMess(ACK_USER_STOP_DRONE, &(ensembleDrones.drones[index]), &ensembleDrones, NULL);
        write(sockfd, (void*)&ack, message_size);

        break;
    /*-----------------------------------------------------------------*/
    case USER_REQ_STATUS:
        printf ("Status report au utilisateur\n\n");

        ack = createMess(ACK_USER_REQ_STATUS, NULL, &ensembleDrones, NULL);

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

    pthread_mutex_lock(&lockCompteur);
    int clientID = connectedClients;
    connectedClients++;
    pthread_mutex_unlock(&lockCompteur);

    int* clientSockets = (int*) p_sock;
    int sockfd = clientSockets[clientID];
    
    int isDrone = -1;

    int readSize;

    Tmessage req, ack;
    initmess(&req);
    initmess(&ack);

    const size_t message_size = sizeof(Tmessage); 

    pthread_mutex_lock(&lockCompteur);
    printf("Connected sockets: ");
    for (int i = 0; i  < connectedClients-1; i++) {
        printf("%d, ", clientSockets[i]);
    }
    printf("%d\n", clientSockets[connectedClients-1]);
    pthread_mutex_unlock(&lockCompteur);

    printf("Connection avec clientID %d etablie, socket n: %d\n\n", clientID, sockfd);

    // Reception des messages et traitement
    while ( (readSize = recv(sockfd, (void*) &req, message_size, 0) > 0) ) {
        //showmess(req);
        treat_message(clientSockets, sockfd, isDrone, clientID, req, ack);
    }
    printf("Connection avec client %d, dans le socket %d termine\n\n", clientID, sockfd);
    
    for(int i = clientID; i < connectedClients-1; i++) {
        clientSockets[i] = clientSockets[i+1];
    }
    connectedClients--;

    return NULL;
}

int getNextAction(Tdrone drone, Tvector3* pos) {
    int index = recherche(drone.droneID, ensembleDrones);
// En pratique ça va demander a un algorithme externe la position pour y aller    
    if (!ensembleDrones.drones[index].isON && !drone.isON) {
        return 0;
    }
    if (ensembleDrones.drones[index].isON && !drone.isON) {
        return 1;
    }
    if (!ensembleDrones.drones[index].isON && drone.isON) {
        return 3;
    }
    if (pos->x != drone.pos.x || pos->y != drone.pos.y || pos->z != drone.pos.z) {
        return 0;
    }

    pos->y = (pos->y + 25);
    
    return 2;
}