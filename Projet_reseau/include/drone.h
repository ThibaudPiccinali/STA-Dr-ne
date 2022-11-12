#ifndef _DRONE_H
#define _DRONE_H

#include <string.h>
#include <math.h>

#define MAXCHAR 20
#define TAILLE_IMAGE 256
#define MAXDRONES 2
#define SECTEURS_X 4
#define SECTEURS_Y 2
#define MAXPOS 100

typedef int Timage[TAILLE_IMAGE][TAILLE_IMAGE];

typedef char Tdrone_id[MAXCHAR];

typedef struct {
    int x;
    int y;
    int z;
} Tposition;

typedef struct {
    Tdrone_id droneID;
    Tposition pos;
    int secteur[SECTEURS_X][SECTEURS_Y];
    int battery;
    int presenceImage;
    //Timage image;
} Tdrone;

typedef struct {
    Tdrone drones[MAXDRONES];
    int secteurs[MAXDRONES];
    int quant;
} Tens_drone;

Tposition dist(Tposition pos1, Tposition pos2);
double abs_pos(Tposition pos);

void afficherDrone(Tdrone drone);

int recherche(Tdrone_id droneid, Tens_drone ensemble);

#endif
