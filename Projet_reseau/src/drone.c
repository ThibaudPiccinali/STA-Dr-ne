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