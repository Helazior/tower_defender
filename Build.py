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
                    try:
                        rangeMini = self.rangeMini
                    except AttributeError: 
                        rangeMini = 0
                   
                    if  distance <= self.range and distance >= rangeMini:
                        self.tempsDernierTir = time()
                        self.tir(plateau, (self.posx, self.posy), (mob.posx + 15, mob.posy + 15)) #animation du tir
                        mob.pv -= self.damage
                        #print(f"Mob {posInListe} touché, lui reste {mob.pv} pv")
                        mob.is_it_dying(listeMob, mob, listeDyingMob, listeMobPriorityTarget)       

                        try:
                            self.damageZone(plateau, listeMob, listeDyingMob, (mob.posx + 15, mob.posy + 15), listeMobPriorityTarget)
                        except AttributeError:
                            pass

                        break



    #________________________staticmethod_______________________



    @staticmethod
    def set_up(plateau, pos, dicoTour, tour):
        (x,y) = pos
        if x > 15 and y > 15:
            taille = tour.taille
            pos = (x - 15*(taille - 1) , y - 15*(taille - 1)) #pour que le clique soit centrés par rapport a la tour qu'il fait apparaitre
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
        try:
            pygame.draw.circle(plateau.fenetre, white, pos, dicoTour[pos].rangeMini, 1)
        except AttributeError:
            pass

        #pygame.display.flip()



class Stalker(Build):
    """docstring for Stalker"""
    name = "stalker"
    taille = 2

    def __init__(self, plateau, pos, brange = 200, damage = 10, attenteTir = 0.8):
        self.imageStalker = plateau.imageStalker
        Build.__init__(self, plateau, pos, brange, damage, Stalker.taille, attenteTir, plateau.imageStalker)

    @staticmethod
    def tir(plateau, posStalker, posMob):
        red = (175,0,0)
        pygame.draw.line(plateau.fenetre, red, posStalker, posMob, 3) #fait un trait rouge de la tour jusqu'au mob


class Sentry(Build):
    """docstring for Sentry"""
    name = "sentry"
    taille = 1
    maxMana = 200
    timeRechargeMana = .3
   

    def __init__(self, plateau, pos, brange = 100, damage = 2, attenteTir = 0.3, mana = 50):
        self.mana = mana
        self.lastRechargeMana = time()

        self.imageSentry = plateau.imageSentry
        Build.__init__(self, plateau, pos, brange, damage, Sentry.taille, attenteTir, plateau.imageSentry)

    def show_mana(self, plateau):
        if self.mana >= forceField.cout:
            couleur = (150, 60, 255)
        else:
            couleur = (255, 0, 0)
        
        pygame.draw.line(plateau.fenetre, couleur, (self.posx - 15, self.posy - 20), (self.posx - 15 + 30 * self.mana / self.maxMana, self.posy - 20), 6)



    @staticmethod
    def tir(plateau, posSentry, posMob):
        blue = (0,255,255)
        pygame.draw.line(plateau.fenetre, blue, posSentry, posMob, 3) #fait un trait rouge de la tour jusqu'au mob


class Tank(Build):
    """docstring for Tank"""
    name = "tank"
    taille = 3
    zone = 50
    dmZone = 50
    rangeMini = 100
    
    def __init__(self, plateau, pos, brange = 300, damage = 20, attenteTir = 3):#dmZone se rajoute à damage
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
                if mob.pv <= 0:
                    temp -= 1
            temp += 1


    @staticmethod
    def tir(plateau, posTank, posMob):
        brown = (175,100,0)
        pygame.draw.line(plateau.fenetre, brown, posTank, posMob, 20) #fait un trait rouge de la tour jusqu'au mob
        plateau.explosion.append(Explosion(plateau, posMob))


class forceField:
    timeAppeared = 8
    cout = 50
    def __init__(self, plateau, pos):
        self.numMatriceAvant = plateau.Matrice[pos[1]//30][pos[0]//30]
        plateau.Matrice[pos[1]//30][pos[0]//30] = 5*(self.numMatriceAvant == 4)
        self.pos = pos
        self.image = plateau.imageforceField
        self.timePos = time()

    def affiche(self, plateau):
        if time() - self.timePos <= self.timeAppeared:
            plateau.fenetre.blit(self.image, (self.pos[0]//30*30 - 8,self.pos[1] //30*30- 5))
        else:
            plateau.Matrice[self.pos[1]//30][self.pos[0]//30] = self.numMatriceAvant
            plateau.forcefield.remove(self)

    
def sentry_min_range(dicoTour, posSouris):
    pos = (posSouris[0] // 30 * 30 + 15, posSouris[1] // 30 * 30 + 15) 
    listeSentry = []
    listeDistanceSentry = []
    for sentry in dicoTour.values():
        
        if sentry.name == "sentry":
            distance = sqrt((pos[0] - sentry.posx)**2 + (pos[1] - sentry.posy)**2)
            if distance <= sentry.range and sentry.mana >= forceField.cout:
                listeSentry.append(sentry)
                listeDistanceSentry.append(distance)

    if listeSentry != []:
        numSentrySelect = listeDistanceSentry.index(min(listeDistanceSentry))
        sentrySelect = listeSentry[numSentrySelect]
        sentrySelect.mana -= 50

        return True

    return False                                                                                                    
		

class Explosion:
    def __init__(self, plateau, pos):
        self.image = 1
        self.pos = (pos[0] - 40, pos[1] - 34)

    def affiche(self, plateau):
        plateau.fenetre.blit(plateau.animationExplosion[int(self.image)], self.pos)
        self.image += 0.2
        if self.image >= 6:
            plateau.explosion.remove(self)
