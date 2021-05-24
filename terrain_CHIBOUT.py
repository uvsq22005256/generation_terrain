# MPCI TD06
# groupe: CHIBOUT CLAUDE
# Lien git: https://github.com/uvsq22005256/generation_terrain

# Explication du programme:
# Alors nous avons ici un programme qui nous permet de générer des terrains de manière 'aléatoire'
# Et d'y positionner un personnage que nous allons pouvoir 
# faire bouger à l'aide des flêches directionnelles du clavier.
# Le personnage ne peux pas apparaitre sur de l'eau et ne peut pas y aller.
# De sauvegarder ces terrains et de les charger à notre guise.
# Les case d'eau sont représenté en bleu et les case de terre en gris
# 
# clique sur le terrain créer le personnage si le clique n'est pas sur une case d'eau
# Bouton 'Génerer map': génère un nouveau terrain
# Bouton 'Supprimer map': Supprime le terrain de l'écran
# (Attention ça supprimera la map de l'écran mais pas de vos fichier il faudra le faire manuellement,
#  s'il provient d'une sauvegarde)
# Bouton 'Paramètres': Ouvre la fenetre de modification des paramètre de génération de terrain
# Ceci vas nous ouvrir une fenêtre qui nous permet de modifier les paramètre de génération du terrain
# Les paramètre en question:
# (
# Taille: pour la longueur des côtés du terrain en blocs
# p: la probabilitée qu'une case soit de l'eau à l'origine
# n: le nombre de répétition de l'automate
# k: L'ordre du voisinage de Moore
# T: Le comparateur au voisinage de moore ( si la valeur du voisinage est supérieure ou égale à T,
# alors une case reste ou est convertie en eau)
# )
# On clique sur 'Valider' une fois les paramètres entré sinon il ne sont pas prit en compte.
# Bouton 'Annuler dernier déplacement': Pour annuler le dernier déplacement du personnage lorqu'il y en a un
# Bouton 'Sauvegarder map': Sauvegarde la map dans un fichier au format csv sous le nom qu'on lui donne
# Bouton 'Charger map': Charge un map à l'aide du fichier csv choisit générer par le programme au préalable


# Les imports
import tkinter as tk
import random
from math import floor
from tkinter.filedialog import asksaveasfilename
import csv


# CONSTANTES
block = ["Eau", "Terre"]
block_color = ["Blue", "gray"]
taille_case = 10

# Variables
length = 50
p = 0.5
n = 4
T = 5
k = 1
perso = None
perso_coord = [0, 0]
persoAlive = False
perso_hist_pos = [] #contient: '[v0, v1],..' avec v0 qui prend (0,1)<=>(x,y) et v1 qui prend (0,1)<=>(-,+)

save_grille = []


def createPerso(pos):
    """
    On créer le personnage et affectons les valeurs des variables du personnage
    Evidemment ceci n'est possible que s'il n'éxiste aucun personnage sur le terrain
    """
    global persoAlive, perso, perso_coord
    if persoAlive: return
    pos = [floor(pos.x/taille_case), floor(pos.y/taille_case)]
    c = canvas.itemcget(items[pos[1]][pos[0]], "fill")
    print(c)
    if c == block_color[0]:
        print("Aie")
        return
    perso = canvas.create_rectangle(taille_case*pos[0],
                            taille_case*pos[1],
                            taille_case*pos[0]+taille_case,
                            taille_case*pos[1]+taille_case,
                            fill="red")

    perso_coord = pos
    persoAlive = True


def deletePerso():
    """
    Suppressions du perso, reset des variables du perso
    """
    global persoAlive, perso, perso_hist_pos
    if not persoAlive: return
    canvas.delete(perso)
    perso_coord = [0, 0]
    perso = None
    persoAlive = False
    perso_hist_pos = []


def movePerso(event):
    """
    Traitement de la demande de déplacement du perso
    """
    global persoAlive, perso, perso_coord
    if not persoAlive: return
    if event.keysym == "Up" and perso_coord[1] != 0:
        try:
            c = canvas.itemcget(items[perso_coord[1]-1][perso_coord[0]], "fill")
            if c == block_color[1]:
                perso_coord[1] -= 1
                canvas.move(perso, 0, -taille_case)
                perso_hist_pos.append([1, 0])
        except:
            pass
    elif event.keysym == "Down":
        try:
            c = canvas.itemcget(items[perso_coord[1]+1][perso_coord[0]], "fill")
            if c == block_color[1]:
                perso_coord[1] += 1
                canvas.move(perso, 0, taille_case)
                perso_hist_pos.append([1, 1])
        except:
            pass
    elif event.keysym == "Left" and perso_coord[0] != 0:
        try:
            c = canvas.itemcget(items[perso_coord[1]][perso_coord[0]-1], "fill")
            if c == block_color[1]:
                perso_coord[0] -= 1
                canvas.move(perso, -taille_case, 0)
                perso_hist_pos.append([0, 0])
        except:
            pass
    elif event.keysym == "Right":
        try:
            c = canvas.itemcget(items[perso_coord[1]][perso_coord[0]+1], "fill")
            if c == block_color[1]:
                perso_coord[0] += 1
                canvas.move(perso, taille_case, 0)
                perso_hist_pos.append([0, 1])
        except:
            pass


