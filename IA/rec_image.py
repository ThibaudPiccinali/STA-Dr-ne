## Import bibliotheques
import numpy as np
from matplotlib import pyplot as plt
from tensorflow.keras import models
import cv2
import os
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
import random

taille=124
## Fonctions utiles
def predire(image):
    X=np.array(image,dtype='float').reshape(-1,taille,taille,3)
    X/=255
    predict=model.predict(X)
    print(predict)
    if(predict[0][1]<=0.5):
        print("Aucun obstacle")
        return 0
    else:
        print("Obstacle detecté")
        return 1
## Récupération du modèle entrainé
model=models.load_model("model.h5")

img = load_img('Images/avec_obs/11.png')
img_array = img_to_array(img)
new_image_array=cv2.resize(img_array,(taille,taille))
predire(new_image_array)


