import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage import io, transform
from PIL import Image
import matplotlib.animation as animation


L = 35
H = 40
dh = 5
dl = 5

nl = int(np.ceil(L/dl))
nh = int(np.ceil(H/dh))

img_l = 100
img_h = 100

MAP = np.zeros((img_h*nh,img_l*nl,4)).astype(int) #Array des images recuperés

MAP_CHAINE = np.zeros((nh,nl,2))
#MAP_REPARTITION = np.zeros((nh,nl,2))  # Array de repartition des taches sur la map. La première valeur est le numero du drone affecté, la 2eme à l'ordre dont sont fait les taches par le drone affecté. (-1,-1) si pas encore fait, (-2,-2) si déja fait
#MAP_REPARTITION.fill(-1)


def new_map():
    MAP_CHAINE = np.zeros((nh,nl,2))
    MAP_REPARTITION = np.zeros((nh,nl,2))  # Array de repartition des taches sur la map. La première valeur est le numero du drone affecté, la 2eme à l'ordre dont sont fait les taches par le drone affecté. (-1,-1) si pas encore fait, (-2,-2) si déja fait
    MAP_REPARTITION.fill(-1)
    for k in range(5):
        x = np.random.randint(0,nl)
        y = np.random.randint(0,nh)
        MAP_REPARTITION[y][x] = [-2,-2]
    return(MAP_REPARTITION,MAP_CHAINE)

DRONE_DISPO = [0,1]
n_drone = 4



def pos(nx,ny):
    return((nx*dl+ dl/2,ny*dh + dh/2))

def dist(pos1,pos2):
    return(np.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2))


def afficher(MAP_REPARTITION,all_rectangles): #Affiche les différents rectangles
    IMG = np.zeros((nh,nl)).astype(int)
    for x in range(nl):
        for y in range(nh):
            if(pos_is_in_any_rectangles((x,y),all_rectangles)):
                for k in range(len(all_rectangles)):
                    if(pos_is_in_rectangle((x,y),all_rectangles[k])):
                        IMG[y][x] = (k+1)*100
            else:
                IMG[y][x] = MAP_REPARTITION[y][x][0]*100

    plt.imshow(IMG)
    plt.show()
    return(IMG)


def tiles_a_faire(map_r,all_rectangles): #Renvoie la liste des tiles qui n'ont pas été affecté à un rectangle ou à un drone
    L = []
    for y in range(len(map_r)):
        for x in range(len(map_r[0])):
            if(map_r[y][x][0]==-1 and not pos_is_in_any_rectangles((x,y),all_rectangles)):
                L.append((x,y))
    return(L)


def pos_is_in_rectangle(pos,L_rectangle): #Verrifie si la pos est dans le rectangle
    for y in range(len(L_rectangle)):
        for x in range(len(L_rectangle[0])):
            if(L_rectangle[y][x] == pos):
                return(True)
    return(False)

def pos_is_in_any_rectangles(pos,all_rectangles):  #Verrifie si la pos est dans l'un des rectangles
    return(any([pos_is_in_rectangle(pos,rectangle) for rectangle in all_rectangles]))

def test_aggrandissement_droite(L_rectangle,map_r,other_rectangles):  #Essaie d'elargir si possible le rectangle vers la droite. Renvoie le nouveau rectangle et la direction d'aggrandissement ((0,0) si impossible)
    direction_aggrandissement = (0,0)
    H = len(L_rectangle)
    L = len(L_rectangle[0])
    (x_ori,y_ori) = L_rectangle[0][0]
    if(L+x_ori >= len(map_r[0])):
        return(L_rectangle,(0,0))
    bool = True #Bool qui verrifie si on peut s'étendre à droite
    x_nouvelle_colonne = L + x_ori
    for y_loc in range(H):
        y = y_ori + y_loc
        if(map_r[y][x_nouvelle_colonne][0] != -1 or pos_is_in_any_rectangles((x_nouvelle_colonne,y),other_rectangles)):
            bool = False
            break
    if(bool): #On peut aggrandir à droite, et on le fait
        direction_aggrandissement = (1,0)
        for y_loc in range(H):
            y = y_ori + y_loc
            L_rectangle[y_loc].append((x_nouvelle_colonne,y))
    return(L_rectangle,direction_aggrandissement)


def choix_haut_ou_bas(L_rectangle,map_r,other_rectangles): #Verrifie s'il est plus "interessant" (et possible) de s'étendre en haut ou en bas. On verrifie de quel coté on peut s'étendre le plus (afin de former des grands rectangles)
    direction_aggrandissement = (0,0)
    (x_ori,y_ori) = L_rectangle[0][0]
    H = len(L_rectangle)
    L = len(L_rectangle[0])
    y_max = y_ori + H - 1
    bool_haut = True
    bool_bas = True
    k = 1 #Correspond à la hauteur de ce que l'on souhaite rajouter
    if(y_ori - 1 < 0):
        bool_bas = False
    if(y_max + 1 >= len(map_r)):
        bool_haut = False
    while(bool_haut or bool_bas):
        if(bool_bas):
            for x_loc in range(L):
                x = x_loc + x_ori
                if(map_r[y_ori-k][x][0] != -1):  #Aggrandissement en bas pas possible car zone sans rien à faire
                    bool_bas = False
                if(pos_is_in_any_rectangles((x,y_ori-k),other_rectangles)): #Aggrandissement en bas pas possible car déja affecté à un rectangle
                    bool_bas = False
                if(not bool_bas):
                    if(not bool_haut): #Si le choix haut à déja été eliminé
                        return(k-1,-1)
                    break
        if(bool_haut):
            for x_loc in range(L):
                x = x_loc + x_ori
                if(map_r[y_ori+ H - 1 + k][x][0] != -1):  #Aggrandissement en haut pas possible car zone sans rien à faire
                    bool_haut = False
                if(pos_is_in_any_rectangles((x,y_ori+k),other_rectangles)): #Aggrandissement en haut pas possible car déja affecté à un rectangle
                    bool_haut = False
                if(not bool_haut):
                    if(not bool_bas): #Si le choix haut à déja été eliminé
                        return(k-1,1)
                    break
        k+=1
        if(y_ori - k < 0):
            bool_bas = False
            if(not bool_haut): #Si le choix haut à déja été eliminé
                return(k-1,-1)
        if(y_max + k >= len(map_r)):
            bool_haut = False
            if(not bool_bas): #Si le choix haut à déja été eliminé
                return(k-1,1)
    return(k-1,-1) #Cas où les deux directions sont équivalentes en termes de hauteur max possible





