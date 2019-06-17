from math import sqrt
from Mob import Mob

def convertPixelMatrice(pos):
    return (int(pos[0]/30), int(pos[1]/30))

class Build :
    def  __init__(self, pygame, plateau, pos, brange = 100, damage = 10, taille = 2):

        #charge la tour
        tour = pygame.image.load("tour.png").convert_alpha()
        self.imageTour = tour

        #affiche la tour
        posM = convertPixelMatrice(pos)
        
        plateau.fenetre.blit(plateau.copy_fond, (0, 0))
        plateau.fenetre.blit(tour, (posM[0]*30, posM[1]*30))
        
        plateau.copy_fond = pygame.display.get_surface().copy()
        self.posx = pos[0]
        self.posy = pos[1]
        self.cadence = 1
        self.range = brange
        self.damage = damage

        for i in range(taille):
            for j in range(taille):
                plateau.Matrice[posM[1]+j][posM[0]+i] = 9 #mettre images
        
    def attack(self,listMob):
        if listMob == []:
            pass
        else:
            for i in range(len(listMob)) :
                mob = listMob[i]
                distance = sqrt(((self.posx - mob.posx)**2)+((self.posy - mob.posy)**2))
                if  distance <= self.range :
                    
                    mob.pv -= self.damage
                    print(i)

                    
                    if mob.pv <= 0:
                         listMob.pop(i)
                    break
