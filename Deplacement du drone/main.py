import cv2
import time

from djitellopy import Tello

myDrone = Tello()   # create drone object
myDrone.connect()   # connect drone
myDrone.enable_mission_pads()
print(myDrone.get_battery())    # display drone battery
#myDrone.streamon()
#frame_read = myDrone.get_frame_read()


# Takeoff
#myDrone.takeoff()
# Avance tout droit
#myDrone.move_forward(50) ## déplacement en cm
#Tourne
#myDrone.rotate_clockwise(90)
#myDrone.flip('r')
#cv2.imwrite("picture.png", frame_read.frame)
time.sleep(3)
mission_pad_number=myDrone.get_mission_pad_id()
myDrone.disable_mission_pads()
print("identifiant : "+str(mission_pad_number))
# Land
#myDrone.land()
