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

secteurs = [[0,1,0,0],[0,0,0,0]]
arr = (ct.c_int * 4 * 2)(*(tuple(i) for i in secteurs))
drone = Tdrone(droneID,Tposition(100,90,80),arr,70,0)

req = Tmessage()

req.codereq = 0
req.drone.battery = 0
req.drone.droneID = droneID
req.drone.pos.x = 0
req.drone.pos.y = 0
req.drone.pos.z = 0
req.drone.presenceImage = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # à mettre au tt débit --> pour se connecter au serveur
s.connect(('127.0.0.1', 3000))

#IDENTIFY
print("Drone identification request")
req.drone.droneID = drone.droneID
req.codereq = DRONE_IDENTIFIER
req.type = TYPE_DRONE_STATUS

s.send(req)
data = s.recv(4096)
ack = Tmessage.from_buffer_copy(data)
if (ack.codereq == ACK_DRONE_IDENTIFIER):
    print("Drone identified\n")
elif (ack.codereq == ERROR_DRONE_IDENTIFIER):
    print("Error to identify drone\n")

#CHECK-SYSTEM
req.codereq = DRONE_CHECK_SYSTEM_STATUS
req.type = TYPE_ACK

print("System is OFF")    
while (not systemON) :
    s.send(req)
    data = s.recv(4096)
    ack = Tmessage.from_buffer_copy(data)

    if (ack.codereq == 1041):
        print("System is ON\n")
        systemON = 1
    time.sleep(1)

#DRONE-STATUS
req.codereq = DRONE_STATUS
req.type = TYPE_DRONE_STATUS

while(drone.battery>0):
    drone.battery -= rd.randint(0,10)
    drone.pos.x += rd.randint(-10,10)
    drone.pos.y += rd.randint(-10,10)
    drone.pos.z += rd.randint(-10,10)
    req.drone = drone

    print("Sending drone status")
    afficherDrone(drone)
    
    s.send(req)
    data = s.recv(4096)
    ack = Tmessage.from_buffer_copy(data)

    if (ack.codereq == ACK_DRONE_STATUS):
        print("Drone status sent\n")
    elif (ack.codereq == ERROR_DRONE_IDENTIFIER):
        print("Error to send drone status\n")

    time.sleep(5)

#DRONE-DISCONNECT
print("Drone disconnect request")

req.codereq = DRONE_DISCONNECT
req.type = TYPE_ACK


s.send(req)
data = s.recv(4096)
ack = Tmessage.from_buffer_copy(data)

if (ack.codereq == ACK_DRONE_DISCONNECT):
    print("Drone disconnected\n")
elif (ack.codereq == ERROR_DRONE_DISCONNECT):
    print("Error to disconnect drone\n")
    
req.codereq = 555
req.type = TYPE_ACK


s.send(req)


s.close()