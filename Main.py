from random import randint
from time import time
import pygame
from pygame.locals import *
import sys, os

from Mob import Mob
from Build import Build
from Plateau import * #sous-programme comprennant toutes les fonctions et la classe concernant la map

pygame.init()

pathname = os.path.dirname(sys.argv[0]) #chemin du programme

os.chdir (os.path.abspath(pathname))    #c'est pour que le repertoire courant soit au niveau du programme
os.chdir ("ressources")                     #c'est pour que le repertoire courant soit dans "ressources"

clock = pygame.time.Clock() #initialise une horloge pour gerer le temps

#__________________________________________________création map:_____________________________________________________

plateau = Plateau(pygame) #initialise l'objet plateau (Matrice, nbCasesX, nbCasesY, tailleFenetre)

#setup pour la creation de mob
listeMob = list()
lastMobAt = time()
listeMob.append(Mob(pygame, plateau.Matrice))

quitter = True

#_________________________________________________boucle principale:_________________________________________________

while quitter: #tout ce passe là dedans
    
    for event in pygame.event.get(): #il passe toutes les touches en revu pour voir lorsque tu appuies sur une touche
        pygame.event.pump() #c'est pour pas qu'il fasse "le programme ne répond plus", normalement ça marche sans mais pour moi non
            
        if event.type == pygame.QUIT: #quand t'appuies sur la croix ça quitte 
            quitter = False
            
    #____________________creer le mob____________________
    #le mob est crée toutes le x secondes a preciser sur le if
    if time() - lastMobAt > 0.5 :
        listeMob.append(Mob(pygame, plateau.Matrice))
        lastMobAt = time()
    else:
        pass
    
    #____________________bouger le mob____________________
    
    plateau.fenetre.blit(plateau.copy_fond, (0,0)) #on affiche le fond de base pour effacer les mobs
    try:
        for i in range(len(listeMob)) :
            newPosMob = listeMob[i].move_to_next_pos(pygame, plateau.Matrice, plateau)
            if newPosMob == "mob is stuck":
                #si le mob est bloqué on le supprime pour l'instant
                listeMob.pop(i)
    except IndexError:
        #la liste est vide
        pass
    
    clock.tick(20) #en fps, valeur+grande = jeu + rapide
    pygame.display.flip() #rafraichit l'image

pygame.quit()