def aggrandir_rectangle(L_rectangle,map_r,other_rectangles):  #Aggrandit le rectangle dans un sens, en essayant de former un carré si possible
    direction_aggrandissement = (0,0)
    H = len(L_rectangle)
    L = len(L_rectangle[0])
    (x_ori,y_ori) = L_rectangle[0][0]
    if(H>=L): #Cas où il y a plus de ligne que de colonne. On essaye donc d'augmenter le nombre de colonnes vers la droite (pas de choix)
        L_rectangle,direction_aggrandissement = test_aggrandissement_droite(L_rectangle,map_r,other_rectangles)
        if(direction_aggrandissement == (1,0)):
            return(L_rectangle,(1,0))
    if(L>H or direction_aggrandissement == (0,0)): #Si L>H ou si le dernier cas à raté. On s'étend en haut ou en bas
        (k,d) = choix_haut_ou_bas(L_rectangle,map_r,other_rectangles)
        if(k!=0):
            direction_aggrandissement = (0,d)
            if(d == 1):
                ligne = []
                for x_loc in range(L):
                    x = x_ori + x_loc
                    ligne.append((x,y_ori + H))
                L_rectangle.append(ligne)
                return(L_rectangle,(0,1))
            else:
                ligne = []
                for x_loc in range(L):
                    x = x_ori + x_loc
                    ligne.append((x,y_ori - 1))
                L_rectangle = ligne + L_rectangle
                return(L_rectangle,(0,-1))
    if(direction_aggrandissement == (0,0)): #Si jamais L>H, mais il est impossible d'aller en haut ou en bas
        L_rectangle,direction_aggrandissement = test_aggrandissement_droite(L_rectangle,map_r,other_rectangles)
        if(direction_aggrandissement == (1,0)):
            return(L_rectangle,(1,0))
    return(L_rectangle,(0,0))


def creation_rectangle(L_rectangle,map_r,other_rectangles):  #Elargis un rectangle déja existant jusqu'a que cela ne soit plus possible
    dir = (1,1)
    while(dir != (0,0)):
        (L_rectangle,dir) = aggrandir_rectangle(L_rectangle,map_r,other_rectangles)
    return(L_rectangle)

def creation_new_rectangle(map_r,all_rectangles = []):  #Créer un nouveau rectangle à la première position disponible, puis l'élargis autant que possible
    pos_init = tiles_a_faire(map_r,all_rectangles)[0]
    new_rectangle = [[pos_init]]
    new_rectangle = creation_rectangle(new_rectangle,map_r,all_rectangles)
    return(new_rectangle)

#Sur un rectangle, il existe toujours 4 chemins possibles qui parcours le traverse intégrallement. Ces 4 possiblités sont définis par la position d'origine (ou de fin) du chemin, et de traversé (2 choix). Il n'y a pas forcement de meilleurs choix si on ne s'interesse qu'au rectangle seul. Néanmoins le principe de l'algorithme est d'étendre les chemins : s'il y a au moins 2 tuiles adjacentes entre elles, et adjacente au coté "long" du chemin. On peut alors étendre le chemin sur ces deux tuiles (cf présentation algo). Il faut donc verrifier de quel coté il y a les plus de potentiel d'ajout de tuiles.

def cote_dispo(rectangle,map_r):
    choice = ["haut","bas","droite","gauche"]
    H = len(rectangle)
    L = len(rectangle[0])
    (x_ori,y_ori) = rectangle[0][0]
    if(x_ori == 0):
        choice.remove("gauche")
    if(y_ori == 0):
        choice.remove("haut")
    if(x_ori + L >= len(map_r[0])):
        choice.remove("droite")
    if(y_ori + H >= len(map_r)):
        choice.remove("bas")
    return(choice)

def hauteur_par_tuile_haut(L_rectangle,map_r,other_rectangles):  #Donne la liste des "hauteurs" sur chaque tuile du coté haut (par hauteur, on entend la distance max avant de rencontrer un obstacle, en partant de cette tuile et en s'éloignant de la paroi)
    H = len(L_rectangle)
    L = len(L_rectangle[0])
    (x_ori,y_ori) = L_rectangle[0][0]
    y_max = y_ori + H - 1
    Liste = []
    for x_loc in range(L):
        bool = True
        k = 1
        x = x_loc + x_ori
        while(bool and y_max + k < len(map_r)):
            if(map_r[y_max + k][x][0] != -1):  #Aggrandissement en haut pas possible car zone sans rien à faire
                bool = False
                break
            if(pos_is_in_any_rectangles((x,y_max +k),other_rectangles)): #Aggrandissement en haut pas possible car déja affecté à un rectangle
                bool = False
                break
            k+= 1
        Liste.append(k-1)
    return(Liste)


def hauteur_par_tuile_bas(L_rectangle,map_r,other_rectangles):
    H = len(L_rectangle)
    L = len(L_rectangle[0])
    (x_ori,y_ori) = L_rectangle[0][0]
    Liste = []
    for x_loc in range(L):
        bool = True
        k = 1
        x = x_loc + x_ori
        while(bool and y_ori - k >= 0):
            if(map_r[y_ori - k][x][0] != -1):  #Aggrandissement en haut pas possible car zone sans rien à faire
                bool = False
                break
            if(pos_is_in_any_rectangles((x,y_ori - k),other_rectangles)): #Aggrandissement en haut pas possible car déja affecté à un rectangle
                bool = False
                break
            k+= 1
        Liste.append(k-1)
    return(Liste)

def hauteur_par_tuile_droite(L_rectangle,map_r,other_rectangles):
    H = len(L_rectangle)
    L = len(L_rectangle[0])
    (x_ori,y_ori) = L_rectangle[0][0]
    x_max = x_ori + L - 1
    Liste = []
    for y_loc in range(H):
        bool = True
        k = 1
        y = y_loc + y_ori
        while(bool and x_max + k < len(map_r[0])):
            if(map_r[y][x_max + k][0] != -1):  #Aggrandissement en haut pas possible car zone sans rien à faire
                bool = False
                break
            if(pos_is_in_any_rectangles((x_max + k,y),other_rectangles)): #Aggrandissement en haut pas possible car déja affecté à un rectangle
                bool = False
                break
            k+= 1
        Liste.append(k-1)
    return(Liste)

