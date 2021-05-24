# Explication du programme:
Alors nous avons ici un programme qui nous permet de générer des terrains de manière 'aléatoire'
Et d'y positionner un personnage que nous allons pouvoir 
faire bouger à l'aide des flêches directionnelles du clavier.
Le personnage ne peux pas apparaitre sur de l'eau et ne peut pas y aller.
On peut sauvegarder ces terrains et les charger à notre guise.
Les case d'eau sont représenté en bleu et les case de terre en gris

un clique sur le terrain créer le personnage si le clique n'est pas sur une case d'eau
Bouton 'Génerer map': génère un nouveau terrain
Bouton 'Supprimer map': Supprime le terrain de l'écran
(Attention ça supprimera la map de l'écran mais pas de vos fichier il faudra le faire manuellement,
 s'il provient d'une sauvegarde)
Bouton 'Paramètres': Ouvre la fenetre de modification des paramètre de génération de terrain
Ceci vas nous ouvrir une fenêtre qui nous permet de modifier les paramètre de génération du terrain
Les paramètre en question:
(
Taille: pour la longueur des côtés du terrain en blocs
p: la probabilitée qu'une case soit de l'eau à l'origine
n: le nombre de répétition de l'automate
k: L'ordre du voisinage de Moore
T: Le comparateur au voisinage de moore ( si la valeur du voisinage est supérieure ou égale à T,
alors une case reste ou est convertie en eau)
)
On clique sur 'Valider' une fois les paramètres entré sinon il ne sont pas prit en compte.
Bouton 'Annuler dernier déplacement': Pour annuler le dernier déplacement du personnage lorqu'il y en a un
Bouton 'Sauvegarder map': Sauvegarde la map dans un fichier au format csv sous le nom qu'on lui donne
Bouton 'Charger map': Charge un map à l'aide du fichier csv choisit générer par le programme au préalable
