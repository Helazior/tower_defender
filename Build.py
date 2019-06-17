from math import sqrt
from Mob import Mob

def convertPixMatrice(pos):
    return (int(pos[0]/30), int(pos[1]/30))

class Build :
    def  __init__(self, pygame, Plateau, pos, brange = 100, damage = 10, taille = 2):
        self.name = name
        self.posx = pos[0]
        self.posy = pos[1]
        self.cadence = 1
        self.range = brange
        self.damage = damage

        for i in range(taille):
            for j in range(taille):
                Plateau.Matrice[j][i] = 9 #mettre images

    def attack(self,listMob):
        if listMob == []:
            pass
        else:
            for i in range(len(listMob)) :
                mob = listMob[i]
                distance = sqrt(((self.posx - mob.posx)**2)+((self.posy - mob.posy)**2))
                if  distance <= self.range :
                    
                    mob.pv -= self.damage
                    print(f"{self.name} deal {self.damage} damage to {mob.name}")
                    print(i)

                    
                    if mob.pv <= 0:
                         listMob.pop(i)
                    break
