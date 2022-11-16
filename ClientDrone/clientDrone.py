import socket
import ctypes as ct
import struct
import sys
import time
import threading
import cv2
from djitellopy import Tello
from messagerie import *

def init():
    myDrone = Tello()   # create drone object
    myDrone.connect()   # connect drone
    myDrone.streamon()
    return myDrone

def moveto(x,y,Drone): # pos est la position actuelle du Drone (avant déplacement)
    if(x-Drone.pos.x>0):
        Drone.move_forward((x-Drone.pos.x))
    if(x-Drone.pos.x<0):
        Drone.move_back(-(x-Drone.pos.x))
    if(y-Drone.pos.y>0):
        Drone.move_right((y-Drone.pos.y))
    if(y-Drone.pos.y<0):
        Drone.move_left(-(y-Drone.pos.y))
    return [x,y]


def photo(Drone,nom): # prend une photo à l'aide du Drone et l'enregristre sous le nom "nom"
    frame_read = Drone.get_frame_read()
    cv2.imwrite(nom+".png", frame_read.frame)

def asservissement (drone, pos):
    moveto(pos.x,pos.y,myDrone)
    photo(myDrone,str(pos.x)+"_"+str(pos.y)+"_"+str(pos.z))
    drone.pos.x = pos.x
    drone.pos.y = pos.y
    drone.pos.z = pos.z
    return

myDrone=init()

systemON = 0

print('Enter drone id:')
droneID = str.encode(input())


drone = Tdrone()
drone.droneID = droneID
drone.battery = 80
drone.pos.x = 0
drone.pos.y = 0
drone.pos.z = 0
drone.isON = 0

req = Tmessage()

req.codereq = 0
req.drone.droneID = droneID
req.drone.presenceImage = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 3000))

#IDENTIFY
print("Drone identification request")
req.drone = drone
req.codereq = DRONE_IDENTIFIER

s.send(req)
data = s.recv(4096)
ack = Tmessage.from_buffer_copy(data)
if (ack.codereq == ACK_DRONE_IDENTIFIER):
    print("Drone identified\n")
elif (ack.codereq == ERROR_DRONE_IDENTIFIER):
    print("Error to identify drone\n")


while(ack.codereq != ACK_DRONE_DISCONNECT):
    
    drone.battery = myDrone.get_battery()
    
    #DRONE-STATUS
    req.drone = drone
    req.codereq = DRONE_STATUS

    print("Sending drone status")
    afficherDrone(drone)
    
    s.send(req)
    data = s.recv(4096)
    ack = Tmessage.from_buffer_copy(data)

    if (ack.codereq == ACK_DRONE_STATUS):
        print("Drone status sent\n")
    elif (ack.codereq == ERROR_DRONE_IDENTIFIER):
        print("Error to send drone status\n")
        
    #DRONE-DEMANDE-ACTION
    req.drone = drone
    req.codereq = DRONE_DEMANDE_ACTION
    print("Waiting for action...")
    
    s.send(req)
    data = s.recv(4096)
    ack = Tmessage.from_buffer_copy(data)
    
    if (ack.codereq == ACK_DRONE_DEMANDE_ACTION_NONE):
        print("Drone ne fait rien\n")
    elif (ack.codereq == ACK_DRONE_DEMANDE_ACTION_START):
        print("Drone demarre\n")
        drone.isON = 1
        myDrone.takeoff()
        myDrone.move_down(50)
    elif (ack.codereq == ACK_DRONE_DEMANDE_ACTION_POS):
        print("Drone va à la position ("+str(ack.pos.x)+", "+str(ack.pos.y)+", "+str(ack.pos.z)+")\n")
        if __name__ == "__main__":
            threadpos = threading.Thread(target=asservissement, args=(drone,ack.pos, ))
            threadpos.start()

    elif (ack.codereq == ACK_DRONE_DEMANDE_ACTION_FIN):
        print("Drone arrete\n")
        drone.isON = 0
        myDrone.land()
    time.sleep(1)
    
    
#DRONE-DISCONNECT
print("Drone disconnect request")

req.drone = drone
req.codereq = DRONE_DISCONNECT

s.send(req)
data = s.recv(4096)
ack = Tmessage.from_buffer_copy(data)

if (ack.codereq == ACK_DRONE_DISCONNECT):
    print("Drone disconnected\n")
elif (ack.codereq == ERROR_DRONE_DISCONNECT):
    print("Error to disconnect drone\n")
    
req.drone = drone
req.codereq = 555

s.send(req)


s.close()