def hauteur_par_tuile_gauche(L_rectangle,map_r,other_rectangles):
    H = len(L_rectangle)
    L = len(L_rectangle[0])
    (x_ori,y_ori) = L_rectangle[0][0]
    Liste = []
    for y_loc in range(H):
        bool = True
        k = 1
        y = y_loc + y_ori
        while(bool and x_ori - k >= 0):
            if(map_r[y][x_ori - k][0] != -1):  #Aggrandissement en haut pas possible car zone sans rien à faire
                bool = False
                break
            if(pos_is_in_any_rectangles((x_ori - k,y),other_rectangles)): #Aggrandissement en haut pas possible car déja affecté à un rectangle
                bool = False
                break
            k+= 1
        Liste.append(k-1)
    return(Liste)

def choix_paires(L):  #Dans le cas où le rallongement du chemin se fait par un coté "long", on peut choisir de rallonger le chemin n'importe où, tant que deux cases sont adjacentes. Il y a donc une multitude de choix différents, il faut choisir les bonnes paires de tuiles pour rallonger le chemin. Cette fonction par reccurence compare les choix entre eux et selectionne le meilleurs.
    n = len(L)
    if(n == 0):
        return([],0)
    if(n == 1):
        return([0],0)

    if(len(L) == 2):
        if(L[0] != 0 and L[1] != 0):
            return([1,1],min(L)*2)
        else:
             return([0,0],min(L)*2)
    (choix1,resultat_si_pas_choisis) = choix_paires(L[1:])
    mi = min(L[0],L[1])
    if(mi != 0):
        (choix2,resu) = choix_paires(L[2:])
        resultat_si_choisis = 2*mi + resu
        if(resultat_si_pas_choisis > resultat_si_choisis):
            return([0]+choix1 , resultat_si_pas_choisis)
        else:
            return([1,1]+choix2 , resultat_si_choisis)
    else:
        return([0] + choix1 , resultat_si_pas_choisis)



def choix_paires_imposed_parity(L): #Dans le cas où le rallongement du chemin se fait par le coté "court" (qui serpente), on ne peut pas choisir n'importe quel paires de tuiles adjactentes pour rallonger le chemin. Il faut choisir une paire adjacentes à un virage. Ainsi, on peut juste choisir entre deux choix : l'un où le chemin commence sur le coté opposé (pour avoir des débuts de virages tout les cases paires), et l'inverse. Cette fonction compare les deux choix:
    choix_impaires = 0
    choix_paires = 0
    for k in range(len(L)-1):
        if(k%2 == 0):
            choix_paires += 2*min(L[k],L[k+1])
        else:
            choix_impaires += 2*min(L[k],L[k+1])
    return(choix_paires,choix_impaires)

def estime_et_choix(L_gauche,L_droite,L_haut,L_bas):  #Estime combien de tuile sont "gagné" si on fait le choix d'aller de gauche à droite, et compare aussi pour savoir quelle est la meilleure position d'origine. Cette fonction peut être aussi utilisé par analogie, en inversant gauche et haut, droite et bas
    choix_depart = -1 #0 pour un départ/fin en haut à gauche, 1 pour en haut à droite
    n_sup = 0
    (choice_bas,n) = choix_paires(L_bas)
    n_sup += n
    (choice_haut,n) = choix_paires(L_haut)
    n_sup += n
    (c_gauche_paire,c_gauche_impaire) = choix_paires_imposed_parity(L_gauche)
    (c_droite_paire,c_droite_impaire) = choix_paires_imposed_parity(L_droite)
    n_depart_gauche = c_droite_paire + c_gauche_impaire
    n_depart_droite = c_droite_impaire + c_gauche_paire
    #On ajoute une ligne droite au départ ou à la fin. Il faut choisir de quelle coté part la ligne.
    choice_ligne_depart_droite = [0,0] #0 si la ligne reste dans la longueur, 1 si la ligne fait un angle droit au niveau du départ/arrivé. Le premier terme correspond au départ, et le deuxième à l'arrivée
    if(choice_haut[0] == 0 and  L_haut[0] > L_gauche[0]):
        choice_ligne_depart_droite[0] = 1
        n_depart_droite += L_haut[0]
    else:
        choice_ligne_depart_droite[0] = 0
        n_depart_droite += L_gauche[0]
    if(choice_bas[len(choice_bas)-1] == 0 and  L_bas[len(L_bas)-1] > L_droite[len(L_droite)-1]):
        choice_ligne_depart_droite[1] = 1
        n_depart_droite += L_bas[len(L_bas)-1]
    else:
        choice_ligne_depart_droite[1] = 0
        n_depart_droite += L_droite[len(L_droite)-1]

    choice_ligne_depart_gauche = [0,0] #0 si la ligne reste dans la longueur, 1 si la ligne fait un angle droit au niveau du départ/arrivé. Le premier terme correspond au départ, et le deuxième à l'arrivée
    if(choice_haut[len(L_haut)-1] == 0 and  L_haut[len(L_haut)-1] > L_droite[0]):
        choice_ligne_depart_gauche[0] = 1
        n_depart_gauche += L_haut[len(L_haut)-1]
    else:
        choice_ligne_depart_gauche[0] = 0
        n_depart_gauche += L_droite[0]
    if(choice_bas[0] == 0 and  L_bas[0] > L_gauche[len(L_droite)-1]):
        choice_ligne_depart_gauche[1] = 1
        n_depart_gauche += L_bas[len(L_bas)-1]
    else:
        choice_ligne_depart_gauche[1] = 0
        n_depart_gauche += L_gauche[len(L_gauche)-1]
    if(n_depart_gauche >= n_depart_droite):
        n_sup += n_depart_gauche
        choix_depart = 0
        choice_ligne = choice_ligne_depart_gauche
    else:
        n_sup += n_depart_droite
        choix_depart = 1
        choice_ligne = choice_ligne_depart_droite
    return(n_sup,choix_depart,choice_haut,choice_bas,choice_ligne)


def best_path_in_rectangle(rectangle,map_r,other_rectangles):
    choix_du_parcours = -1 #-1 si pas définis, 0 si en largeur, 1 si en hauteur
    origine = -1 #-1 si pas définis, 0 si l'origine est un point de départ/fin, 1 sinon
    L_droite = hauteur_par_tuile_droite(rectangle,map_r,other_rectangles)
    L_gauche = hauteur_par_tuile_gauche(rectangle,map_r,other_rectangles)
    L_haut = hauteur_par_tuile_haut(rectangle,map_r,other_rectangles)
    L_bas = hauteur_par_tuile_bas(rectangle,map_r,other_rectangles)
    #Premier cas, on choisit de traverser le rectangle de gauche à droite
    (n_sup1,choix_depart1,choix_haut,choix_bas,choice_ligne1) = estime_et_choix(L_gauche,L_droite,L_haut,L_bas)
    #Deuxieme cas, on choisit de traverser le rectangle de haut en bas
    (n_sup2,choix_depart2,choix_gauche,choix_droite,choice_ligne2) = estime_et_choix(L_bas,L_haut,L_gauche,L_droite)
    if(n_sup1 >= n_sup2):
        return(0,choix_depart1,choix_bas,choix_haut,choice_ligne1)
    else:
        return(1,choix_depart2,choix_gauche,choix_droite,choice_ligne2)


