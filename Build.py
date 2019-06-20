from math import sqrt
from time import time
from Mob import Mob

import pygame

def convertPixelMatrice(pos):
    return (int(pos[0]/30), int(pos[1]/30))

class Build :
    def  __init__(self, plateau, pos, brange = 200, damage = 10, taille = 2, attenteTir = 0.5):

        #charge la tour
        tour = pygame.image.load("tour.png").convert_alpha()
        self.imageTour = tour

        #affiche la tour
        posM = convertPixelMatrice(pos)
        
        plateau.fenetre.blit(plateau.copy_fond, (0, 0))
        plateau.fenetre.blit(tour, (posM[0]*30, posM[1]*30))
        
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
        
    def attack(self, plateau, listeMob, listeDyingMob):
        if listeMob == []:
            pass
        else:
            if time() - self.tempsDernierTir >= self.attenteTir: #attente d'une seconde avant de retirer
                self.tempsDernierTir = time()
                for posliste in range(len(listeMob)) :
                    mob = listeMob[posliste]
                    distance = sqrt(((self.posx - mob.posx + 15)**2)+((self.posy - mob.posy + 15)**2))
                    if  distance <= self.range :
                        self.tir(plateau, (self.posx, self.posy), (mob.posx + 15, mob.posy + 15)) #annimation du tir
                        mob.pv -= self.damage
                        print(f"Mob {posliste} touché, lui reste {mob.pv} pv")

                        mob.is_it_dying(listeMob, posliste, listeDyingMob)

                        break



    #________________________staticmethod_______________________

    @staticmethod
    def tir(plateau, posTour, porMob):
        red = (255,0,0)
        pygame.draw.line(plateau.fenetre, red, posTour, porMob) #fait un trait rouge de la tour jusqu'au mob


    @staticmethod
    def set_up(plateau, pos, taille, listeTour):
        (x,y) = pos
        pos = (x - 15*(taille - 1) , y - 15*(taille - 1)) #pour que le clique soit centré par rapport a la tour qu'il fait apparaitre
        posMatrice = convertPixelMatrice(pos)
        conditionSolVide = True
        try:
            for i in range(taille):
                for j in range(taille):
                    (y, x) = (posMatrice[1] + i , posMatrice[0] + j)
                    if plateau.Matrice[y][x] != 0 :
                        conditionSolVide = False
                        break             
        except IndexError:
            #si il y a une index error c'est qu'on est en dehors de la matrice
            conditionSolVide = False

        if conditionSolVide:
            listeTour.append(Build(plateau, pos)) #création de la tour