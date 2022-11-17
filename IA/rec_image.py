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

## Tests
compte=0
for i in range(1,100):
    n=random.randint(1,2799)  # 5578 sans obs, 2799 avec obs
    nom='photosvideo/1/'+str(n)+'.png'
    if os.path.isfile(nom):
        img = load_img(nom)
        img_array = img_to_array(img)
        new_image_array=cv2.resize(img_array,(taille,taille))
        #plt.imshow(new_image_array.astype(int))
        #plt.show()
        compte+=predire(new_image_array)
print(compte)
