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
                        print(f"Mob numéro {posliste} a été touché, il lui reste {mob.pv} pv")

                        mob.is_it_dying(listeMob, posliste, listeDyingMob)

                        break




    @staticmethod
    def tir(plateau, posTour, porMob):
        print(posTour)
        red = (255,0,0)
        pygame.draw.line(plateau.fenetre, red, posTour, porMob) #fait un trait rouge de la tour jusqu'au mob
        pygame.display.flip()  #rafraichit