def rectangle_to_chain(rectangle,map_chaine,choix_sens,choix_depart):
    H = len(rectangle)
    L = len(rectangle[0])
    (x_ori,y_ori) = rectangle[0][0]
    (x_max,y_max) = (x_ori + L - 1, y_ori + H - 1)
    for x_loc in range(L):
        x = x_loc + x_ori
        for y_loc in range(H):
            y = y_loc + y_ori
            if(choix_sens == 0): #De gauche à droite
                if((x_loc == 0 and y_loc%2 != choix_depart) or (x_loc == L - 1 and y_loc%2 == choix_depart)):
                    map_chaine[y][x] = [0,-1]
                else:
                    if(y_loc%2 == choix_depart):
                        map_chaine[y][x] = [1,0]
                    else:
                        map_chaine[y][x] = [-1,0]
            if(choix_sens == 1): #De haut en bas
                if((y_loc == 0 and x_loc%2 == choix_depart) or (y_loc == H - 1 and x_loc%2 != choix_depart)):
                    map_chaine[y][x] = [1,0]
                else:
                    if(x_loc%2 == choix_depart):
                        map_chaine[y][x] = [0,1]
                    else:
                        map_chaine[y][x] = [0,-1]
    return(map_chaine)

def rectangle_to_chain2(rectangle,map_chaine,choix_sens,choix_depart):
    H = len(rectangle)
    L = len(rectangle[0])
    (x_ori,y_ori) = rectangle[0][0]
    (x_max,y_max) = (x_ori + L - 1, y_ori + H - 1)
    for x_loc2 in range(L):
        x_loc = L-1 - x_loc2
        x = x_loc + x_ori
        for y_loc2 in range(H):
            y_loc = H - 1 - y_loc2
            y = y_loc + y_ori
            if(choix_sens == 0): #De gauche à droite
                if((x_loc == 0 and y_loc%2 == choix_depart) or (x_loc == L - 1 and y_loc%2 != choix_depart)):
                    map_chaine[y][x] = [0,1]
                else:
                    if(y_loc%2 == choix_depart):
                        map_chaine[y][x] = [-1,0]
                    else:
                        map_chaine[y][x] = [1,0]
            if(choix_sens == 1): #De haut en bas
                if((y_loc == 0 and x_loc%2 != choix_depart) or (y_loc == H - 1 and x_loc%2 == choix_depart)):
                    map_chaine[y][x] = [-1,0]
                else:
                    if(x_loc%2 == choix_depart):
                        map_chaine[y][x] = [0,-1]
                    else:
                        map_chaine[y][x] = [0,1]
    return(map_chaine)


fleche_haut =  [[0,0,1,0,0],
                [0,1,1,1,0],
                [1,0,1,0,1],
                [0,0,1,0,0],
                [0,0,1,0,0]]

ligne_haut =  [[0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0]]


def afficher_chaine2(map_chaine,map_repartition = None):
    H = len(map_chaine)
    L = len(map_chaine[0])
    img = np.zeros((6*H,6*L))
    for y in range(H):
        for x in range(L):
            if(map_chaine[y][x].tolist() != [0,0]):
                if(map_chaine[y][x].tolist()  == [0,1]):
                    n_rot = 0
                if(map_chaine[y][x].tolist()  == [-1,0]):
                    n_rot = 1
                if(map_chaine[y][x].tolist()  == [0,-1]):
                    n_rot = 2
                if(map_chaine[y][x].tolist()  == [1,0]):
                    n_rot = 3
                fleche = np.rot90(fleche_haut,n_rot)
                for y1 in range(5):
                    for x1 in range(5):
                        img[6*y+y1][6*x + x1] = fleche[y1][x1]
            if(map_repartition is not None):
                if(map_repartition[y][x].tolist() == [-2,-2]):
                    for y1 in range(5):
                        for x1 in range(5):
                            img[6*y+y1][6*x + x1] = 1

    plt.imshow(img)
    plt.show()

def afficher_chaine(map_chaine,map_repartition = None):
    H = len(map_chaine)
    L = len(map_chaine[0])
    img = np.zeros((6*H,6*L))
    for y in range(H):
        for x in range(L):
            if(map_chaine[y][x].tolist() != [0,0]):
                decalage_y = 0
                decalage_x = 0
                if(map_chaine[y][x].tolist()  == [0,1]):
                    n_rot = 0
                    decalage_y = -3
                if(map_chaine[y][x].tolist()  == [-1,0]):
                    n_rot = 1
                    decalage_x = -3
                if(map_chaine[y][x].tolist()  == [0,-1]):
                    n_rot = 2
                    decalage_y = 3
                if(map_chaine[y][x].tolist()  == [1,0]):
                    n_rot = 3
                    decalage_x = 3
                ligne = np.rot90(ligne_haut,n_rot)
                try:
                    for y1 in range(5):
                        for x1 in range(5):
                            img[6*y+y1+decalage_y][6*x + x1 + decalage_x] = ligne[y1][x1]
                except:
                    n_rot
            if(map_repartition is not None):
                if(map_repartition[y][x].tolist() == [-2,-2]):
                    for y1 in range(5):
                        for x1 in range(5):
                            img[6*y+y1][6*x + x1] = 1

    plt.imshow(img)
    plt.show()


def create_rectangle_pos(x_ori,y_ori,L,H):
    rec = []
    for y in range(H):
        ligne = []
        for x in range(L):
            ligne.append((x_ori+x,y_ori+y))
        rec.append(ligne)
    return(rec)


