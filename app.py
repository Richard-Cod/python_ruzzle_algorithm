from tkinter import * 
from helpers import *
from test import make_list_randomly
from random import randrange

from datetime import datetime
import time as tm



from tkinter.messagebox import *



""" Liste Des Constantes liées à l'affichage""" 
SCREEN_HEIGHT,SCREEN_WIDTH = 400,400
NB_CASES = 4
ONE_CASE_WIDTH = SCREEN_WIDTH/NB_CASES
SUCCESS_COLOR='#ff8700'


""" Liste des Variables liées au programme""" 
MINUTES,SECONDES=2,0
SCORE = 0

#Nous permettra de savoir si l'utilisateur a commencé à séléctionner des lettres pour former son mot
SELECTION_MODE = False

#Listes des mots que l'utilisateur a déja trouvé (Si il reforme un de ces mots on dira erreur car c'est déja trouvé)
WORDS_FOUNDED = []

#La Chaine de caractere qui est formé au fur et à mesure que l'utilisateur choisit des lettres
CURRENT_STRING = ""

# Les cases avec des lettres sont considérés comme des widgets (Plus précisement des bouttons)
LISTE_WIDGET_SELECTED=[]


#Permet de remettre à 0 le Jeu en l'occurence quand l'utilisateur recommence le jeu
def reinitialise_game():
	global MINUTES,SECONDES
	MINUTES,SECONDES = 2,0
	increase_score(-1*SCORE)
	WORDS_FOUNDED=[]
	display_message('.')
	#display_buttons()
	canvas.old_coords = None


#Permet la mise en place du timer 
def countDown():
	global MINUTES,SECONDES

	text="{}:{}".format(MINUTES,SECONDES)

	if MINUTES>0:
		if SECONDES==0:
			SECONDES=59
			MINUTES-=1
		else:
			SECONDES-=1
	elif MINUTES==0 and SECONDES>0:
		SECONDES-=1
	else:
		reponse = askokcancel("recommencer", "Voulez-vous recommencer ?")
		if reponse:
			reinitialise_game()
		else:
			quit_song.play()
			tm.sleep(2)
			f.quit()



	time['text']=text

	f.update()

	f.after(1000, countDown)


#Permet d'afficher un message dans la zone destinés aux messages pour l'utilisateur
def display_message(message,couleur='white',arriere='white'):
	message_zone['text']=message
	message_zone['bg']=arriere
	message_zone['fg']=couleur


#Quand l'utilisateur fini de séléctionner les lettres,vu que les cases choisies sont colorés
#On les remets à leur couleur initiale pour lui montrer que la séléction est terminé
def reset_frame_to_zero():
	global LISTE_WIDGET_SELECTED
	for case in LISTE_WIDGET_SELECTED:
		case['background'] = 'white'

#Augmenter le score de la valeur qui est passée puis l'actualiser à l'écran (une valeur négative permet de diminuer)
def increase_score(valeur):
	global SCORE
	SCORE+=valeur
	score_part['text']=SCORE

#En fonction du mot que l'utilisateur à créé , si il est bon on lui affiche un message de succes ou d'echec
#On augmente le score si le mot est bon 
#la validation c'est : le mot est il dans le fichier de mots ? N'est il pas déja trouvé par l'utilisateur ?
def check_word_created():
	if verify_in_file(CURRENT_STRING) and CURRENT_STRING not in WORDS_FOUNDED:
		t = "Bravo '{}' est un bon mot".format(v.get())
		increase_score(get_points_from_chaine(CURRENT_STRING))
		WORDS_FOUNDED.append(CURRENT_STRING)
		display_message(t,'green')
		success_song.play()

	elif CURRENT_STRING in WORDS_FOUNDED:
		t = "'{}' est déja trouvé par vous".format(v.get())
		display_message(t,'yellow','blue')
		deja_in_song.play()

	else:
		t="ERREUR ! '{}'' existe pas".format(v.get())
		display_message(t,"red",'black')
		
		erreur_song.play()


