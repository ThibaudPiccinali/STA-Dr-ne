import string
from random import randint, choice
from tkinter import *
import socket
import ctypes as ct
import struct
import sys
from time import strftime
from datetime import datetime
import random as rd
from messagerie import *
from tkinter import ttk

req = Tmessage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # à mettre au tt début --> pour se connecter au serveur
s.connect(('127.0.0.1', 3000))

#IDENTIFY
print("Drone identification request")
req.codereq = USER_IDENTIFIER
#req.type = TYPE_ACK

s.send(req)
data = s.recv(4096)
ack = Tmessage.from_buffer_copy(data)
if (ack.codereq == ACK_USER_IDENTIFIER):
    print("user identified\n")
elif (ack.codereq == ERROR_USER_IDENTIFIER):
    print("Error to identify user\n")

# Obtenir les positions enx,y,z
req.codereq = USER_REQ_STATUS

s.send(req)
data = s.recv(4096)
ack = Tmessage.from_buffer_copy(data)
if (ack.codereq == ACK_USER_REQ_STATUS):
    print("user identified\n")
elif (ack.codereq == ERROR_USER_REQ_STATUS):
    print("Error to identify user\n")

ensembledrone= Tens_drone()    
ensembledrone=ack.droneList
print(ensembledrone.drones[0].pos.x) # donner position x
print(ensembledrone.drones[0].battery)


# les noms du drone que l'on veut demarrer
def demarrer_drone():
    print("Starting application \n :")
    req.codereq = USER_START_DRONE
    req.drone.droneID = b"Drone1"
    #req.type = TYPE_ACK

    s.send(req)
    data = s.recv(4096)
    ack = Tmessage.from_buffer_copy(data)
    if (ack.codereq == ACK_USER_START_DRONE):
        print("Application started\n")
    elif (ack.codereq == ERROR_USER_START_DRONE):
        print("Failed to start application\n")

def arreter_drone():
    print("arreter application \n :")
    req.codereq = USER_STOP_DRONE
    req.drone.droneID = b"Drone1"
    #req.type = TYPE_ACK

    s.send(req)
    data = s.recv(4096)
    ack = Tmessage.from_buffer_copy(data)
    if (ack.codereq == ACK_USER_STOP_DRONE):
        print("Application stopped\n")
    elif (ack.codereq == ERROR_USER_STOP_DRONE):
        print("Failed to stopped application\n")

def bjr():
    return 1

# creer la fenetre
window = Tk()
window.title("Controle des drones")
window.geometry("980x760")
window.config(background="gray")

# creation de l'espace pour afficher les photos 
width=300
height=300
'''image = PhotoImage(file="STA-Dr-ne\Interface utilisateur\camera.png").zoom(25).subsample(40) # Attention obligatoirement en png
canvas = Canvas(window, width=width+100, height=height+10, bg='gray', bd=0, highlightthickness=0)
canvas.create_image(width/2, height/2, image=image)
canvas.place(x=350,y=100)'''



# Espace visualisation des positions du drone
frame_pos= Frame(window, bg='black', width=500, height=100)
label_pos = Label(frame_pos, text="Position  \n x : \n y : \n z : \n ", font=("Arial",16), bd=0, bg='white', fg='black', width=10, justify='left' )

# Canvas positions
canvas_x = Canvas(frame_pos, width=35, height=18, bg='gray')
canvas_x.place(x=60,y=32)

canvas_y = Canvas(frame_pos, width=35, height=18, bg='gray')
canvas_y.place(x=60,y=58)

canvas_z = Canvas(frame_pos, width=35, height=18, bg='gray')
canvas_z.place(x=60,y=83)

 # Espace visualisation des vitesses du drone
frame_vit= Frame(window, bg='black', width=500, height=100)
label_vit = Label(frame_vit, text="Vitesse    \n x :  \n y :  \n z :  \n", font=("Arial",16), bd=0, bg='white', fg='black' )
# Canvas vitesses
canvas_vx = Canvas(frame_vit, width=20, height=18, bg='gray')
canvas_vx.place(x=60,y=30)

canvas_vy = Canvas(frame_vit, width=20, height=18, bg='gray')
canvas_vy.place(x=60,y=55)

canvas_vz = Canvas(frame_vit, width=20, height=18, bg='gray')
canvas_vz.place(x=60,y=77)

# Fenêtre messages d'alerte
frame_alerte= Frame(window, bg='black', width=500, height=100)
label_alerte = Label(frame_alerte, text=" Message d'alerte des drones :  \n \n \n ", font=("Arial",16), bd=0, bg='white', fg='black' )

canvas_alerte = Canvas(frame_alerte, width=260, height=50, bg='yellow')
canvas_alerte.place(x=10,y=30)

# espace visualisation de la batterie

#image_bat = PhotoImage(file="STA-Dr-ne\Interface utilisateur\catterie.png").zoom(3) # Attention obligatoirement en png


