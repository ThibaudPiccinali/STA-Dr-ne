#ifndef _DRONE_H
#define _DRONE_H

#include <string.h>
#include <math.h>

#define MAXCHAR 20
#define TAILLE_IMAGE 1
#define MAXDRONES 2
#define MAXPOS 100

typedef int Timage[TAILLE_IMAGE][TAILLE_IMAGE];

typedef char Tdrone_id[MAXCHAR];

typedef struct {
    int x;
    int y;
    int z;
} Tvector3;

typedef struct {
    Tdrone_id droneID;
    int isON;
    int battery;
    int obstacle;
    Tvector3 pos;
    Tvector3 vitesse;
    Timage image;
} Tdrone;

typedef struct {
    Tdrone drones[MAXDRONES];
    int quant;
} Tens_drone;

Tvector3 dist(Tvector3 pos1, Tvector3 pos2);
double abs_pos(Tvector3 pos);

void afficherDrone(Tdrone drone);

int recherche(Tdrone_id droneid, Tens_drone ensemble);

#endif
