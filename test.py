import pandas as pd
import requests
from bs4 import BeautifulSoup
from helpers import *
from random import random
url = "https://fr.wikipedia.org/wiki/Fr%C3%A9quence_d%27apparition_des_lettres_en_fran%C3%A7ais"
page = requests.get(url)
soup= BeautifulSoup(page.content,'html.parser')
table_class = "wikitable sortable jquery-tablesorter"

def get_letter_frequency():
    table = soup.find_all("table")[0]
    tableau = {}
    for tr in table.find('tbody').find_all('tr') :
        if(tr.td):
            i = tr.find_all('td')
            rang = i[0].getText()
            caractere=i[1].getText().strip()
            pourcentage = i[3].getText().strip()
            tableau[caractere] = float(pourcentage.replace(',','.').replace('%','')) 
    return tableau

tab = get_letter_frequency()

def make_letters_range():
    cpt= 0
    tableau={}
    for lettre in LETTRES:
        #print(lettre,tab[lettre])
        test= cpt+tab[lettre]
        #print(f"{lettre} si on est entre {cpt} et {test}")
        tableau[lettre]= [cpt,test]
        cpt = test
    return tableau


def make_list_randomly():
    l = []
    while len(l) < 16 :
        aleatoire = round(random()*100, 2)
        LETTERS_AND_RANGE = make_letters_range()
        for k,v in LETTERS_AND_RANGE.items():
            if v[0]<= aleatoire <= v[1] :
                l.append(k)
    
    return l


#liste = make_list_randomly()
#print(liste)
input = ['abaissement', 'manger','boire'] 
charSet = ['a','b','i','s','s','e','e','m','n','t'] 
mots = possible_words(input = input, charSet=charSet)


print("les mots sont : ",mots)