from random import randint

from Mob import Mob
from Build import Build
from Plateau import * #sous-programme comprennant toutes les fonctions et la classe concernant la map

from time import time

import pygame
from pygame.locals import *

pygame.init()

import sys, os
pathname = os.path.dirname(sys.argv[0]) #chemin du programme

os.chdir (os.path.abspath(pathname))    #c'est pour que le repertoire courant soit au niveau du programme
os.chdir ("ressources")                     #c'est pour que le repertoire courant soit dans "ressources"

clock = pygame.time.Clock() #initialise une horloge pour gerer le temps

#__________________________________________________création map:_____________________________________________________

plateau = Plateau(pygame) #initialise l'objet plateau (Matrice, nbCasesX, nbCasesY, tailleFenetre)


mob1 = Mob(plateau.Matrice , pygame)
#print(f"{mob1.posxmatrice},{mob1.posymatrice}")


quitter = True

#_________________________________________________boucle principale:_________________________________________________

while quitter: #tout ce passe là dedans
    
    for event in pygame.event.get(): #il passe toutes les touches en revu pour voir lorsque tu appuies sur une touche
        pygame.event.pump() #c'est pour pas qu'il fasse "le programme ne répond plus", normalement ça marche sans mais pour moi non
            
        if event.type == pygame.QUIT: #quand t'appuies sur la croix ça quitte :)
            quitter = False
    #____________________bouger le mob____________________
    try:
        plateau.fenetre.blit(plateau.copy_fond, (0,0)) #on affiche le fond de base pour effacer les mobs
        mob1.move_to_next_pos(plateau.Matrice , pygame , plateau)
        print(f"{mob1.posxmatrice},{mob1.posymatrice}")
    except IndexError:
        print(f"{mob1.name} is stuck on a border")

    clock.tick(30) #3 fps, c'est juste pour tester le déplacement du mob
    pygame.display.flip() #rafraichit l'image !

pygame.quit()