#Activation du mode selection de lettres (Au Clique droit de la souris)
def activate_selection(e):
	global SELECTION_MODE
	if SELECTION_MODE==False:
		#canvas.old_coords = e.x , e.y
		SELECTION_MODE=True
		on_mouse_over_frame_buttons(e)

#Si le mode séléction est démarré (True) , l'orsque l'utilisateur survole une case	elle est séléctionné
def on_mouse_over_frame_buttons(e):
	global CURRENT_STRING,SELECTION_MODE
	if SELECTION_MODE:
		#On ajoute ce widget à la liste de widget selctioné
		LISTE_WIDGET_SELECTED.append(e.widget)
		
		#(Considere WIDGET et CASE à lettre comme pareil)
		#Si il ne s'agit pas de la  1ere lettre du mot qui est en constitution
		if len(LISTE_WIDGET_SELECTED)>1:
			#print(e.x,e.y,canvas.old_coords)
			#canvas.create_line(e.x,e.y,canvas.old_coords[0],canvas.old_coords[1],width=10)
			#canvas.old_coords = e.x , e.y
			#Récupère la position de la case courante dans la liste
			index = LISTE_WIDGET_SELECTED.index(e.widget) 

			#On recupere le widget qui a été choisit juste avant celui sur lequel on est 
			widget_precedent = LISTE_WIDGET_SELECTED[index-1]

			#On recupere la liste des voisins du widget précédent
			voisins_of_precedent = get_liste_voisins_from_case(widget_precedent)

			#La valeur du widget courant
			value_of_current_widget =get_value_from_position(get_position_row_col(e.widget))
			current_wigdget_is_voisin = value_of_current_widget in voisins_of_precedent

			#Si le widget courant , ne fais pas parti de la liste des voisins du précédent on annule tout
			if current_wigdget_is_voisin == False:
				on_mouse_leave_frame(e)
				return None


		if e.widget['background']== SUCCESS_COLOR:
			return None

		#On ajoute la lettre à la chaine construite
		CURRENT_STRING+= e.widget['text']

		#On Affiche la chaine construite dans le INPUT DU HAUT
		v.set(CURRENT_STRING)

		#On change la couleur d'arriere plan du boutton pour que le user sache ce qu'il a selectionné !
		e.widget['background'] = SUCCESS_COLOR


#Si l'utilisateur sort de notre grid de cases , ou si il fais clique droit sur la souris la séléction est terminé 
#Permet de terminer donc la séléction en remettant tout à 0
def on_mouse_leave_frame(e):
	global CURRENT_STRING,SELECTION_MODE,LISTE_WIDGET_SELECTED
	canvas.delete("all")
	canvas.old_coords = None
	if SELECTION_MODE:
		#Remet toutes les lettres à leur couleur initiale
		reset_frame_to_zero()

		LISTE_WIDGET_SELECTED=[]
		check_word_created()
		
		#On réinitialise la chaine construite
		CURRENT_STRING=""

		#On désactive le mode selection
		SELECTION_MODE = False

		#Viderla selction
		LISTE_WIDGET_SELECTED =[]

		#On vide aussi le champ Input 
		v.set("")



#Fonction très importante du programme
#Permet d'afficher les différentes cases à lettres 
#Pour l'instant on affiche des lettres au hasard mais bientot 
#Il va falloir trouver un algorithme qui permet d'afficher les lettres de sorte à optimiser 
#le nombre de mot trouvables

