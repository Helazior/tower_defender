from random import randint
from pygame.locals import *
from time import time
import sys, os
import pygame

from Mob import *
from Build import *
from Plateau import * #sous-programme comprennant toutes les fonctions et la classe concernant la map

pygame.init()

pathname = os.path.dirname(sys.argv[0])     #chemin du programme

os.chdir (os.path.abspath(pathname))        #c'est pour que le repertoire courant soit au niveau du programme
os.chdir ("ressources")                     #c'est pour que le repertoire courant soit dans "ressources"

clock = pygame.time.Clock() #initialise une horloge pour gerer le temps

#__________________________________________________création map:_____________________________________________________

#setup pour le plateau
plateau = Plateau(pygame)
#setup pour la creation de mob
listeMob = list()
listeDyingMob = list()
lastMobAt = 0
#setup pour la creation de tour
listeTour = list()

continuer = True

#_________________________________________________boucle principale:_________________________________________________

while continuer: #tout ce passe là dedans
    
    for event in pygame.event.get(): #il passe toutes les touches en revu pour voir lorsque tu appuies sur une touche
        pygame.event.pump() #c'est pour pas qu'il fasse "le programme ne répond plus", normalement ça marche sans mais pour moi non
            
        if event.type == pygame.QUIT: #quand t'appuies sur la croix ça quitte 
            continuer = False
            
        #_________________poser une tour___________________
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            posMatrice = convertPixelMatrice(pos)
            if posMatrice[0] < 39 and posMatrice[1] < 19:
                for k in range(2):
                    for l in range(2):
                        conditionSolVide = 1
                        for i in range(2):
                            for j in range(2):
                                y = posMatrice[1] + j - l
                                x = posMatrice[0] + i - k

                                if y < 0 or y > plateau.nbCasesY or x < 0 or x > plateau.nbCasesX:
                                    conditionSolVide = 0

                                conditionSolVide *= (plateau.Matrice[y][x] == 0)
                        if conditionSolVide:
                            listeTour.append(Build(plateau, (pos[0] - 30*k, pos[1] - 30*l)))
                            break
                    if conditionSolVide:
                        break



    #____________________bouger les mobs____________________
    #on affiche le fond de base pour effacer les mobs
    plateau.fenetre.blit(plateau.copy_fond, (0,0))
    Mob.movemobs(plateau, listeMob)

    #____________________la tour attaque____________________
    #je l'ai mis au milieu des tes fonctions pour que le rayon reste un peu plus longtemps
    for tour in listeTour:
        tour.attack(plateau, listeMob, listeDyingMob)
        
    #____________________tuer les mobs____________________
    Mob.killmobs(plateau, listeDyingMob)

    #____________________creer les mobs____________________
    #un mob est crée toutes les x secondes (a preciser sur le if)
    if time() - lastMobAt > 0.5 :
        lastMobAt = Mob.spawnmobs(plateau, listeMob)


    clock.tick(30) #en fps, valeur +grande = jeu + rapide
    pygame.display.flip() #rafraichit l'image

pygame.quit()
