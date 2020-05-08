from random import randrange

import pygame
from pygame.locals import *
pygame.init()

#Déclarations de tous les sons 
erreur_song = pygame.mixer.Sound("sons/erreur.wav")
success_song = pygame.mixer.Sound("sons/reussite.wav")
deja_in_song = pygame.mixer.Sound("sons/deja_in.wav")
quit_song = pygame.mixer.Sound("sons/quit.wav")


#Renvoie tous les mots d'une liste de mots sous forme de liste
def get_list_mot_from_file(langue='francais'):
	t = "liste_mots/{}.txt".format(langue)
	f = open(t, "r")
	return [i for i in f]

#Vérifie si un mot est dans une liste de mots
def verify_in_file(mot,langue='francais'):
	mot= mot+"\n"
	l=get_list_mot_from_file()
	return mot in l

#Obtenir un mot au  hasard
def get_random_mot(langue='francais'):
	l=get_list_mot_from_file(langue)
	return l[randrange(len(l))]


LETTRES = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r', 's', 't', 'u', 'v','w','x','y', 'z' ]

#Comme pour un scrabble chaque lettre est associée a un nombre de point
LETTRES_POINTS =  {'a': 1,
	               'b': 2,
	               'c': 3,
	               'd': 4,
	               'e': 5,
	               'f': 6,
	               'g': 7,
	               'h': 8,
	               'i': 9,
	               'l': 1,
	               'm': 2,
	               'n': 3,
	               'o': 4,
	               'p': 5,
	               'q': 6,
	               'r': 7,
	               's': 8,
	               't': 9,
	               'u': 1,
	               'v': 2,
	               'z': 3,
	               'x': 4}

#Permet d'obtenir le total de point a partir d'une chaine grace aux valeurs des différentes lettres
#qui la constitue
def get_points_from_chaine(chaine):
	result =0
	for i in chaine:
		result += LETTRES_POINTS[i]
	return result




#Un graphe qui représente les differents sommets avec leur voisin
#C'est très important car il faut voir notre grille de case comme étant une matrice
#Chaque case de la matrice a une ligne et une colonne
# (1,1) correspond à la ligne 1 colonne 1
#VOICI LA GRILLE REPRESENTE SOUS FORME DE MATRICE (C'est l'élément le plus fondamental du programme)
"""
	1,2,3,4
	5,6,7,8
	9,10,11,12
   13,14,15,16
"""
"""
Apres comprehension de la representation précédente , on se rend compte que chaque point a ses voisins 
par exemple : 
si je suis sur 1 je peux acceder à 2,5,6
Si je suis sur 2 je peux acceder à 1,5,6,7,3  ainsi de suite pour chaque sommet

je peux pas être sur 1 et sauter pour atteindre 11 par exemple
je peux pas être sur 9 et sauter pour atteindre 15 par exemple
"""
#Biensur il faudra peut être trouver apres un algorithme pour générer ce graphe la pour que l'application soit plus
#facilement évolutive et maintenable
GRAPHE_REPR =[
				[],
				[2,5,6],#1
				[1,5,6,7,3],#2
				[2,6,7,8,4],#3
				[3,7,8],#4

				[1,2,6,9,10],#5
				[1,2,3,5,7,9,10,11],#6
				[2,3,4,6,8,10,11,12],#7
				[3,4,7,11,12],#8

				[5,6,10,13,14],#9
				[5,6,7,9,11,13,14,15],#10
				[6,7,8,10,12,14,15,16],#11
				[7,8,11,15,16],#12

				[9,10,14],#13
				[9,10,11,13,15],#14
				[10,11,12,14,16],#15
				[11,12,15],#16
	]



"""
(1,1)  1
(1,2)  2
(1,3)  3
(2,1)  5
(2,3)  7
La fonction qui nous permet d'avoir ceci est la suivante (get_value_from_position)
"""
def get_value_from_position(t):
	# (1,1)  (1-1)*4 + 1 = 1
	# (3,1)  (3-1)*4 + 1  = 9
	return (t[0]-1)*4+t[1]

#Obtenir la position d'un widget(Une case) en tant que tuple (ligne,colonne)
#case 2 de ligne 1  par exemple nous renvoie (1,2)
#En gros c'est cette fonction qui nous permet d'avoir le tuple que nous passons a get_value_from_position
def get_position_row_col(w):
	info = w.grid_info()
	return (info['row']+1,info['column']+1)

#Par exemple je donne la case 2 de la ligne 1  j'aurais tout ses voisins à partir du graph representatif
#(1,2) correspond à 2 et je donne 2 au graph representatif pour avoir ses voisins
def get_liste_voisins_from_case(w):
	value_from_position =get_value_from_position(get_position_row_col(w))
	return GRAPHE_REPR[value_from_position]




