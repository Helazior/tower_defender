
"""
_______________help________________

- 0,1,2,3,4 pour choisir le bloc correspondant (0 par défaut)
- clique pour poser un bloc
- rester appuyer et bouger la souris pour poser plein de blocs
- 's' pour enregistrer (en fait pour l'instant ça enregistre automatiquement quand on quitte)
- 'u' pour revenir à la dernière sauvegarde, utile pour ne pas enregistrer ('z' était trop proche de 's')

- fileName est le nom du fichier texte, il doit exister.
"""

import pygame
from pygame.locals import *
import sys, os

from Plateau import * #sous-programme comprennant toutes les fonctions et la classe concernant la map

pygame.init()

pathname = os.path.dirname(sys.argv[0])     #chemin du programme

os.chdir (os.path.abspath(pathname))        #c'est pour que le repertoire courant soit au niveau du programme
os.chdir ("ressources")                     #c'est pour que le repertoire courant soit dans "ressources"

clock = pygame.time.Clock() 				#initialise une horloge pour gerer le temps


#setup pour le plateau
fileName = "map.txt"   #mettre un fichier txt existant qui peut-être vide
plateau = Plateau(pygame)
#je charge et convertis les images dans des variables
fond = pygame.image.load("fond.png").convert()
chemin = pygame.image.load("chemin.png").convert()
chemin4 = pygame.image.load("chemin4.png").convert()
start = pygame.image.load("start.png").convert_alpha()
end = pygame.image.load("end.png").convert_alpha()


def to_show_the_4(plateau, chemin4):
    for y in range(len(plateau.Matrice)):
        for x in range(len(plateau.Matrice[0])):
            if plateau.Matrice[y][x] == 4:
                plateau.fenetre.blit(chemin4, (30*x,30*y))
                pygame.display.flip() #rafraichit l'image

to_show_the_4(plateau, chemin4) #affiche un 4 sur toutes les cases 4
            
#______________save_______________
def save(matrice, fileName):
    try:
        with open(fileName,"w") as fichier:     #ouverture du fichier texte en mode écriture
            for ligne in matrice:
                for chiffre in ligne:
                    chiffre = str(chiffre)
                    fichier.write(chiffre)
                fichier.write("\n")


        print(f"{fileName} a bien été enregistrée !")
    except:
        print("ERREUR d'enregistrement...")

def is_in_matrice(matrice, n): #test si n est dans la matrice
    for ligne in matrice:
        if n in ligne:
            return True
    return False

def put_a_block(plateau, event, numCase, dictImage):
    x = event.pos[0] // 30
    y = event.pos[1] // 30
    try:
        numCaseActuel = plateau.Matrice[y][x]
        if numCase != numCaseActuel:
            plateau.Matrice[y][x] =  numCase
            plateau.fenetre.blit(dictImage[numCase], (30*x,30*y))
            pygame.display.flip() #rafraichit l'image
                                 
    except:
        pass



dictKey = {256 : 0, 257 : 1, 258 : 2, 259 : 3, 260 : 4, 224 : 0, 38 : 1, 233 : 2, 34 : 3, 39 : 4}
dictImage = {0: fond, 1: chemin, 2: start, 3: end, 4: chemin4}
numCase = 0
clique = False
continuer = True


#_________________________________________________boucle principale:_________________________________________________

while continuer: #tout ce passe là dedans
    
    for event in pygame.event.get(): #il passe toutes les touches en revu pour voir lorsque tu appuies sur une touche
        pygame.event.pump() #c'est pour pas qu'il fasse "le programme ne répond plus", normalement ça marche sans mais pour moi non
            
        if event.type == pygame.QUIT: #quand t'appuies sur la croix ça quitte et enregistre
            save(plateau.Matrice, fileName)
            continuer = False


        elif event.type == pygame.MOUSEBUTTONDOWN:
            clique = True
            put_a_block(plateau, event, numCase, dictImage)
        elif event.type == pygame.MOUSEMOTION and clique:
            put_a_block(plateau, event, numCase, dictImage)
        elif event.type == pygame.MOUSEBUTTONUP:
            clique = False
        elif event.type == pygame.KEYDOWN:
            try:
                numCase = dictKey[event.key]
                print(numCase)
            except:
                if event.key == K_s: #appuyer sur 's' pour enregistrer la map
                    save(plateau.Matrice, fileName)
                elif event.key == K_u: #'u' revient à la dernière sauvegarde
                    plateau = Plateau(pygame)
                    to_show_the_4(plateau, chemin4)



    clock.tick(60) #en fps, valeur +grande = jeu + rapide



pygame.quit()
