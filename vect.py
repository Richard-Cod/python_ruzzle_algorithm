"Primitives de traitement des vecteurs et matrices pour les TP"


## Pour faire clairement une distinction entre listes et vecteurs (tous deux
## mis en ouvre par le type List de python) nous allons écrire des primitives
## de création de vecteurs et de matrices afin de masquer que ce sont des listes Python
## On manipulera donc les vecteurs et matrices par création et initialisation (à l'aide des
## primitives suivantes puis accès direct à leurs éléments
## V= initVect(n,0), V[2]=1,
## initMat(n,0) M[i][j]=4 etc..
## Ils seront toujours de taille constante

## En revanche pour les listes nous utiliserons les méthodes d'insertion, d'ajout ou de suppression
## avec la syntaxe pointée, après initialisation à la liste vide  :
## Exemples : L=[] L.append(1) L.pop(0),...


def initVect(n,a):
    "Initialisation d'un vecteur de taille n et de valeur a"
    V=[]
    for j in range(n):
        V.append(a)
    return V


def initMat(n,a):
    "création d'une matrice carrée de taille n initialisée à a"
    M=[]
    for i in range(n):
        L=[]
        for j in range(n):
            L.append(a)
        M.append(L)
    return M


def affMat(M):
    "Affichage d'une matrice"
    for i in range(len(M)):
        print(M[i])


