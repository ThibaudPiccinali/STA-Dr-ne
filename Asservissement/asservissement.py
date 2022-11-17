# Import

import numpy as np
import cv2
import math
import imutils
from djitellopy import Tello
import time

#Fonctions

def imageregistration(nomImage1,nomImage2):
    ## On cherche dans un premier temps la rotation nécessaire
    img1 = cv2.imread(nomImage1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(nomImage2, cv2.IMREAD_GRAYSCALE)

    akaze = cv2.AKAZE_create()
    kp1, des1 = akaze.detectAndCompute(img1, None)
    kp2, des2 = akaze.detectAndCompute(img2, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.75*n.distance:
            good_matches.append([m])

    output = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv2.imwrite('Asservissement/output1.png', output)

    # Select good matched keypoints
    ref_matched_kpts = np.float32([kp1[m[0].queryIdx].pt for m in good_matches])
    sensed_matched_kpts = np.float32([kp2[m[0].trainIdx].pt for m in good_matches])

    # Compute homography
    H, status = cv2.findHomography(sensed_matched_kpts, ref_matched_kpts, cv2.RANSAC,5.0)
    #print(H)
    theta=math.degrees(math.atan(H[1][0]/H[0][0]))

    #print(theta) # Rotation nécessaire pour retrouver l'image originale.

    #Rotate Image
    rotate_image=imutils.rotate(img2,theta)
    cv2.imwrite('Asservissement/rotate.jpg', rotate_image)

    ## On cherche maintenant uniquement la translation nécessaire
    img1 = cv2.imread(nomImage1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread('Asservissement/rotate.jpg', cv2.IMREAD_GRAYSCALE)

    akaze = cv2.AKAZE_create()
    kp1, des1 = akaze.detectAndCompute(img1, None)
    kp2, des2 = akaze.detectAndCompute(img2, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.75*n.distance:
            good_matches.append([m])

    output = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv2.imwrite('Asservissement/output2.png', output)

    # Select good matched keypoints
    ref_matched_kpts = np.float32([kp1[m[0].queryIdx].pt for m in good_matches])
    sensed_matched_kpts = np.float32([kp2[m[0].trainIdx].pt for m in good_matches])

    # Compute homography
    H, status = cv2.findHomography(sensed_matched_kpts, ref_matched_kpts, cv2.RANSAC,5.0)
    #print(H)

    #print(H[0][2]) # Deplacement en x nécessaire pour retrouver l'image originale. 
    #print(H[1][2]) # Deplacement en y nécessaire pour retrouver l'image originale.

    # Warp image
    warped_image = cv2.warpPerspective(img2, H, (img2.shape[1], img2.shape[0]))
                
    cv2.imwrite('Asservissement/warped.jpg', warped_image)
    return [H[0][2],H[1][2],theta]

def init():
    myDrone = Tello()   # create drone object
    myDrone.connect()   # connect drone
    myDrone.enable_mission_pads()
    myDrone.streamon()
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
    frame_read = Drone.get_frame_read()
    cv2.imwrite(nom+".png", frame_read.frame)

def reconnaissance_pad(Drone): #retourne l'identifiant (un string) du pad détecté au sol (-1 si rein détecté)
    mission_pad_number=Drone.get_mission_pad_id()
    return str(mission_pad_number)

#Constantes
limite_x= 10
limite_y= 10
limite_angle= 10
taille_pixel=0.04 #1px est équivalent à 0.04 cm



myDrone=init()
print(myDrone.get_battery())    # display drone battery
# Takeoff
myDrone.takeoff()
myDrone.move_down(30)
#Asservissement
while(True):
    # On asservit le drone en position
    photo(myDrone,"Asservissement/photo_asservissement")
    l=imageregistration('Photosreferences/1.0.png','Asservissement/photo_asservissement.png')
    print("Pixel en x : "+ str(l[0])+" Pixel en y : "+ str(l[1])+" Angle : "+ str(l[2]))
    depl_x=int(l[0]*taille_pixel)
    depl_y=int(l[1]*taille_pixel)
    angle=int(l[2])
    print("Deplacement en x : "+ str(depl_x)+"cm Deplacement en y : "+ str(depl_y)+"cm Angle : "+ str(angle))
    # Condition de fin d'asservissemement
    if (depl_x<limite_x and depl_y<limite_y and angle<limite_angle):
        break
    myDrone.set_speed(10)
    if (angle>limite_angle):
        if (l[2]>0):
            myDrone.rotate_counter_clockwise(angle)
        else :
            myDrone.rotate_clockwise(-angle)
    if (np.abs(depl_x)>limite_x):
        if (depl_x<0):
            myDrone.move_right(-depl_x)
        else :
            myDrone.move_left(depl_x)
    if (np.abs(depl_y)>limite_y):
        if (depl_y<0):
            myDrone.move_forward(-depl_y)
        else :
            myDrone.move_back(depl_y)
    break
print("Asservissement terminé")
# Land
myDrone.land()