def add_sides(rectangle,choix_sens,choix_depart,choix_cote1,choix_cote2,choix_ligne,map_r,map_chaine,all_rectangles):
    H = len(rectangle)
    L = len(rectangle[0])
    (x_ori,y_ori) = rectangle[0][0]
    (x_max,y_max) = (x_ori + L - 1, y_ori + H - 1)
    new_rectangles = []
    if(choix_sens == 0): #De gauche à droite
        L_haut = hauteur_par_tuile_haut(rectangle,map_r,all_rectangles)
        L_bas = hauteur_par_tuile_bas(rectangle,map_r,all_rectangles)
        x = 0
        while(x<L-1):
            if(choix_cote2[x] == 1 and min(L_bas[x],L_bas[x+1]) != 0): #en bas
                rec = create_rectangle_pos(x_ori+x,y_ori-min(L_bas[x],L_bas[x+1]),2,min(L_bas[x],L_bas[x+1]))
                if(choix_depart%2 == 0):
                    map_chaine[y_ori][x_ori+x] = [0,1]
                    rectangle_to_chain(rec,map_chaine,1,0)
                    new_rectangles.append((rec,1,0,0))
                    map_chaine[y_ori-1][x_ori+x+1] = [0,-1]
                else:
                    map_chaine[y_ori][x_ori+x+1] = [0,1]
                    rectangle_to_chain2(rec,map_chaine,1,0)
                    new_rectangles.append((rec,1,0,1))
                    map_chaine[y_ori-1][x_ori+x] = [0,-1]
                afficher_chaine(map_chaine,map_r)
                all_rectangles.append(rec)
                x += 2
            else: x+=1
        x = 0
        while(x<L-1):
            if(choix_cote1[x] == 1 and min(L_haut[x],L_haut[x+1]) != 0 ): #En haut
                rec = create_rectangle_pos(x_ori+x,y_max+1,2,min(L_haut[x],L_haut[x+1]))
                all_rectangles.append(rec)
                if((H + choix_depart)%2 == 0):
                    map_chaine[y_max][x_ori+x+1] = [0,-1]
                    rectangle_to_chain2(rec,map_chaine,1,1)
                    new_rectangles.append((rec,1,1,1))
                    map_chaine[y_max+1][x_ori+x] = [0,1]
                else:
                    map_chaine[y_max][x_ori+x] = [0,-1]
                    rectangle_to_chain(rec,map_chaine,1,1)
                    new_rectangles.append((rec,1,1,0))
                    map_chaine[y_max+1][x_ori+x+1] = [0,1]
                x += 2
                afficher_chaine(map_chaine,map_r)
            else: x+=1
    if(choix_sens == 1): #De haut en bas
        L_gauche = hauteur_par_tuile_gauche(rectangle,map_r,all_rectangles)
        L_droite = hauteur_par_tuile_droite(rectangle,map_r,all_rectangles)
        y = 0
        while(y<H-1): #à gauche
            if(choix_cote1[y] == 1 and min(L_gauche[y],L_gauche[y+1]) != 0):
                rec = create_rectangle_pos(x_ori-min(L_gauche[y],L_gauche[y+1]),y_ori+y,min(L_gauche[y],L_gauche[y+1]),2)
                all_rectangles.append(rec)
                if((choix_depart)%2 == 0):
                    map_chaine[y_ori+y+1][x_ori] = [-1,0]
                    rectangle_to_chain2(rec,map_chaine,0,1)
                    new_rectangles.append((rec,0,1,1))
                    map_chaine[y_ori+y][x_ori-1] = [1,0]

                else:
                    map_chaine[y_ori+y][x_ori] = [-1,0]
                    rectangle_to_chain(rec,map_chaine,0,1)
                    new_rectangles.append((rec,0,1,0))
                    map_chaine[y_ori+y+1][x_ori-1] = [1,0]
                afficher_chaine(map_chaine,map_r)
                y += 2
            else: y+=1
        y = 0
        while(y<H-1):
            if(choix_cote2[y] == 1 and min(L_droite[y],L_droite[y+1]) != 0) : #A droite
                rec = create_rectangle_pos(x_max+1,y_ori+y,min(L_droite[y],L_droite[y+1]),2)
                all_rectangles.append(rec)
                if((L + choix_depart)%2 == 1):
                    map_chaine[y_ori+y+1][x_max] = [1,0]
                    rectangle_to_chain2(rec,map_chaine,0,0)
                    new_rectangles.append((rec,0,0,1))
                    map_chaine[y_ori+y][x_max+1] = [-1,0]
                else:
                    map_chaine[y_ori+y][x_max] = [1,0]
                    rectangle_to_chain(rec,map_chaine,0,0)
                    new_rectangles.append((rec,0,0,0))
                    map_chaine[y_ori+y+1][x_max+1] = [-1,0]
                afficher_chaine(map_chaine,map_r)
                y += 2
            else: y+=1
    return(new_rectangles)


def add_sides2(rectangle,choix_sens,choix_depart,choix_cote1,choix_cote2,choix_ligne,map_r,map_chaine,all_rectangles):
    H = len(rectangle)
    L = len(rectangle[0])
    (x_ori,y_ori) = rectangle[0][0]
    (x_max,y_max) = (x_ori + L - 1, y_ori + H - 1)
    new_rectangles = []
    if(choix_sens == 0): #De gauche à droite
        L_gauche = hauteur_par_tuile_gauche(rectangle,map_r,all_rectangles)
        L_droite = hauteur_par_tuile_droite(rectangle,map_r,all_rectangles)
        y = 0
        while(y<H-1):
            if(y%2 != choix_depart): #à gauche
                l = min(L_gauche[y],L_gauche[y+1])
                if(l!=0):
                    rec = create_rectangle_pos(x_ori-l,y_ori + y,l,2)
                    map_chaine[y_ori + y][x_ori] = [-1,0]
                    rectangle_to_chain(rec,map_chaine,0,1)
                    new_rectangles.append((rec,0,0,1))
                    map_chaine[y_ori + y + 1][x_ori - 1] = [1,0]
                    afficher_chaine(map_chaine,map_r)
                    all_rectangles.append(rec)
                y += 2
            else: y+=1
        y = 0
        while(y<H-1):
            if(y%2 == choix_depart): #à droite
                l = min(L_droite[y],L_droite[y+1])
                if(l!=0):
                    rec = create_rectangle_pos(x_max + 1,y_ori + y,l,2)
                    all_rectangles.append(rec)
                    map_chaine[y_ori + y][x_max] = [1,0]
                    rectangle_to_chain(rec,map_chaine,0,0)
                    new_rectangles.append((rec,0,0,0))
                    map_chaine[y_ori + y + 1][x_max + 1] = [-1,0]
                    afficher_chaine(map_chaine,map_r)
                y+=2
            else: y+=1
    if(choix_sens == 1): #De haut en bas
        L_haut = hauteur_par_tuile_haut(rectangle,map_r,all_rectangles)
        L_bas = hauteur_par_tuile_bas(rectangle,map_r,all_rectangles)
        x = 0
        while(x<L-1):
            if(x%2 != choix_depart): #En haut
                h = min(L_haut[x],L_haut[x+1])
                if(h != 0):
                    rec = create_rectangle_pos(x_ori+x,y_max+1,2,h)
                    all_rectangles.append(rec)
                    map_chaine[y_max][x_ori + x] = [0,-1]
                    rectangle_to_chain(rec,map_chaine,1,1)
                    new_rectangles.append((rec,1,1,0))
                    map_chaine[y_max+1][x_ori + x + 1] = [0,1]
                    afficher_chaine(map_chaine,map_r)
                x += 2
            else: x+=1
        x = 0
        while(x<L-1):
            if(x%2 == choix_depart): #En bas
                h = min(L_bas[x],L_bas[x+1])
                if(h!=0):
                    rec = create_rectangle_pos(x_ori + x,y_ori - h,2,h)
                    all_rectangles.append(rec)
                    map_chaine[y_ori][x_ori + x] = [0,-1]
                    rectangle_to_chain2(rec,map_chaine,1,0)
                    new_rectangles.append((rec,1,0,1))
                    map_chaine[y_ori][x_ori + x] = [0,-1]
                    afficher_chaine(map_chaine,map_r)
                x += 2
            else: x+=1
    return(new_rectangles)





