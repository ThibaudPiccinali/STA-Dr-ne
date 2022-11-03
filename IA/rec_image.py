## Import
import numpy as np
from matplotlib import pyplot as plt
from tensorflow.keras import models
import cv2
import os
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
## Fonctions utiles
def predire(image):
    X=np.array(image,dtype='float').reshape(-1,224,224,3)
    X/=255
    predict=model.predict(X)
    print(predict)
    if(predict[0][1]<=0.5):
        print("C'est un oiseau")
    else:
        print("C'est un papillon")
## Récupération du modèle entrainé
model=models.load_model("model.h5")
## Tests
img = load_img('1.jpg')
img_array = img_to_array(img)
new_image_array=cv2.resize(img_array,(224,224))
predire(new_image_array)
