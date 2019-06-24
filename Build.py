from math import sqrt
from time import time
from Mob import *

import pygame

def convertPixelMatrice(pos):#à mettre dans plateau je pense, mais faudra importer plateau après
    return (int(pos[0]/30), int(pos[1]/30))

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
                plateau.Matrice[posM[1]+j][posM[0]+i] = 9 #mettre images
        

    def attack(self, plateau, listeMob, listeDyingMob, listeMobPriorityTarget):
        if listeMob == []:
            pass
        else:
            if time() - self.tempsDernierTir >= self.attenteTir: #attente avant de retirer
                listeMobAndPriority = listeMobPriorityTarget + listeMob # listeMobPriorityTarget devant sera lue en première
                for posInListe in range(len(listeMobAndPriority)) :
                    mob = listeMobAndPriority[posInListe]
                    distance = sqrt(((self.posx - mob.posx + 15)**2)+((self.posy - mob.posy + 15)**2))
                    if  distance <= self.range :
                        self.tempsDernierTir = time()
                        self.tir(plateau, (self.posx, self.posy), (mob.posx + 15, mob.posy + 15)) #annimation du tir
                        mob.pv -= self.damage
                        #print(f"Mob {posInListe} touché, lui reste {mob.pv} pv")

                        mob.is_it_dying(listeMob, posInListe - len(listeMobPriorityTarget) , listeDyingMob)
                        if mob.pv <= 0:
                            try:
                                listeMobPriorityTarget.pop(posInListe)
                            except:
                                pass
                        break



    #________________________staticmethod_______________________

    @staticmethod
    def tir(plateau, posTour, porMob):
        red = (255,0,0)
        pygame.draw.line(plateau.fenetre, red, posTour, porMob, 3) #fait un trait rouge de la tour jusqu'au mob, 3 est la grosseur


    @staticmethod
    def set_up(plateau, pos, dicoTour):
        (x,y) = pos
        if x > 15 and y > 15:
            taille = Tour.taille
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
                #si il y a une index error c'est qu'on est en dehors de la matrice
                freeSpace = False

            if freeSpace:
                posx = pos[0] // 30 * 30 + 15*Tour.taille
                posy = pos[1] // 30 * 30 + 15*Tour.taille
                dicoTour[(posx,posy)] = Tour(plateau, pos) #création de la tour#bug du tir décalé lorsqu'on met la tour tout au bord à corriger (rajouter condition)

    @staticmethod
    def is_build(plateau, pos, dicoTour):
        posx = (pos[0] - 15) // 30 * 30 + 15*Tour.taille  #ne marche pas pour taille > 2 et il faut viser pile le carré
        posy = (pos[1] - 15) // 30 * 30 + 15*Tour.taille
        pos = (posx,posy)
        try:
            dicoTour[pos]
            return True, pos
        except:
            return False, pos

    @staticmethod
    def info_build(plateau, pos, dicoTour):
        white = (200,200,200)
        pygame.draw.circle(plateau.fenetre, white, pos, dicoTour[pos].range, 1)
        #pygame.display.flip()



class Tour(Build):
    """docstring for tour"""
    taille = 2

    def __init__(self, plateau, pos, brange = 200, damage = 10, attenteTir = 0.5):

        imageTour = pygame.image.load("tour.png").convert_alpha()
        self.imageTour = imageTour
        Build.__init__(self, plateau, pos, brange, damage, Tour.taille, attenteTir, imageTour)