def add_ligne(rectangle,choix_sens,choix_depart,choix_cote1,choix_cote2,choix_ligne,map_r,map_chaine,all_rectangles):
    H = len(rectangle)
    L = len(rectangle[0])
    (x_ori,y_ori) = rectangle[0][0]
    (x_max,y_max) = (x_ori + L - 1, y_ori + H - 1)
    new_rectangles = []
    if(L == 1):
        L_gauche = hauteur_par_tuile_gauche(rectangle,map_r,all_rectangles)
        L_droite = hauteur_par_tuile_droite(rectangle,map_r,all_rectangles)
        if(L_droite[0]>=L_gauche[0] and L_droite[0] != 0):
            rec = create_rectangle_pos(x_ori+1,y_ori,L_droite[0],1)
            all_rectangles.append(rec)
            rectangle_to_chain(rec,map_chaine,0,choix_depart)
            new_rectangles.append((rec,0,choix_depart,0))
            if(choix_depart == 0):
                map_chaine[y_ori][x_ori] = [1,0]
            else:
                map_chaine[y_ori][x_ori+1] = [-1,0]
        if(L_droite[0]<L_gauche[0] and L_gauche[0] != 0):
            rec = create_rectangle_pos(x_ori-L_gauche[0],y_ori,L_gauche[0],1)
            all_rectangles.append(rec)
            rectangle_to_chain(rec,map_chaine,0,(choix_depart+1)%2)
            new_rectangles.append((rec,0,(choix_depart+1)%2,0))
            if(choix_depart == 0):
                map_chaine[y_ori][x_ori] = [-1,0]
            else:
                map_chaine[y_ori][x_ori-1] = [1,0]
        afficher_chaine(map_chaine,map_r)


        if(L_droite[H-1]>=L_gauche[H-1] and L_droite[H-1] != 0):
            rec = create_rectangle_pos(x_max+1,y_max,1,L_droite[H-1])
            all_rectangles.append(rec)
            rectangle_to_chain(rec,map_chaine,1,(choix_depart+1)%2)
            new_rectangles.append((rec,1,(choix_depart+1)%2,0))
            if((choix_depart+1)%2 == 0):
                map_chaine[y_max][x_max] = [1,0]
            else:
                map_chaine[y_max][x_max+1] = [-1,0]
        if(L_droite[H-1]<L_gauche[H-1] and L_gauche[H-1] != 0):
            rec = create_rectangle_pos(x_max-L_gauche[H-1],y_max,L_gauche[H-1],1)
            all_rectangles.append(rec)
            rectangle_to_chain(rec,map_chaine,1,choix_depart)
            new_rectangles.append((rec,1,choix_depart,0))
            if(choix_depart == 0):
                map_chaine[y_max][x_max] = [-1,0]
            else:
                map_chaine[y_max][x_max-1] = [1,0]
        afficher_chaine(map_chaine,map_r)
        return(new_rectangles)


    if(H == 1):
        L_haut = hauteur_par_tuile_haut(rectangle,map_r,all_rectangles)
        L_bas = hauteur_par_tuile_bas(rectangle,map_r,all_rectangles)
        if(L_haut[0]>=L_bas[0] and L_haut[0] != 0):
            rec = create_rectangle_pos(x_ori,y_ori+1,1,L_haut[0])
            all_rectangles.append(rec)
            rectangle_to_chain(rec,map_chaine,1,(choix_depart+1)%2)
            new_rectangles.append((rec,1,(choix_depart+1)%2,0))
            if((choix_depart+1)%2 == 0):
                map_chaine[y_ori+1][x_ori] = [0,1]
            else:
                map_chaine[y_ori][x_ori] = [0,-1]
        if(L_haut[0]<L_bas[0] and L_bas[0] != 0):
            rec = create_rectangle_pos(x_ori,y_ori-L_bas[0],1,L_bas[0])
            all_rectangles.append(rec)
            rectangle_to_chain(rec,map_chaine,1,choix_depart)
            new_rectangles.append((rec,1,choix_depart,0))
            if(choix_depart != 0):
                map_chaine[y_ori][x_ori] = [1,0]
            else:
                map_chaine[y_ori+1][x_ori] = [-1,0]
        afficher_chaine(map_chaine,map_r)

        if(L_haut[L-1]>=L_bas[L-1] and L_haut[L-1] != 0):
            rec = create_rectangle_pos(x_max,y_max+1,1,L_haut[L-1])
            all_rectangles.append(rec)
            rectangle_to_chain(rec,map_chaine,1,choix_depart)
            new_rectangles.append((rec,1,choix_depart,0))
            if(choix_depart == 0):
                map_chaine[y_max+1][x_max] = [0,1]
            else:
                map_chaine[y_max][x_max] = [0,-1]
        if(L_haut[L-1]<L_bas[L-1] and L_bas[L-1] != 0):
            rec = create_rectangle_pos(x_max,y_max-L_bas[L-1],1,L_bas[L-1])
            all_rectangles.append(rec)
            rectangle_to_chain(rec,map_chaine,1,(choix_depart+1)%2)
            new_rectangles.append((rec,1,(choix_depart+1)%2,0))
            if((choix_depart+1)%2 != 0):
                map_chaine[y_max][x_max] = [1,0]
            else:
                map_chaine[y_ori+1][x_max] = [-1,0]
        afficher_chaine(map_chaine,map_r)
        return(new_rectangles)


    if((choix_sens == 0 and (choix_depart+H)%2 == 0) or (choix_sens == 1 and (choix_depart + L)%2 == 0)): #Départ en haut à gauche
        if((choix_sens == 0 and choix_ligne[0] == 0) or (choix_sens == 1 and choix_ligne[0] == 1)): #Ligne vers la gauche
            L_gauche = hauteur_par_tuile_gauche(rectangle,map_r,all_rectangles)
            if(L_gauche[0] != 0):
                rec = create_rectangle_pos(x_ori-L_gauche[0],y_ori,1,L_gauche[0])
                all_rectangles.append(rec)
                rectangle_to_chain2(rec,map_chaine,0,0)
                new_rectangles.append((rec,0,0,1))
                map_chaine[x_ori-1][y_ori] = [1,0]
                afficher_chaine(map_chaine,map_r)
        else: #Ligne vers le haut
            L_haut = hauteur_par_tuile_haut(rectangle,map_r,all_rectangles)
            if(L_haut[0] != 0):
                rec = create_rectangle_pos(x_ori,y_max+1,1,L_haut[0])
                all_rectangles.append(rec)
                rectangle_to_chain(rec,map_chaine,1,0)
                new_rectangles.append((rec,1,0,0))
                map_chaine[y_max+1][x_ori] = [0,1]
                afficher_chaine(map_chaine,map_r)
    if((choix_sens == 0 and (choix_depart+H)%2 == 1) or (choix_sens == 1 and (choix_depart + L)%2 == 0)): #Depart/Fin en haut à droite
        if((choix_sens == 0 and choix_ligne[0] == 0) or (choix_sens == 1 and choix_ligne[0] == 1)): #Ligne vers la droite
            L_droite = hauteur_par_tuile_droite(rectangle,map_r,all_rectangles)
            if(L_droite[H-1] != 0):
                rec = create_rectangle_pos(x_max+1,y_max,L_droite[H-1],1)
                all_rectangles.append(rec)
                if(choix_sens == 0): #On change le sens des fleches si besoins
                    rectangle_to_chain(rec,map_chaine,0,0)
                    new_rectangles.append((rec,0,0,0))
                    map_chaine[y_max][x_max] = [1,0]
                else:
                    rectangle_to_chain2(rec,map_chaine,0,0)
                    new_rectangles.append((rec,0,0,1))
                    map_chaine[y_max][x_max] = [-1,0]
                afficher_chaine(map_chaine,map_r)
        else: #Ligne vers le haut
            L_haut = hauteur_par_tuile_haut(rectangle,map_r,all_rectangles)
            if(L_haut[L-1] != 0):
                rec = create_rectangle_pos(x_max,y_max+1,1,L_haut[L-1])
                all_rectangles.append(rec)
                if(choix_sens == 0):
                    rectangle_to_chain(rec,map_chaine,1,1)
                    new_rectangles.append((rec,1,1,0))
                    map_chaine[y_max+1][x_max] = [0,-1]
                    afficher_chaine(map_chaine,map_r)
                else:
                    rectangle_to_chain2(rec,map_chaine,1,0)
                    new_rectangles.append((rec,1,0,1))
                    map_chaine[y_max][x_max] = [0,-1]
                    afficher_chaine(map_chaine,map_r)
    if((choix_sens == 0 and (choix_depart + H)%2 == 0) or (choix_sens == 1 and choix_depart == 1)): #Depart/Fin en bas à gauche
        if((choix_sens == 0 and choix_ligne[1] == 0) or (choix_sens == 1 and choix_ligne[1] == 1)): #Ligne vers la gauche
            L_gauche = hauteur_par_tuile_gauche(rectangle,map_r,all_rectangles)
            if(L_gauche[0] != 0):
                rec = create_rectangle_pos(x_ori-1,y_max,L_gauche[H-1],1)
                all_rectangles.append(rec)
                if(choix_sens == 0): #On change le sens des fleches si besoins
                    rectangle_to_chain(rec,map_chaine,0,0)
                    new_rectangles.append((rec,0,0,0))
                    map_chaine[y_max][x_max+1] = [1,0]
                else:
                    rectangle_to_chain2(rec,map_chaine,0,0)
                    new_rectangles.append((rec,0,0,1))
                    map_chaine[y_max][x_max+1] = [-1,0]
                afficher_chaine(map_chaine,map_r)
        else: #Ligne vers le bas
            L_bas = hauteur_par_tuile_bas(rectangle,map_r,all_rectangles)
            if(L_bas[0] != 0):
                rec = create_rectangle_pos(x_ori,y_max+1,1,L_haut[L-1])
                all_rectangles.append(rec)
                if(choix_sens == 0):
                    rectangle_to_chain(rec,map_chaine,1,0)
                    new_rectangles.append((rec,1,0,0))
                    map_chaine[y_max+1][x_ori] = [0,-1]
                    afficher_chaine(map_chaine,map_r)
                else:
                    rectangle_to_chain2(rec,map_chaine,1,0)
                    new_rectangles.append((rec,1,0,1))
                    map_chaine[y_max+1][x_ori] = [0,-1]
                    afficher_chaine(map_chaine,map_r)
    if((choix_sens == 0 and (choix_depart + H)%2 == 1) or (choix_sens == 1 and (choix_depart + L)%2 == 0)): #Depart/Fin en bas à droite
        if((choix_sens == 0 and choix_ligne[1] == 1) or (choix_sens == 1 and choix_ligne[1] == 1)): #Ligne vers la droite
            L_droite = hauteur_par_tuile_droite(rectangle,map_r,all_rectangles)
            if(L_droite[H-1] != 0):
                rec = create_rectangle_pos(x_max+1,y_max,L_droite[H-1],1)
                all_rectangles.append(rec)
                if(choix_sens == 0): #On change le sens des fleches si besoins
                    rectangle_to_chain(rec,map_chaine,0,0)
                    new_rectangles.append((rec,0,0,0))
                    map_chaine[y_max][x_max] = [1,0]
                else:
                    rectangle_to_chain2(rec,map_chaine,0,0)
                    new_rectangles.append((rec,0,0,1))
                    map_chaine[y_max][x_max+1] = [-1,0]
                afficher_chaine2(map_chaine,map_r)
        else: #Ligne vers le bas
            L_bas = hauteur_par_tuile_haut(rectangle,map_r,all_rectangles)
            if(L_bas[L-1] != 0):
                rec = create_rectangle_pos(x_max,y_max+1,1,L_bas[L-1])
                all_rectangles.append(rec)
                if(choix_sens == 0):
                    rectangle_to_chain(rec,map_chaine,1,0)
                    new_rectangles.append((rec,1,0,0))
                    map_chaine[y_max+1][x_ori] = [0,-1]
                    afficher_chaine(map_chaine,map_r)
                else:
                    rectangle_to_chain2(rec,map_chaine,1,0)
                    new_rectangles.append((rec,1,0,1))
                    map_chaine[y_max][x_max] = [0,-1]
                    afficher_chaine(map_chaine,map_r)
    return(new_rectangles)