"""
def display_buttons():
	cpt=1
	for i in range(0,4):
		for j in range(0,4):
			#Lettre de la case
			k=LETTRES[randrange(26)]
			btn=Button(gridframe,width=8,height=4, text=k,font=("Times", "14", "bold"))
			btn.grid(row=i,column=j,padx=4,pady=4)

			#Clique gauche (clique normal) de la souris démarre le mode séléction
			btn.bind("<Button-1>", activate_selection)
			#Clique droit de la souris permet de terminer le mode séléction
			btn.bind("<Button-3>", on_mouse_leave_frame)

			#L'orsque on est en train de survoler les cases de la grille de case
			btn.bind("<Enter>", on_mouse_over_frame_buttons)
			cpt+=1
"""
#make_list_randomly
"""
def display_buttons():
    cpt=1
    maliste = make_list_randomly()
    for i in range(0,4):
        for j in range(0,4):
            btn=Button(gridframe,width=8,height=4, text=maliste.pop(),font=("Times", "14", "bold"))
            btn.grid(row=i,column=j,padx=20,pady=15)
            #Clique gauche (clique normal) de la souris démarre le mode séléction
            btn.bind("<Button-1>", activate_selection)
            #Clique droit de la souris permet de terminer le mode séléction
            btn.bind("<Button-3>", on_mouse_leave_frame)
            #L'orsque on est en train de survoler les cases de la grille de case
            btn.bind("<Enter>", on_mouse_over_frame_buttons)
            cpt+=1
    
"""	
def display_buttons():
    cpt=1
    maliste = make_list_randomly()
    possible_words(charSet=maliste)
    for i in range(0,4):
        for j in range(0,4):
            g = maliste.pop()
            texte = f"{g} \n {LETTRES_POINTS[g]}"
            btn=Button(canvas,width=8,height=4, text=g,font=("Times", "14", "bold"))
            btn.grid(row=i,column=j,padx=20,pady=15)
            #Clique gauche (clique normal) de la souris démarre le mode séléction
            btn.bind("<Button-1>", activate_selection)
            #Clique droit de la souris permet de terminer le mode séléction
            btn.bind("<Button-3>", on_mouse_leave_frame)
            #L'orsque on est en train de survoler les cases de la grille de case
            btn.bind("<Enter>", on_mouse_over_frame_buttons)
            cpt+=1
    	
def myfunction(event):
    if SELECTION_MODE:
        x, y = event.x, event.y
        if canvas.old_coords:
            x1, y1 = canvas.old_coords
            canvas.create_line(x, y, x1, y1,width=10,fill='yellow')
        canvas.old_coords = x, y

#Permet de terminer le temps
def termine():
	global MINUTES,SECONDES
	MINUTES,SECONDES=0,0


#Tout à propos de l'affichage
f = Tk()
f.title("Projet python ARISTIDE RICHARD")
f.geometry("650x600")
f['bg'] = "#246eaf"

time = Label(f,font=("Times", "14", "bold italic"),fg="white",bg="#0282b3",width=5)
time.grid(row=0,column=0)


score_part = Label(f,text=SCORE,font=("Times", "15", "bold"),fg="white",bg="#0282b3")
score_part.grid(row=0,column=1)


B = Button(f, text ="Terminé",bg="#099ccc",fg="white",font=("Times", "12", "bold"), command =termine).grid(row=0,column=2)
v = StringVar()

e1 = Entry(f,textvariable=v,width=20,font=("Times", "20", "bold"),bg='#2671b4',fg='white',justify=CENTER)
e1.grid(row=1,column=1)

message_zone = Label(f,text=".",font=("Times", "14", "bold"))
message_zone.grid(row=2,column=1)

gridframe = Frame(f,bg='#438abe')
gridframe.grid(row=3,column=1)

canvas = Canvas(gridframe,bg="#428bc3")
canvas.grid(row=1,column=1)
#canvas.bind("<Button-1>", clique)
canvas.bind('<Motion>', myfunction)
canvas.old_coords = None


consigne_zone = Label(f,text="Clique gauche pour commencer la séléction et clique droit pour la terminer ",
						font=("Times", "10", "bold"))

consigne_zone.grid(row=4,column=1)

#Quand l'utilisateur quitte notre grille de cases 
gridframe.bind("<Leave>", on_mouse_leave_frame)

def clique(e):
	print("vous avez cliqué dans un coin vide")
#Quand on clique dans un endroit vide 



#Afficher l'ensemble des Buttons pour l'utilisateur
display_buttons()


#ooooooooooooooooooooooooooooooooooo
parcours_rob_as_letters(canvas.winfo_children())
#Démarrer le timer
countDown()


#Fonction utilitaire
f.mainloop()





