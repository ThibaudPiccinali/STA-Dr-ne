import socket
import ctypes as ct
import struct
import sys
import time
import random as rd
from messagerie import *

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
    elif (ack.codereq == ACK_DRONE_DEMANDE_ACTION_POS):
        print("Drone va à la position ("+str(ack.pos.x)+", "+str(ack.pos.y)+", "+str(ack.pos.z)+")\n")
        drone.pos = ack.pos
    elif (ack.codereq == ACK_DRONE_DEMANDE_ACTION_FIN):
        print("Drone arrete\n")
        drone.isON = 0
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