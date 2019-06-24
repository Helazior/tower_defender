from pygame.locals import *
from random import randint
from time import *
import pygame

#direction sert pour bouger les mobs
direction = [(-1,0),(0,1),(1,0),(0,-1)] #haut,droite,bas,gauche

class Mob:

    def __init__(self, plateau, speed = 1, pv = 100, wasat = 3, dying = 10):
        #on set la position initiale du mob
        for posy in range(len(plateau.Matrice)):
            for posx in range(len(plateau.Matrice[posy])):
                if plateau.Matrice[posy][posx] == 2:
                    self.posxmatrice = posx
                    self.posymatrice = posy
                    self.posx = posx * 30
                    self.posy = posy * 30
                    break
            if plateau.Matrice[posy][posx] == 2:
                #sort de la boucle s'il a trouvé
                break 
        #on set toutes les variables
        self.speed = 30 * (1/speed)
        self.pv = pv
        posxmax = len(plateau.Matrice[0]) #ou Plateau.nbCasesX
        posymax = len(plateau.Matrice)
        self.wasat = wasat        #le mob considere de base qu'il viens de la gauche
        self.dying = dying
        
    def move_to_next_pos(self, plateau):
        directiondispo = dict()
        if self.posx % 30 == 0 and self.posy % 30 == 0:
            try:
                for i in range(4):
                    #on regarde tout autour du mob
                    (y,x) = direction[i]
                    if i == self.wasat :
                        #le mob ne peut pas reculer
                        pass
                    elif plateau.Matrice[self.posymatrice + y][self.posxmatrice + x] == 3:
                        #force le mob a finir si la case de fin est a coté
                        directiondispo = {i:direction[i]}
                        break
                    elif plateau.Matrice[self.posymatrice + y][self.posxmatrice + x] == 4:
                        #force le mob a aller dans la bonne direction
                        directiondispo = {i:direction[i]} 
                        break
                    elif plateau.Matrice[self.posymatrice + y][self.posxmatrice + x] == 1:
                        #crée un dictionnaire contenant toute les directions possibles
                        directiondispo[i] = direction[i]
                    else:
                        pass
            except IndexError:
                #si il y a un IndexError, c'est que le mob regarde le coté de la map, donc pas une direction valable
                pass
        else:
            directiondispo = {(self.wasat + 2) % 4 : direction[(self.wasat + 2) % 4]}
        
        try:
            #on choisis une direction parmis toutes celles disponibles
            randomdirection = randint(0,len(directiondispo)-1)
            goingto = list(directiondispo.keys())[randomdirection]
            (y,x) = directiondispo.get(goingto)
            #et on update toutes les variables concernées
            self.wasat = ( goingto + 2 ) % 4
            self.posx = self.posx + (x * self.speed)
            self.posy = self.posy + (y * self.speed)
            self.posxmatrice = int(self.posx / 30)
            self.posymatrice = int(self.posy / 30)
            #enfin on deplace visuellement le mob
            plateau.fenetre.blit(self.aliveSkin, (self.posx, self.posy)) #on affiche le mob

        except ValueError:
            #si il y a une ValueError, c'est qu'il n'y a pas de directions possibles, et donc le randint bug
            return "mob is stuck"
        
    def is_it_dying(self, listeMob, posliste, listeDyingMob):
        if self.pv <= 0:
            listeMob.pop(posliste)
            listeDyingMob.append(self)
            

    def is_dying(self, plateau):
        if self.dying > 0 :
            plateau.fenetre.blit(self.dyingSkin, (self.posx, self.posy))
        else:
            return "mob is dead"
        self.dying -= 1


    #_______________________Fonctions statiques_________________________
    @staticmethod
    def spawnmobs(plateau, listeMob):
        randomponey = randint(0,2)
        if randomponey == 0:
            listeMob.append(Scootaloo(plateau))
        elif randomponey == 1:
            listeMob.append(AppleBloom(plateau))
        else:
            listeMob.append(SweetieBelle(plateau))
        return time()

    @staticmethod
    def movemobs(plateau, listeMob):
        temp = 0
        while temp < len(listeMob):
            newPosMob = listeMob[temp].move_to_next_pos(plateau)
            if newPosMob == "mob is stuck":
                #si le mob est bloqué on le supprime pour l'instant
                listeMob.pop(temp)
                temp -= 1
            temp += 1


    @staticmethod
    def killmobs(plateau, listeDyingMob):
        temp = 0
        while temp < len(listeDyingMob):
            etatMob = listeDyingMob[temp].is_dying(plateau)
            if etatMob == "mob is dead":
                #si le mob est mort on le supprime de la liste
                listeDyingMob.pop(temp)
                temp -= 1
            temp += 1


#____________________________Sous classes de Mob________________________

class Scootaloo(Mob):

    def __init__(self, plateau):
        Mob.__init__(self, plateau, speed = 3, pv = 25)

        self.type = "earth"
        
        #on attribue au mob une image et on l'affiche
        self.aliveSkin = pygame.image.load("scootalooAlive.png").convert_alpha()
        self.dyingSkin = pygame.image.load("scootalooDying.png").convert_alpha()
        plateau.fenetre.blit(self.aliveSkin, (self.posx, self.posy)) 
        

class AppleBloom(Mob):

    def __init__(self, plateau):
        Mob.__init__(self, plateau, speed = 6, pv = 75)

        self.type = "earth"
        
        #on attribue au mob une image et on l'affiche
        self.aliveSkin = pygame.image.load("applebloomAlive.png").convert_alpha()
        self.dyingSkin = pygame.image.load("applebloomDying.png").convert_alpha()
        plateau.fenetre.blit(self.aliveSkin, (self.posx, self.posy)) 

        
class SweetieBelle(Mob):
    def __init__(self, plateau):
        Mob.__init__(self, plateau, speed = 5, pv = 50)

        self.type = "earth" #magic?
        
        #on attribue au mob une image et on l'affiche
        self.aliveSkin = pygame.image.load("sweetiebelleAlive.png").convert_alpha()
        self.dyingSkin = pygame.image.load("sweetiebelleDying.png").convert_alpha()
        plateau.fenetre.blit(self.aliveSkin, (self.posx, self.posy)) 


















    
