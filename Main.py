from random import randint
from pygame.locals import *
from time import time
import sys, os
import pygame

from initialise_lvl import * 
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
listeMobPriorityTarget = list()
listeDyingMob = list()
lastMobAt = 0
#setup pour la creation de tour
dicoTour = dict()
dicoToursMenu = {1 : Stalker, 2 : Sentry, 3 : Tank} #dictionnaire des tours par leur position pour cliquer dessus
dicoImagesMenu = {Stalker : plateau.imageStalker, Sentry : plateau.imageSentry, Tank : plateau.imageTank}
tourSelectMenu = None
selectBuild = False
selectForceField = False

continuer = True

#_________________________________________________boucle principale:_________________________________________________

while continuer: #tout ce passe là dedans
    
    for event in pygame.event.get(): #il passe toutes les touches en revu pour voir lorsque tu appuies sur une touche
        pygame.event.pump() #c'est pour pas qu'il fasse "le programme ne répond plus", normalement ça marche sans mais pour moi non
            
        if event.type == pygame.QUIT: #quand t'appuies sur la croix ça quitte
            continuer = False

       #______________________séléction batiment posé_____________________________________
        elif event.type == pygame.MOUSEMOTION:
            posSouris = event.pos
            if tourSelectMenu == None:
                selectBuild, posSelect = Build.is_build(plateau, posSouris, dicoTour)
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #print(clock.get_fps()) #affiche les vrais fps
            #_________________séléction batiment menu_____________________________________
            (posx, posy) = (event.pos[0], event.pos[1])
            if posx >= 1200:
                try:
                    tourSelectMenu = dicoToursMenu[posy // 100]
                    imageSelect = dicoImagesMenu[tourSelectMenu]
                except:
                    pass
            else:
                tourSelectMenu = None
                
                #_________________Take force field in a Sentry__________________________
                if selectBuild and dicoTour[posSelect].name == "sentry" and dicoTour[posSelect].mana >= 50:
                    selectForceField = True
                    sentryUseForceField = dicoTour[posSelect]
                    posSentryUseForceField = posSelect
                    imageSelect = plateau.imageforceField
                    

                #_________________séléctionner un mob pour le mettre en priorité______________
                Mob.prioritizemob(plateau, listeMob, listeMobPriorityTarget, event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if tourSelectMenu != None:
                #_________________poser une tour__________________________________________
                Build.set_up(plateau, event.pos, dicoTour, tourSelectMenu) #pose un bâtiment s'il y a de la place, taille dépendra du bâtiment séléctionné
                tourSelectMenu = None

            elif selectForceField:
                selectForceField = False
                numMatrice = plateau.Matrice[posSouris[1]//30][posSouris[0]//30]
                #_________________put force field__________________________________
                if numMatrice == 1 or numMatrice == 4: 
                    sentryInRange = sentry_min_range({posSentryUseForceField : sentryUseForceField}, posSouris)
                    if sentryInRange:
                        plateau.forcefield.append(forceField(plateau,posSouris))


        elif event.type == pygame.KEYDOWN:
            try:
                numMatrice = plateau.Matrice[posSouris[1]//30][posSouris[0]//30]
                #_________________put force field____________________________________
                if event.key == K_f and (numMatrice == 1 or numMatrice == 4):
                    sentryInRange = sentry_min_range(dicoTour, posSouris)
                    if sentryInRange:
                        plateau.forcefield.append(forceField(plateau, posSouris))
            except IndexError:
                pass


    #____________________vague suivante_____________________
    if plateau.lvl.nbMobs[plateau.lvl.vague] <= 0: 
        if time() - plateau.lvl.tempsFinVague >= plateau.lvl.tempsAvantVague[plateau.lvl.vague]:
            plateau.lvl.vague += 1
            print("vague" , plateau.lvl.vague + 1)
            if plateau.lvl.vague > len(plateau.lvl.ordreMobs):
                print("Gagné !")
                continuer = False
        #_______________gagné !_______________
        if plateau.lvl.vague + 1 >= len(plateau.lvl.ordreMobs) and listeMob == []:
                print("Gagné !")
                continuer = False
                sleep(5)





    #____________________recharge la mana___________________
    for tour in dicoTour.values():
        try:
            if time() - tour.lastRechargeMana >= tour.timeRechargeMana and tour.mana < tour.maxMana:
                tour.mana += 1
                tour.lastRechargeMana = time()
        except AttributeError:
            pass

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
    if time() - lastMobAt > plateau.lvl.tempsEntreMobs[plateau.lvl.vague] and plateau.lvl.nbMobs[plateau.lvl.vague] > 0:
        lastMobAt = Mob.spawnmobs(plateau, listeMob)

    #____________________affiche la range des tours_________ plus les infos
    if selectBuild:
        Build.info_build(plateau, posSelect, dicoTour)
    #____________________affiche élément séléctionné________ 
    if tourSelectMenu != None:
        plateau.fenetre.blit(imageSelect, (posSouris[0] - 15 * tourSelectMenu.taille, posSouris[1] - 15 * tourSelectMenu.taille))
    if selectForceField:
        plateau.fenetre.blit(imageSelect, (posSouris[0] - 23, posSouris[1] - 15))

    #____________________affiche les explosions_____________
    for explosion in plateau.explosion:
        explosion.affiche(plateau)

    #____________________affiche les force fields___________
    for forcef in plateau.forcefield:
        forcef.affiche(plateau)
    #____________________affiche les barres de mana_________
    for tour in dicoTour.values():
        try:
            tour.show_mana(plateau)
        except AttributeError:
            pass
    
    #___________________affiche les pv mobs_________________
    for mob in listeMob:
        if mob.pv < mob.pvMax: #s'il n'a pas tous ses pv
            mob.show_pv(plateau)


    clock.tick(45) #en fps, valeur +grande = jeu + rapide
    pygame.display.flip() #rafraichit l'image

pygame.quit()


