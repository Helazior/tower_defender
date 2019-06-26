from math import sqrt
from time import time
from Mob import *

import pygame

def convertPixelMatrice(pos):#à mettre dans plateau je pense, mais faudra importer plateau après
    return (pos[0]//30, pos[1]//30)

class Build :
    def  __init__(self, plateau, pos, brange, damage, taille, attenteTir, bulding):


        #affiche la tour
        posM = convertPixelMatrice(pos)
        
        plateau.fenetre.blit(plateau.copy_fond, (0, 0))
        plateau.fenetre.blit(bulding, (posM[0]*30, posM[1]*30))

        
        plateau.copy_fond = pygame.display.get_surface().copy()
        self.posx = pos[0] // 30 * 30 + 15*taille # on centre le position
        self.posy = pos[1] // 30 * 30 + 15*taille
        self.attenteTir = attenteTir
        self.range = brange
        self.damage = damage
        self.tempsDernierTir = time() - attenteTir

        for i in range(taille):
            for j in range(taille):
                plateau.Matrice[posM[1]+j][posM[0]+i] = 6 + taille
        

    def attack(self, plateau, listeMob, listeDyingMob, listeMobPriorityTarget):
        if listeMob == []:
            pass
        else:
            if time() - self.tempsDernierTir >= self.attenteTir: #attente avant de retirer
                listeMobAndPriority = listeMobPriorityTarget + listeMob # listeMobPriorityTarget devant sera lue en première
                for posInListe in range(len(listeMobAndPriority)) :
                    mob = listeMobAndPriority[posInListe]
                    distance = sqrt(((self.posx - (mob.posx + 15))**2)+((self.posy - (mob.posy + 15))**2))
                    if  distance <= self.range :
                        self.tempsDernierTir = time()
                        self.tir(plateau, (self.posx, self.posy), (mob.posx + 15, mob.posy + 15)) #animation du tir
                        mob.pv -= self.damage
                        #print(f"Mob {posInListe} touché, lui reste {mob.pv} pv")
                        try:
                            self.damageZone(plateau, listeMob, listeDyingMob, (mob.posx + 15, mob.posy + 15), listeMobPriorityTarget)
                        except AttributeError:
                            pass

                        mob.is_it_dying(listeMob, mob, listeDyingMob, listeMobPriorityTarget)                           
                        break



    #________________________staticmethod_______________________



    @staticmethod
    def set_up(plateau, pos, dicoTour, tour):
        (x,y) = pos
        if x > 15 and y > 15:
            taille = tour.taille
            pos = (x - 15*(taille - 1) , y - 15*(taille - 1)) #pour que le clique soit centré par rapport a la tour qu'il fait apparaitre
            posMatrice = convertPixelMatrice(pos)
            freeSpace = True
            try:
                for i in range(taille):
                    for j in range(taille):
                        (y, x) = (posMatrice[1] + i , posMatrice[0] + j)
                        if plateau.Matrice[y][x] != 0 :
                            freeSpace = False
                            break             
            except IndexError:
                freeSpace = False

            if freeSpace:
                posx = pos[0] // 30 * 30 + 15*tour.taille
                posy = pos[1] // 30 * 30 + 15*tour.taille
                dicoTour[(posx,posy)] = tour(plateau, pos) #création de la tour

    @staticmethod
    def is_build(plateau, pos, dicoTour):
        try:
            taille = plateau.Matrice[pos[1]//30][pos[0]//30] - 6
            if taille >= 1:
                posx = (pos[0] - 15 * (taille - 1)) // 30 * 30 + 15 * taille
                posy = (pos[1] - 15 * (taille - 1)) // 30 * 30 + 15 * taille
                pos = (posx,posy)
                try:
                    dicoTour[pos]
                    return True, pos
                except KeyError:
                    return False, pos
            return False, pos
        except IndexError:
            return False, pos

    @staticmethod
    def info_build(plateau, pos, dicoTour):
        white = (150,150,150)
        pygame.draw.circle(plateau.fenetre, white, pos, dicoTour[pos].range, 1)
        #pygame.display.flip()



class Stalker(Build):
    """docstring for Stalker"""
    taille = 2

    def __init__(self, plateau, pos, brange = 200, damage = 10, attenteTir = 0.7):
        self.imageStalker = plateau.imageStalker
        Build.__init__(self, plateau, pos, brange, damage, Stalker.taille, attenteTir, plateau.imageStalker)

    @staticmethod
    def tir(plateau, posStalker, posMob):
        red = (175,0,0)
        pygame.draw.line(plateau.fenetre, red, posStalker, posMob, 3) #fait un trait rouge de la tour jusqu'au mob


class Sentry(Build):
    """docstring for Sentry"""
    taille = 1
    
    def __init__(self, plateau, pos, brange = 100, damage = 3, attenteTir = 0.4):
        self.imageSentry = plateau.imageSentry
        Build.__init__(self, plateau, pos, brange, damage, Sentry.taille, attenteTir, plateau.imageSentry)

    @staticmethod
    def tir(plateau, posSentry, posMob):
        blue = (0,255,100)
        pygame.draw.line(plateau.fenetre, blue, posSentry, posMob, 3) #fait un trait rouge de la tour jusqu'au mob


class Tank(Build):
    """docstring for Sentry"""
    taille = 3
    zone = 50
    dmZone = 50
    
    def __init__(self, plateau, pos, brange = 300, damage = 20, attenteTir = 3, rangeMini = 60):#dmZone se rajoute à damage
        self.imageTank = plateau.imageTank
        Build.__init__(self, plateau, pos, brange, damage, Tank.taille, attenteTir, plateau.imageTank)

    def damageZone(self, plateau, listeMob, listeDyingMob, posTir, listeMobPriorityTarget):
        (posTirx, posTiry) = posTir
        temp = 0

        while temp < len(listeMob):
            mob = listeMob[temp]
            distance = sqrt(((mob.posx + 15 - posTirx)**2)+((mob.posy + 15 - posTiry)**2))
            if distance <= self.zone:
                mob.pv -= Tank.dmZone
                mob.is_it_dying(listeMob, mob, listeDyingMob, listeMobPriorityTarget)
                temp -= 1
            temp += 1



    @staticmethod
    def tir(plateau, posTank, posMob):
        brown = (175,100,0)
        pygame.draw.line(plateau.fenetre, brown, posTank, posMob, 20) #fait un trait rouge de la tour jusqu'au mob
        plateau.explosion.append(Explosion(plateau, posMob))





class Explosion:
    def __init__(self, plateau, pos):
        self.image = 1
        self.pos = (pos[0] - 30, pos[1] - 30)

    def affiche(self, plateau):
        plateau.fenetre.blit(plateau.animationExplosion[int(self.image)], self.pos)
        self.image += 0.2
        if self.image >= 6:
            plateau.explosion.remove(self)
