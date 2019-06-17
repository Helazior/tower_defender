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
                                conditionSolVide *= (plateau.Matrice[posMatrice[1] + j - l][posMatrice[0] + i - k] == 0)
                        if conditionSolVide:
                            listeTour.append(Build(pygame, plateau, (pos[0] - 30*k, pos[1] - 30*l)))
                            break
                    if conditionSolVide:
                        break

    #____________________bouger le mob____________________
    
    plateau.fenetre.blit(plateau.copy_fond, (0,0)) #on affiche le fond de base pour effacer les mobs
    temp = 0
    while temp < len(listeMob):
        newPosMob = listeMob[temp].move_to_next_pos(pygame, plateau)
        if newPosMob == "mob is stuck":
            #si le mob est bloqué on le supprime pour l'instant
            listeMob.pop(temp)
            temp -= 1
        temp += 1
        
    #____________________tuer le mob____________________
    
    temp = 0
    while temp < len(listeDyingMob):
        etatMob = listeDyingMob[temp].is_dying(pygame, plateau)
        if etatMob == "mob is dead":
            #si le mob est mort on le supprime de la liste
            listeDyingMob.pop(temp)
            temp -= 1
        temp += 1

    #____________________creer le mob____________________
    #le mob est crée toutes le x secondes (a preciser sur le if)
    if time() - lastMobAt > 0.5 :
        randomponey = randint(0,2)
        if randomponey == 0:
            listeMob.append(Scootaloo(pygame, plateau))
        elif randomponey == 1:
            listeMob.append(AppleBloom(pygame, plateau))
        else:
            listeMob.append(SweetieBelle(pygame, plateau))
        lastMobAt = time()


    clock.tick(30) #en fps, valeur+grande = jeu + rapide
    pygame.display.flip() #rafraichit l'image

pygame.quit()
