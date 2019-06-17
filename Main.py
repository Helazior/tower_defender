from random import randint
from time import time
import pygame
from pygame.locals import *
import sys, os

from Mob import Mob
from Build import *
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
listeMob.append(Mob(pygame, plateau))

quitter = True

tour = []

#_________________________________________________boucle principale:_________________________________________________

while quitter: #tout ce passe là dedans
    
    for event in pygame.event.get(): #il passe toutes les touches en revu pour voir lorsque tu appuies sur une touche
        pygame.event.pump() #c'est pour pas qu'il fasse "le programme ne répond plus", normalement ça marche sans mais pour moi non
            
        if event.type == pygame.QUIT: #quand t'appuies sur la croix ça quitte 
            quitter = False
            
        #_________________poser une tour___________________
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            posMatrice = convertPixelMatrice(pos)
            print (posMatrice)
            if posMatrice[0] < 39 and posMatrice[1] < 19: #car taille = 2, changer sinon
                conditionSolVide = 1
                for i in range(2):
                    for j in range(2):
                        conditionSolVide *= (plateau.Matrice[posMatrice[1] + j][posMatrice[0] + i] == 0)
                if conditionSolVide:
                    tour.append(Build(pygame, plateau, pos))
            
    
    #____________________bouger le mob____________________
    
    plateau.fenetre.blit(plateau.copy_fond, (0,0)) #on affiche le fond de base pour effacer les mobs
    try:
        for i in range(len(listeMob)) :
            newPosMob = listeMob[i].move_to_next_pos(pygame, plateau)
            if newPosMob == "mob is stuck":
                #si le mob est bloqué on le supprime pour l'instant
                listeMob.pop(i)
    except IndexError:
        #la liste est vide
        pass

        #____________________creer le mob____________________
    #le mob est crée toutes le x secondes a preciser sur le if
    if time() - lastMobAt > 0.5 :
        listeMob.append(Mob(pygame, plateau))
        lastMobAt = time()
    
    clock.tick(20) #en fps, valeur+grande = jeu + rapide
    pygame.display.flip() #rafraichit l'image

pygame.quit()
