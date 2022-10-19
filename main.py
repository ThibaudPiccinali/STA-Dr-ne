import cv2
import time

from djitellopy import Tello

myDrone = Tello()   # create drone object
myDrone.connect()   # connect drone
print(myDrone.get_battery())    # display drone battery
myDrone.streamon()
frame_read = myDrone.get_frame_read()


# Takeoff
myDrone.takeoff()
# Avance tout droit
myDrone.move_forward(100)
#Tourne
#myDrone.rotate_clockwise(90)
time.sleep(3)
myDrone.flip('r')
cv2.imwrite("picture.png", frame_read.frame)
# Land
myDrone.land()