def undoPersoPosition():
    """
    Annulation du dernier déplacement du perso
    """
    global perso_coord
    if not persoAlive: return
    try:
        dep = perso_hist_pos[-1]
    except:
        return
    if dep[0] == 0: # si x
        if dep[1] == 0: # si -
            perso_coord[0] += 1
            canvas.move(perso, taille_case, 0)
        else:# si +
            perso_coord[0] -= 1
            canvas.move(perso, -taille_case, 0)

    else: # si y
        if dep[1] == 0: # si -
            perso_coord[1] += 1
            canvas.move(perso, 0, taille_case)
        else:# si +
            perso_coord[1] -= 1
            canvas.move(perso, 0, -taille_case)
    perso_hist_pos.pop(-1)


def createGrille():
    """
    création de la grille de base contenant de manière aléatoire des 0 et des 1
    """
    # 0 -- Eau et 1 -- Terre
    grille = [
    [
        0 if random.random() < p else 1 for i in range(length)
        ] for i in range(length)
    ]
    return showGrille(runAutomate(grille))


def showGrille(grille):
    """
    Affiche la grille sur l'écrans
    """
    grille_items = [
        [
            canvas.create_rectangle(x*taille_case, y*taille_case, x*taille_case+taille_case,
                                    y*taille_case+taille_case,
                                    fill=block_color[grille[y][x]])
            for x in range(length)
        ] for y in range(length)
    ]
    canvas.config(width=(length * taille_case), height=(length * taille_case))

    return grille_items


def runAutomate(grille):
    """
    Renvoie le résultat de l'application de l'automate n fois sur la grille donnée
    """
    global save_grille
    #On répete l'automate n fois
    for etape in range(n):
        newgrille = [
            [
                0 for v in range(length)
            ] for i in range(length)
        ]
        grille_voisin = getVoisinageGrille(grille)
        for y, row in enumerate(grille):
            for x, col in enumerate(row):
                if grille_voisin[y][x] >= T:
                    newgrille[y][x] = 0
                else:
                    newgrille[y][x] = 1
        grille = newgrille
    save_grille = grille
    return grille


def getVoisinageGrille(grille):
    """
        Fonction qui nous permet d'obtenir le tableau du nombre
        de voisins de chaque case.
        return un tableau à deux dimension de la taille de la grille
    """
    voisinage_grille = [
        [
            0 for i in range(length)
        ] for i in range(length)
    ]
    for y, row in enumerate(grille):
        for x, col in enumerate(row):
            # 0,0,0
            # 0,x,0
            # 0,0,0
            for i in range(k*2+1):
                for v in range(k*2+1):
                    try:
                        if grille[y-k+i][x-k+v] == 0 and not (y-k+i == y and x-k+v == x):
                            voisinage_grille[y][x] += 1
                    except:
                        pass
                # try:
                    # if grille[y-1+i][x] == 0 and y-1+i != y:
                        # voisinage_grille[y][x] += 1
                # except:
                    # pass
                # try:
                    # if grille[y-1+i][x+1] == 0 and not y-1+i == y:
                        # voisinage_grille[y][x] += 1
                # except:
                    # pass
    #print(voisinage_grille)
    return voisinage_grille


def deleteGrille():
    """
    On supprime la grille
    """
    global items
    deletePerso()
    for row in items:
        for item in row:
            canvas.delete(item)
    items = []


def genNewMap():
    """
    génération d'un nouveau terrain
    """
    global items
    deleteGrille()
    deletePerso()
    items = createGrille()