def create_new_chain(map_r,map_chaine,all_rectangles = []):
    rectangle = creation_new_rectangle(map_r,all_rectangles)
    H = len(rectangle)
    L = len(rectangle[0])
    (x_ori,y_ori) = rectangle[0][0]
    (x_max,y_max) = (x_ori + L - 1, y_ori + H - 1)
    (choix_sens,choix_depart,choix_cote1,choix_cote2,choix_ligne) = best_path_in_rectangle(rectangle,map_r,all_rectangles)
    map_chaine = rectangle_to_chain(rectangle,map_chaine,choix_sens,choix_depart)
    afficher_chaine(map_chaine,map_r)
    all_rectangles.append(rectangle)
    new_rectangles = add_sides(rectangle,choix_sens,choix_depart,choix_cote2,choix_cote1,choix_ligne,map_r,map_chaine,all_rectangles)
    new_rectangles = new_rectangles + add_sides2(rectangle,choix_sens,choix_depart,choix_cote1,choix_cote2,choix_ligne,map_r,map_chaine,all_rectangles)
    new_rectangles = new_rectangles + add_ligne(rectangle,choix_sens,choix_depart,choix_cote1,choix_cote2,choix_ligne,map_r,map_chaine,all_rectangles)
    while(new_rectangles != []):
        (rec,sens_rec,depart_rec,sens_parcours) = new_rectangles.pop(0)
        depart_rec = (depart_rec + sens_parcours)%2
        if(sens_rec == 0): #De gauche à droite
            L_1 = hauteur_par_tuile_haut(rec,map_r,all_rectangles)
            L_2 = hauteur_par_tuile_bas(rec,map_r,all_rectangles)
            h = len(L_1)
            l = len(rec)
            choix_cote1 = choix_paires(L_1)[0]
            choix_cote2 = choix_paires(L_2)[0]
            (choix_cote1_paire,choix_cote1_impaire) = choix_paires_imposed_parity(L_1)
            (choix_cote2_paire,choix_cote2_impaire) = choix_paires_imposed_parity(L_2)

        else: #De haut en bas
            L_1 = hauteur_par_tuile_gauche(rec,map_r,all_rectangles)
            L_2 = hauteur_par_tuile_droite(rec,map_r,all_rectangles)
            h = len(L_1)
            l = len(rec[0])
            (choix_cote1_paire,choix_cote1_impaire) = choix_paires_imposed_parity(L_1)
            (choix_cote2_paire,choix_cote2_impaire) = choix_paires_imposed_parity(L_2)
            choix_cote1 = choix_paires(L_1)[0]
            choix_cote2 = choix_paires(L_2)[0]
        if(l == 1): #Dans ce cas, on fait le choix entre étendre d'un coté ou de l'autre (alternant)
            n_1 = choix_cote1_paire + choix_cote2_impaire
            n_2 = choix_cote1_impaire + choix_cote2_paire
            if(n_1 >= n_2):
                choix_cote1 = [1 if (k%2 == 0 and min(L_1[k],L_1[k+1]) != 0) else 0 for k in range(h-1)]
                choix_cote2 = [1 if (k%2 != 0 and min(L_2[k],L_2[k+1]) != 0) else 0 for k in range(h-1)]

            else:
                choix_cote1 = [1 if (k%2 != 0 and min(L_1[k],L_1[k+1]) != 0) else 0 for k in range(h-1)]
                choix_cote2 = [1 if (k%2 == 0 and min(L_2[k],L_2[k+1]) != 0) else 0 for k in range(h-1)]
        choix_cote1.append(0)
        choix_cote2.append(0)
        new_rectangles = new_rectangles + add_sides(rec,sens_rec,depart_rec,choix_cote1,choix_cote2,[0,0],map_r,map_chaine,all_rectangles)
        if(l == 1):
            new_rectangles = new_rectangles + add_ligne(rec,sens_rec,depart_rec,choix_cote1,choix_cote2,[0,0],map_r,map_chaine,all_rectangles)
    return(all_rectangles)



