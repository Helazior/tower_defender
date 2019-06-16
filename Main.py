from random import randint

from Mob import Mob
from Build import Build
from Plateau import * #sous-programme comprennant toutes les fonctions et la classe concernant la map

import pygame
from pygame.locals import *

pygame.init()

import sys, os
pathname = os.path.dirname(sys.argv[0]) #chemin du programme
os.chdir (os.path.abspath(pathname))    #c'est pour que le repertoire courant soit au niveau du programme
os.chdir ("ressources")                     #c'est pour que le repertoire courant soit dans "ressources"



#___________________création map:__________________
Plateau = Plateau() #initialise l'objet plateau (Matrice, nbCasesX, nbCasesY, tailleFenetre)

#Creation et affichage de la fenetre:
initFenetre(Plateau,pygame)

quitter = 0




#__________________boucle principale:________________

while quitter == 0: #tout ce passe là dedans
    
    for event in pygame.event.get(): #il passe toutes les touches en revu pour voir lorsque tu appuies sur une touche
        pygame.event.pump() #c'est pour pas qu'il fasse "le programme ne répond plus", normalement ça marche sans mais pour moi non
            
        if event.type == pygame.QUIT: #quand t'appuies sur la croix ça quitte :)
            quitter = 1


    pygame.display.flip() #rafraichit l'image !
pygame.quit()
