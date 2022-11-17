/*
TODO:   proteger le code en utilisant la programation defensive: utiliser
        check_error() pour verifier les échecs des fonctions
*/

#include <string.h>
#include <stdio.h>
#include "../include/drone.h"

Tvector3 dist(Tvector3 pos1, Tvector3 pos2) {
    Tvector3 res;

    res.x = pos1.x-pos2.x;
    res.y = pos1.y-pos2.y;
    res.z = pos1.z-pos2.z;

    return res;    
}

double abs_pos(Tvector3 pos) {
    return sqrtf(powf(pos.x, 2) + powf(pos.y, 2) + powf(pos.z, 2));
}

void afficherDrone(Tdrone drone) {
    if (drone.isON) {
        printf("  %10s - Batterie: %2d%% - Pos: (%d, %d, %d) - ON\n", drone.droneID, drone.battery, drone.pos.x, drone.pos.y, drone.pos.z);
    } else {
        printf("  %10s - Batterie: %2d%% - Pos: (%d, %d, %d) - OFF\n", drone.droneID, drone.battery, drone.pos.x, drone.pos.y, drone.pos.z);
    }
}

int recherche(Tdrone_id droneid, Tens_drone ensemble) {
    int i;
    for (i = 0; i < MAXDRONES; i++) {
        if (strcmp(droneid, ensemble.drones[i].droneID) == 0) {
            return i;
        }
    }
    return -1;
}

void saveImage(Timage image, char* nom) {
    FILE* fd = fopen(nom, "w");
    fprintf(fd, "P2\n%d %d\n255\n", TAILLE_IMAGE, TAILLE_IMAGE);

  //  char imgstr[TAILLE_IMAGE*TAILLE_IMAGE+2];
    for (int i = 0; i < TAILLE_IMAGE; i++) {
        for (int j = 0; j < TAILLE_IMAGE; j++) {
            fprintf(fd, "%d ", image[i][j]);
        }
        fprintf(fd, "\n");
    }
    /*imgstr[TAILLE_IMAGE*TAILLE_IMAGE+1] = '\n';
    imgstr[TAILLE_IMAGE*TAILLE_IMAGE+2] = '\0';
    fwrite(image, sizeof(char), TAILLE_IMAGE*TAILLE_IMAGE+2, stdout);
*/
    fclose(fd);
}