def cherche_debut_fin(all_rectangles,map_chaine):
    D = []
    for rec in all_rectangles:
        if(len(rec) == 1 or len(rec[0]) == 1):
            H = len(rec)
            L = len(rec[0])
            (x_ori,y_ori) = rectangle[0][0]
            (x_max,y_max) = (x_ori + L - 1, y_ori + H - 1)
            x = x_ori
            y = y_ori
            L = [(x,y)]
            while(L[len(L)-1] not in L[:(len(L)-1)] and map_chaine[y][x].tolist() != [0,0] and map_chaine[y][x].tolist() != [-1,-1]and (x,y) != (x_max,y_max)):
                (dx,dy) = map_chaine[y][x]
                x += dx
                y += dy
                if(x < 0 or y < 0 or y >=  len(map_chaine) or x >= len(map_chaine[0])):
                    break
                L.append((x,y))
            if((x,y) == (x_max,y_max)):
                map_chaine[y_ori][x_ori] = [-1,-1]
                D.append((x_max,y_max))
            else:
                x = x_max
                y = y_max
                L = [(x,y)]
                while(L[len(L)-1] not in L[:(len(L)-1)] and map_chaine[y][x].tolist() != [0,0] and map_chaine[y][x].tolist() != [-1,-1]and (x,y) != (x_ori,y_ori)):
                    (dx,dy) = map_chaine[y][x]
                    x += dx
                    y += dy
                    if(x < 0 or y < 0 or y >=  len(map_chaine) or x >= len(map_chaine[0])):
                        break
                    L.append((x,y))
                if((x,y) == (x_ori,y_ori)):
                    map_chaine[y_ori][x_ori] = [-1,-1]
                    D.append((x_max,y_max))
    return(D)


all_rectangles = []















