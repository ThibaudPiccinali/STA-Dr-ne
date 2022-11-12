#include <string.h>
#include <stdio.h>
#include "../include/drone.h"

Tposition dist(Tposition pos1, Tposition pos2) {
    Tposition res;

    res.x = pos1.x-pos2.x;
    res.y = pos1.y-pos2.y;
    res.z = pos1.z-pos2.z;

    return res;    
}

double abs_pos(Tposition pos) {
    return sqrtf(powf(pos.x, 2) + powf(pos.y, 2) + powf(pos.z, 2));
}

void afficherDrone(Tdrone drone) {
    printf("  %10s - Batterie: %2d%% - Pos: (%d, %d, %d)\n", drone.droneID, drone.battery, drone.pos.x, drone.pos.y, drone.pos.z);
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