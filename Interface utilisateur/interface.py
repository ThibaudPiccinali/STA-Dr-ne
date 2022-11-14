from tkinter import *
import webbrowser

def open_web_page():
    webbrowser.open_new=("adresse de la page")
# créer une première fenetre 
window = Tk()

#personnaliser la fenetre
window.title("My Application")
window.geometry("480x360") # taille fenetre
window.minsize(480, 360) # definir une taille minimal
window.iconbitmap("STA-Dr-ne\Interface utilisateur\Bienvenue.ico") # mettre un logo à la fenêtre
window.config(background='gray') # on peut mettre le code hexadecimal

#creer la frame
frame = Frame(window, bg='gray', bd=1, relief=SUNKEN)

# ajout d'un composant
label_title = Label(window, text="Bienvenue", font=("Arial",40), bg='gray', fg='black')
label_title.pack() # afficher texte et mettre au centre

label_subtitle = Label(window, text="Coucou", font=("Arial",25), bg='gray', fg='black')
label_subtitle.pack() # afficher texte et mettre au centre

# ajout d'un bouton
button = Button(frame, text="Demarrer drone", font=("Arial",25), bg='white', fg='green', command=open_web_page)
button.pack(pady=25, fill=X)

frame.pack(expand=YES)



# afficher la fenetre
window.mainloop()
