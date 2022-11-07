# Import
import cv2
import time
from djitellopy import Tello

#Constantes
position_initiale_Drone=[0,0]
position_Drone=position_initiale_Drone
taille_case=50 # Chaque case du damier fait 50 cm de côté (ce sont des carrés)

#Fonctions
def init():
    myDrone = Tello()   # create drone object
    myDrone.connect()   # connect drone
    return myDrone

def moveto(x,y,Drone,pos): # pos est la position actuelle du Drone (avant déplacement)
    if(x-pos[0]>0):
        Drone.move_forward((x-pos[0])*taille_case)
    if(x-pos[0]<0):
        Drone.move_back(-(x-pos[0])*taille_case)
    if(y-pos[1]>0):
        Drone.move_right((y-pos[1])*taille_case)
    if(y-pos[1]<0):
        Drone.move_left(-(y-pos[1])*taille_case)
    return [x,y]

def photo(Drone,nom): # prend une photo à l'aide du Drone et l'enregristre sous le nom "nom"
    Drone.streamon()
    frame_read = Drone.get_frame_read()
    cv2.imwrite(nom+".png", frame_read.frame)
    Drone.streamoff()

# Démonstration
myDrone=init()
# Takeoff
myDrone.takeoff()
position_Drone=moveto(1,1,myDrone,position_Drone)
photo(myDrone,"test")
position_Drone=moveto(0,0,myDrone,position_Drone)
# Land
myDrone.land()
