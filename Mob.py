from random import randint
direction = [(-1,0),(0,1),(1,0),(0,-1)] #haut,droite,bas,gauche

class Mob:

    def __init__(self, matrice , pygame ,name = "mobBase",speed = 1 ,pv = 100 ,wasat = 3):
        #on set la position initiale du mob
        for posy in range(len(matrice)):
            for posx in range(len(matrice[posy])):
                if matrice[posy][posx] == 2:
                    self.posxmatrice = posx
                    self.posymatrice = posy
                    self.posx = posx * 30
                    self.posy = posy * 30
                    break
            if matrice[posy][posx] == 2:
                #sort de la boucle s'il a trouvé
                break 
        #on set toutes les variables
        self.speed = speed 
        self.pv = pv
        self.name = name
        posxmax = len(matrice[0]) #ou Plateau.nbCasesX
        posymax = len(matrice)
        self.wasat = wasat        #le mob considere de base qu'il viens de la gauche
        #on attribue au mob une image
        mobImage = pygame.image.load("mob.png").convert_alpha()
        self.image = mobImage

        
    def move_to_next_pos(self, matrice, pygame, plateau):
        directiondispo = dict()
        for i in range(4):
            #on regarde tout autour du mob
            (y,x) = direction[i]
            if i == self.wasat :
                #le mob ne peut pas reculer
                pass
            elif matrice[self.posymatrice + y][self.posxmatrice + x] == 3:
                #force le mob finir si la case de fin est a coté
                directiondispo = {i:direction[i]} 
                print("fini")
                break
            elif matrice[self.posymatrice + y][self.posxmatrice + x] == 4:
                #force le mob a aller dans la bonne direction
                directiondispo = {i:direction[i]} 
                break
            elif matrice[self.posymatrice + y][self.posxmatrice + x] == 1:
                #crée un dictionnaire contenant toute les directions possibles
                directiondispo[i] = direction[i]
            else:
                pass
        try:
            #on choisis une direction parmis toutes celles disponibles
            randomdirection = randint(0,len(directiondispo)-1)
            goingto = list(directiondispo.keys())[randomdirection]
            (y,x) = directiondispo.get(goingto)
            #et on update toutes les variables concernées
            self.wasat = ( goingto + 2 ) % 4
            self.posxmatrice += x
            self.posymatrice += y
            self.posx = self.posxmatrice * 30
            self.posy = self.posymatrice * 30
            #enfin on deplace visuellement le mob
            plateau.fenetre.blit(self.image, (self.posx, self.posy)) #on affiche le mob

        except ValueError:
            #si il y a une ValueError, c'est qu'il n'y a pas de directions possibles, et donc le randint bug
            print(f"{self.name} is stuck at ({self.posxmatrice},{self.posymatrice})")
                
