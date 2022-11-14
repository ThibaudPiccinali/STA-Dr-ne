import string
from random import randint, choice
from tkinter import *

def generate_password():
    password_min = 6
    password_max = 12
    all_chars = string.ascii_letters + string.punctuation + string.digits
    password = "".join(choice(all_chars) for x in range(randint(password_min, password_max)))
    password_entry.delete(0, END)
    password_entry.insert(0, password)    

# creer la fenetre
window = Tk()
window.title("Controle des drones")
window.geometry("980x760")
window.config(background="gray")

# creer la frame principale
#frame = Frame(window, bg='gray')
#frame.pack(side=MIDDLE)

# creation image 
width=300
height=300
image = PhotoImage(file="STA-Dr-ne\Interface utilisateur\camera.png").zoom(25).subsample(40) # Attention obligatoirement en png
canvas = Canvas(window, width=width+100, height=height+10, bg='gray', bd=0, highlightthickness=0)
canvas.create_image(width/2, height/2, image=image)
canvas.place(x=350,y=100)

image_bat = PhotoImage(file="STA-Dr-ne\Interface utilisateur\catterie.png").zoom(3) # Attention obligatoirement en png
canvas_bat = Canvas(window, width=100, height=100, bg='gray', bd=0, highlightthickness=0)
canvas_bat.create_image(50, 50, image=image_bat)
canvas_bat.place(x=800,y=20)

frame_pos= Frame(window, bg='black', width=500, height=100)
label_pos = Label(frame_pos, text="Position  \n x : \n y : \n z : \n ", font=("Arial",16), bd=0, bg='white', fg='black' )

pos_x = Entry(frame_pos, font=("Arial",16), bg='white', fg='black')
pos_x.pack()
pos_x.place(x=60,y=30, width=20, height=20)
pos_y = Entry(frame_pos, font=("Arial",16), bg='white', fg='black')
pos_y.pack()
pos_y.place(x=60,y=55, width=20, height=20)
pos_z = Entry(frame_pos, font=("Arial",16), bg='white', fg='black')
pos_z.pack()
pos_z.place(x=60,y=80, width=20, height=20)

label_pos.pack(padx=3, pady=3)
frame_pos.pack(padx=40, pady=40)
frame_pos.place(x=50,y=100)

# Fenêtre vitesse
frame_vit= Frame(window, bg='black', width=500, height=100)
label_vit = Label(frame_vit, text="Vitesse    \n x : \n y : \n z : \n", font=("Arial",16), bd=0, bg='white', fg='black' )

vit_x = Entry(frame_vit, font=("Arial",16), bg='white', fg='black')
vit_x.pack()
vit_x.place(x=65,y=30, width=20, height=20)
vit_y = Entry(frame_vit, font=("Arial",16), bg='white', fg='black')
vit_y.pack()
vit_y.place(x=65,y=55, width=20, height=20)
vit_z = Entry(frame_vit, font=("Arial",16), bg='white', fg='black')
vit_z.pack()
vit_z.place(x=65,y=80, width=20, height=20)

label_vit.pack(padx=3, pady=3)
frame_vit.pack(padx=40, pady=40)
frame_vit.place(x=50,y=250)

# Fenêtre messages d'alerte
frame_alerte= Frame(window, bg='black', width=500, height=100)
label_alerte = Label(frame_alerte, text=" Message d'alerte des drones :  \n \n \n ", font=("Arial",16), bd=0, bg='white', fg='black' )
alerte = Entry(frame_alerte, font=("Arial",16), bg='gray', fg='green')
alerte.pack()
alerte.place(x=10,y=30, width=260, height=50)

label_alerte.pack(padx=3, pady=3)
frame_alerte.pack(padx=40, pady=40)
frame_alerte.place(x=50,y=450)

#label_pos.place(x=10,y=10)

# creer un titre
#label_title = Label(right_frame, text="mdp", font=("Arial",20), bg='gray', fg='white' )
#label_title.pack()

# creer un champ/input


# creer un bouton

button_demarrer = Button(window, text="Démarrer \n le drone", font=("Arial",20), bg='gray', fg='white', command=generate_password )
button_demarrer.place(x=570,y=470)

button_arret = Button(window, text="Arrêter \n le drone", font=("Arial",20), bg='gray', fg='white', command=generate_password )
button_arret.place(x=750, y=470)

''' left_frame.grid(row=6, column=6, padx=20)


label_vit = Label(window, text="Vitesse \n x : \n y : \n z : ", font=("Arial",20), bd=0, bg='white', fg='black' )
label_vit.pack(padx=1, pady=1)
label_vit.place(x=10,y=150)

# afficher la frame
frame.pack(expand=YES) '''

# creation d'une barre de menu
menu_bar = Menu(window)
# creer un premier menu
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Nouveau", command=generate_password)
file_menu.add_command(label="Quitter", command=window.quit)
menu_bar.add_cascade(label="Fichier", menu=file_menu)

# configurer notre fenetre pour ajouter le menu bar
window.config(menu=menu_bar)

window.mainloop()


######### DOCUMENTATION #########
# https://docs.python.org/3/library/tkinter.html
# http://tkinter.fdex.eu/ 