def openParamWindow():
    """
    Ouvre la fenetre de modification des paramètre de la génération de terrain
    """

    def set_param(box, val):
        box.delete(0, len(box.get()))
        box.insert(0, val)


    def validate_information():
        global p, k, n, T, length
        p = float(p_spin.get())
        n = int(n_spin.get())
        T = int(T_spin.get())
        k = int(k_spin.get())
        length = int(length_spin.get())
        param_window.destroy()


    global p, k, n, T, length
    param_window = tk.Toplevel(root)
    param_window.lift()
    p_spin = tk.Spinbox(param_window, from_=0, to=1, increment=0.1)
    p_spin.grid(row=1, column=1, padx=(0, 20))
    set_param(p_spin, p)
    p_label = tk.Label(param_window, text="p:")
    p_label.grid(row=1, column=0)
    n_spin = tk.Spinbox(param_window, from_=0, to=9999, increment=1)
    n_spin.grid(row=2, column=1, padx=(0, 20))
    set_param(n_spin, n)
    n_label = tk.Label(param_window, text="n:")
    n_label.grid(row=2, column=0)
    k_spin = tk.Spinbox(param_window, from_=0, to=9999, increment=1)
    k_spin.grid(row=3, column=1, padx=(0, 20))
    set_param(k_spin, k)
    k_label = tk.Label(param_window, text="k:")
    k_label.grid(row=3, column=0)
    T_spin = tk.Spinbox(param_window, from_=0, to=9999, increment=1)
    T_spin.grid(row=4, column=1, padx=(0, 20))
    set_param(T_spin, T)
    T_label = tk.Label(param_window, text="T:")
    T_label.grid(row=4, column=0)
    length_spin = tk.Spinbox(param_window, from_=0, to=9999, increment=1)
    length_spin.grid(row=0, column=1, pady=(20,0), padx=(0, 20))
    set_param(length_spin, length)
    length_label = tk.Label(param_window, text="Taille:")
    length_label.grid(row=0, column=0, pady=(20,0), padx=(20, 0))
    valider = tk.Button(param_window, text="Valider", command=validate_information)
    valider.grid(row=5, column=0, columnspan=2, pady=(0, 20))
    param_window.mainloop()


# Fonctions liées à la sauvegarde.

def saveMap():
    """Fonction qui nous permet de sauvegarder la map actuelle dans un fichier
    csv nommé par l'utilisateur"""
    save_path = tk.filedialog.asksaveasfilename()
    if save_path == "": 
        raise Exception("Pas de nom donné")

    # On créer et ouvre en écriture un fichier csv
    with open(save_path+".csv", "w", newline='') as f:
        writer = csv.writer(f)

        # on enregistre les paramètres de la map
        map_param = [length, p, n, T, k]
        writer.writerow(map_param)

        #On enregistre les paramètres du joueur
        player_param = [persoAlive, perso_coord, perso_hist_pos]
        writer.writerow(player_param)

        # on enregistre à l'intérrieur du fichier csv la grille
        for row in save_grille:
            writer.writerow(row)


def loadMap():
    """Fonction qui nous permet de charger une map depuis un fichier
    csv générer par le programme lors d'une sauvegarde"""
    global items, save_grille, length, p, n, T, k, persoAlive, perso_coord, perso_hist_pos, perso
    save_path = tk.filedialog.askopenfilename()
    with open(save_path, "r") as f:
        reader = list(csv.reader(f))
        
        # On supprime la grille actuelle
        deleteGrille()

        # On récupère les paramètres de la map
        map_param = [int(i) if float(i).is_integer() else float(i) for i in reader[0]]
        length, p, n, T, k = map_param

        # On récupère les paramètres du joueur
        player_param = reader[1]
        if player_param[0] == "True":
            player_param[0] = True
        else:
            player_param[0] = False
        player_param[1] = [int(x) for x in player_param[1][1:-1].split(", ")]
        if player_param[2] != '[]':
            player_param[2] = [
                [
                    int(b) for b in x[1:].split(", ")
                ] for x in player_param[2][1:-2].split("], ")
            ]
        else:
            player_param[2] = []
        persoAlive, perso_coord, perso_hist_pos = player_param[0], player_param[1], player_param[2]

        # On récupère la grille
        save_grille = [
            [
                int(x) for x in row
            ] for row in reader[2:]
        ]

    # On dessine la grille chargé
    items = showGrille(save_grille)
    # On affiche le personnage
    if persoAlive:
        perso = canvas.create_rectangle(taille_case*perso_coord[0],
                                        taille_case*perso_coord[1],
                                        taille_case*perso_coord[0]+taille_case,
                                        taille_case*perso_coord[1]+taille_case,
                                        fill="red")

        


root = tk.Tk()
root.resizable(width=False, height=True)
canvas = tk.Canvas(root, width=(length * taille_case),
                   height=(length * taille_case), bg="Black")
canvas.grid(row=0, column=1, rowspan=7)
canvas.bind("<Button-1>", createPerso)
canvas.bind("<1>", canvas.focus_set())
canvas.bind('<KeyPress>', movePerso)
items = createGrille()
param_button = tk.Button(text="Paramètres", command=openParamWindow)
param_button.grid(row=2, column=0)
gen_button = tk.Button(text="Supprimer map", command=deleteGrille)
gen_button.grid(row=1, column=0)
gen_button = tk.Button(text="Générer map", command=genNewMap)
gen_button.grid(row=0, column=0)

delete_perso_button = tk.Button(text="Supprimer le perso", command = deletePerso)
delete_perso_button.grid(row = 3, column = 0)
undo_perso_position_button = tk.Button(text="Annuler dernier déplacement", command = undoPersoPosition)
undo_perso_position_button.grid(row = 4, column = 0)

save_button = tk.Button(text="Sauvegarder map", command=saveMap)
save_button.grid(row=5, column=0)
load_button = tk.Button(text="Charger map", command=loadMap)
load_button.grid(row=6, column=0)

root.mainloop()