x = ensembledrone.drones[0].pos.x
x_var = StringVar()
x_var.set(str(x))

y = ensembledrone.drones[0].pos.y
y_var = StringVar()
y_var.set(str(y))

z = ensembledrone.drones[0].pos.z
z_var = StringVar()
z_var.set(str(z))

# Récupération des vitesses

vx = ensembledrone.drones[0].vitesse.x
vx_var = StringVar()
vx_var.set(str(vx))

vy = ensembledrone.drones[0].vitesse.y
vy_var = StringVar()
vy_var.set(str(vy))

vz = ensembledrone.drones[0].vitesse.z
vz_var = StringVar()
vz_var.set(str(vz)) 

batterie = ensembledrone.drones[0].battery
batterie_var = StringVar()
batterie_var.set(str(batterie))


# affichage des positions 
text_x = canvas_x.create_text(27, 11, text=x_var.get())
text_y = canvas_y.create_text(27, 11, text=y_var.get())
text_z = canvas_z.create_text(27, 11, text=z_var.get())
text_vx = canvas_vx.create_text(12, 12, text=vx_var.get())
text_vy = canvas_vy.create_text(12, 12, text=vy_var.get())
text_vz = canvas_vz.create_text(12, 12, text=vz_var.get())

#text_alerte = canvas_alerte.create_text(12, 12, text=i_var.get())
text_batterie = canvas_alerte.create_text(12, 12, text=batterie_var.get())
 
 # fonction d'actualisation
def updateEverySecond():
    global x
    global y
    global z
    
    global vx
    global vy
    global vz
    
    global batterie

    req.codereq = USER_REQ_STATUS

    s.send(req)
    data = s.recv(4096)
    ack = Tmessage.from_buffer_copy(data)
    if (ack.codereq == ACK_USER_REQ_STATUS):
        print("status received\n")
    elif (ack.codereq == ERROR_USER_REQ_STATUS):
        print("Error to received status\n")

    ensembledrone= Tens_drone()    
    ensembledrone=ack.droneList
    
    # positions :
    x =  ensembledrone.drones[0].pos.x               
    x_var.set(str(x))
    y =  ensembledrone.drones[0].pos.y              
    y_var.set(str(y))
    z =  ensembledrone.drones[0].pos.z                
    z_var.set(str(z))
    
    vx =  ensembledrone.drones[0].vitesse.x               
    vx_var.set(str(vx))
    vy =  ensembledrone.drones[0].vitesse.y               
    vy_var.set(str(vy))
    vz =  ensembledrone.drones[0].vitesse.z               
    vz_var.set(str(vz))
    
    batterie =  ensembledrone.drones[0].battery              
    batterie_var.set(str(batterie))
    
    canvas_x.itemconfigure(text_x, text=x_var.get())
    canvas_y.itemconfigure(text_y, text=y_var.get())
    canvas_z.itemconfigure(text_z, text=y_var.get())

    canvas_vx.itemconfigure(text_vx, text=vx_var.get())
    canvas_vy.itemconfigure(text_vy, text=vy_var.get())
    canvas_vz.itemconfigure(text_vz, text=vz_var.get())

    canvas_alerte.itemconfigure(text_batterie, text=batterie_var.get())
    

    window.after(1000, updateEverySecond)

updateEverySecond()

# Affichage
label_pos.pack(padx=3, pady=3)
frame_pos.pack(padx=40, pady=40)
frame_pos.place(x=50,y=100)

label_vit.pack(padx=3, pady=3)
frame_vit.pack(padx=40, pady=40)
frame_vit.place(x=50,y=250)

label_alerte.pack(padx=3, pady=3)
frame_alerte.pack(padx=40, pady=40)
frame_alerte.place(x=50,y=450)

#label_pos.place(x=10,y=10)

# creer un titre
#label_title = Label(right_frame, text="mdp", font=("Arial",20), bg='gray', fg='white' )
#label_title.pack()

# creer un champ/input


# creer un bouton

button_demarrer = Button(window, text="Démarrer \n le drone", font=("Arial",20), bg='gray', fg='white', command=demarrer_drone)
button_demarrer.place(x=570,y=470)

button_arret = Button(window, text="Arrêter \n le drone", font=("Arial",20), bg='gray', fg='white', command=arreter_drone)
button_arret.place(x=750, y=470)

# creation d'une barre de menu
menu_bar = Menu(window)
# creer un premier menu
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Nouveau", command=bjr)
file_menu.add_command(label="Quitter", command=window.quit)
menu_bar.add_cascade(label="Fichier", menu=file_menu)

# configurer notre fenetre pour ajouter le menu bar
window.config(menu=menu_bar)


window.mainloop()


#s.close()


######### DOCUMENTATION #########
# https://docs.python.org/3/library/tkinter.html
# http://tkinter.fdex.eu/ 
