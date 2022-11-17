# import required module
import os
# assign directory
directory = r'C:\Users\Thibaud Piccinali\.vscode\STA-Dr-ne\obs1 [MConverter.eu] (1)'
 
# iterate over files in
# that directory
i=2483
for filename in os.listdir(directory):
    i+=1
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        os.rename(f,str(i)+".png")