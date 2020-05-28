from random import randrange

import vect
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
				   'j' : 3,
				   'k':2,
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
				   'w':2,
       			   'x': 4,
				   'y':2,
	               'z': 3,
	               }

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




#Implementation des derniers features
liste = ['i', 'e', 'u', 'i', 'd', 'p', 'u', 'n', 'o', 'o', 'b', 'i', 'i', 'm', 'n', 'u']

  
from collections import Counter
def possible_words(input = get_list_mot_from_file(), charSet=[]):
    result = [] 
    for word in input:
        word = word.rstrip() 
        dict = Counter(word)
        flag = 1
        for key in dict.keys(): 
            if key not in charSet: 
                flag = 0
        if flag == 1:
            #print(word,'est un bon mot')
            testeur = True
            for i in word : 
                if (word.count(i) > charSet.count(i)):
                    #print("+ de ",i," dans ",word,"que dans ",charSet)
                    testeur = False
                    break
            if (testeur):
                #print(word)
                result.append(word)
    return result 


#print(charCount(get_list_mot_from_file()))   
input = ['abaissement', 'manger','boire'] 
charSet = ['m','a','n','g','o','e','r','b','i'] 
#possible_words(input, charSet) 
#possible_words(get_list_mot_from_file(), charSet) 

already = []
def parcours_profondeur(index):
    if(index not in already):
        voisins = GRAPHE_REPR[index]
        print("les voisins ",index,"sont : ",voisins)
        for voisinIndex in voisins :
            """
            voisins = voisins.remove(voisinIndex)
            already.append(voisinIndex)
            print(already)"""
            parcours_profondeur(voisinIndex)
        """
        if len(voisins) == 0 :
            return already
        if voisinIndex not in already:
            voisins.remove(voisinIndex)
            already.append(voisinIndex)
            parcours_profondeur(voisinIndex)"""


def largeur(G,i):
    #initialisation du vecteur de visite
    Visite=vect.initVect(len(G),0)    
    ordreVisite=[]
    Visite[i]=1
    File=[i]
    while len(File)!=0:
        x=File.pop(0)
        ordreVisite.append(x)
        for y in G[x]:
            if Visite[y] == 0:
                File.append(y)
                Visite[y]=1
    return ordreVisite

#Fonctions qui nous donne tous les parcours dispo
#On l'utilisera avec notre fonction qui donne tous les mots dispo 
#a partir d'une liste de lettres
def parcours_rob_as_numbers():
    result = []
    for i in range(17):
        chemin = largeur(GRAPHE_REPR ,i)
        result.append(chemin)
        
    return result[1:len(result)]
    
def parcours_rob_as_letters(l):
    liste = parcours_rob_as_numbers()
    result = []
    for i in liste:
        #print(i)
        truc = [l[index -1]['text'] for index in i]
        #result.append(list(zip(i,truc)))
        print(truc)
        """
        for index in i:
            print(l[index -1]['text'],end="")"""
    return result


def letterAndPosition(l):
    liste = parcours_rob_as_numbers()[0]
    result = {}
    for i in liste : 
        result[l[i -1]['text']] = []
               
               
    for i in liste :
        result[l[i -1]['text']].append(i)
            
    #print(result)
    return result


"""
			if index < len(mot) -1 :
				if dico[mot[index + 1]] in voisins:
					print(f'{mot[index]} peut toucher {mot[index + 1]}')
					
				else:
					testeur = False
					print(f'{mot[index]} NOTOUCH {mot[index + 1]}') 
"""

def touchable(position ,suivant,liste,parto):
    for positionNext in liste:
        if positionNext in GRAPHE_REPR[position]:
            print("suivant ",suivant, " ",positionNext," dans ",GRAPHE_REPR[position])
            return touchable(positionNext,suivant,GRAPHE_REPR[position],parto)
        else:
            print('far')
            break
                        
def importante(mot,dico):
    isGOOD = True
    canTouch = False
    print(mot)
    for positionDeLettreCourante in range(len(mot)):
        
        lettre = mot[positionDeLettreCourante]
        allPositionsOfLetter = dico[lettre]
        #voisins = GRAPHE_REPR[dico[i]]
        for position in allPositionsOfLetter:
            
            voisins = GRAPHE_REPR[position]
            #print("les voisins de ",lettre," ",voisins)
            
            if positionDeLettreCourante < len(mot) -1 :
                actu , suivant = mot[positionDeLettreCourante] ,mot[positionDeLettreCourante +1]
                print(actu,"pos = ",position," son suivant ",suivant," se situe ",dico[suivant])
                print(f"voisin de {actu} ",GRAPHE_REPR[position] )
                intersection = list(set(dico[suivant]).intersection(GRAPHE_REPR[position]))
                
                if(len(intersection) > 0):
                    print(f"{actu} peut atteindre {suivant}")
                    break
                else:
                    return 
                    break
                
                #touchable(position ,suivant,dico[suivant],[i for i in mot])
                        
  
    return isGOOD
                
    
    
def supper(l,listeDeLettres):
    result = []
    allWords = possible_words(charSet=listeDeLettres)
    print(allWords)
    
    lettreEtPosition = letterAndPosition(l)
    print(lettreEtPosition)
    #importante(allWords[0],lettreEtPosition)
    
    for mot in allWords:
        if (importante(mot,lettreEtPosition)):
            print(f"Le {mot} est un bon mot")
            
            result.append(mot)
    print(result)       
    return result

            
            
