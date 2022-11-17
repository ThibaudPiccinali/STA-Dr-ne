import random
import shutil
import os
import cv2
import numpy as np

file_source = r'C:\Users\Thibaud Piccinali\.vscode\STA-Dr-ne\photosvideo\0'
file_destination = r'C:\Users\Thibaud Piccinali\.vscode\STA-Dr-ne\photoIA\0'
 

for i in range(1,201):
    t=1
    while(t!=0):
        t=1
        n=random.randint(1,5578) # 5578 sans obs, 2799 avec obs
        g="/"+str(n)+".png"
        if (os.path.exists(file_source + g)):
            t=0
            shutil.move(file_source + g, file_destination)
