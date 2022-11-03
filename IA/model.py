## Import
from importlib.resources import path
import pandas as pd

import numpy as np

from matplotlib import pyplot as plt

import seaborn as sns

from sklearn import model_selection

from sklearn.metrics import classification_report, confusion_matrix, roc_curve, roc_auc_score,auc, accuracy_score

from sklearn.preprocessing import StandardScaler, MinMaxScaler

from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import train_test_split

from sklearn import datasets

from tensorflow.keras.models import Sequential, load_model

from tensorflow.keras.layers import Dense, Dropout, Flatten

from tensorflow.keras.layers import Conv2D, MaxPooling2D

from tensorflow.keras.utils import to_categorical

import cv2
import os
import glob
import gc

from tensorflow.keras.applications import InceptionV3, ResNet50V2

## Fonctions utiles
def lire_images(img_dir, xdim, ydim, nmax=5000) :
    """ 
    Lit les images dans les sous répertoires de img_dir
    nmax images lues dans chaque répertoire au maximum
    Renvoie :
    X : liste des images lues, matrices xdim*ydim
    y : liste des labels numériques
    label : nombre de labels
    label_names : liste des noms des répertoires lus
    """
    label = 0
    label_names = []
    X = []
    y=[]
    for dirname in os.listdir(img_dir):
        print(dirname)
        label_names.append(dirname)
        data_path = os.path.join(img_dir + "/" + dirname,'*g')
        files = glob.glob(data_path)
        n=0
        for f1 in files:
            if n>nmax : break
            img = cv2.imread(f1) # Lecture de l'image dans le repertoire
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Conversion couleur RGB
            img = cv2.resize(img, (xdim,ydim)) # Redimensionnement de l'image
            X.append(np.array(img)) # Conversion en tableau et ajout a la liste des images
            y.append(label) # Ajout de l'etiquette de l'image a la liste des etiquettes
            n=n+1
        print(n,' images lues')
        label = label+1
    X = np.array(X)
    y = np.array(y)
    gc.collect() # Récupération de mémoire
    return X,y, label, label_names

def plot_scores(train) :
    accuracy = train.history['accuracy']
    val_accuracy = train.history['val_accuracy']
    epochs = range(len(accuracy))
    plt.plot(epochs, accuracy, 'b', label='Score apprentissage')
    plt.plot(epochs, val_accuracy, 'r', label='Score validation')
    plt.title('Scores')
    plt.legend()
    plt.show()

## Création du modèle
path= r"C:\Users\Thibaud Piccinali\Desktop\STA-Dr-ne\IA\Data\Archive\Birdvsbutterfly\Test"
X,y,Nombre_classes,Classes = lire_images(path, 224, 224, 1000)

y = to_categorical(y)
# Normalisation entre 0 et 1
X = X / 255
print(X[0][0])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=1)
del X,y

resnet = ResNet50V2(weights='imagenet', include_top=False, input_shape=(224,224,3))

resnet.trainable = False
resnet.layers[0].trainable = True

model = Sequential()
model.add(resnet)
model.add(Flatten())
model.add(Dense(Nombre_classes, activation='softmax'))

# Compilation du modèle
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

train = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=20, verbose=1)

inception = InceptionV3(weights='imagenet', include_top=False, input_shape=(224,224,3))

inception.trainable = False
inception.layers[0].trainable = True

model = Sequential()
model.add(inception)
model.add(Flatten())
model.add(Dense(Nombre_classes, activation='softmax'))

# Compilation du modèle
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

train = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=20, verbose=1)

plot_scores(train)
## Fin de la création du modèle

## Sauvegarde du modèle (pour de futur utilisation)
model.save("model.h5")
