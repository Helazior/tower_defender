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
plateau = Plateau(pygame, "map.txt")
#setup pour la creation de mob
listeMob = list()
listeMobPriorityTarget = list()
listeDyingMob = list()
lastMobAt = 0
#setup pour la creation de tour
dicoTour = dict()
selectBuild = False

continuer = True

#_________________________________________________boucle principale:_________________________________________________

while continuer: #tout ce passe là dedans
    
    for event in pygame.event.get(): #il passe toutes les touches en revu pour voir lorsque tu appuies sur une touche
        pygame.event.pump() #c'est pour pas qu'il fasse "le programme ne répond plus", normalement ça marche sans mais pour moi non
            
        if event.type == pygame.QUIT: #quand t'appuies sur la croix ça quitte 
            continuer = False

       #______________________séléction batiment________________________________________
        elif event.type == pygame.MOUSEMOTION:
            selectBuild, posSelect = Build.is_build(plateau, event.pos, dicoTour)

        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #print(clock.get_fps()) #affiche les vrais fps
            #_________________poser une tour______________________________________________
            Tour.set_up(plateau, event.pos, dicoTour) #pose un bâtiment s'il y a de la place, taille dépendra du bâtiment séléctionné


            #_________________séléctionner un mob pour le mettre en priorité______________
            Mob.prioritizemob(plateau, listeMob, listeMobPriorityTarget, event.pos)
                

    #____________________bouger les mobs____________________
    #on affiche le fond de base pour effacer les mobs
    plateau.fenetre.blit(plateau.copy_fond, (0,0))
    Mob.movemobs(plateau, listeMob,listeMobPriorityTarget)

    #____________________tour attaque______________________
    for tour in dicoTour.values():
        tour.attack(plateau, listeMob, listeDyingMob, listeMobPriorityTarget)
        
    #____________________tuer les mobs____________________
    Mob.killmobs(plateau, listeDyingMob)

    #____________________creer les mobs____________________
    #un mob est crée toutes les x secondes (a preciser sur le if)
    if time() - lastMobAt > .5 :
        lastMobAt = Mob.spawnmobs(plateau, listeMob)

    #____________________affiche la range des tours_________ plus les infos
    if selectBuild:
        Build.info_build(plateau, posSelect, dicoTour)


    clock.tick(15) #en fps, valeur +grande = jeu + rapide
    pygame.display.flip() #rafraichit l'image

pygame.quit()


