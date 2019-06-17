from random import randint
direction = [(-1,0),(0,1),(1,0),(0,-1)] #haut,droite,bas,gauche

class Mob:

    def __init__(self, pygame, plateau, speed = 1, pv = 100, wasat = 3):
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
        self.speed = speed 
        self.pv = pv
        posxmax = len(plateau.Matrice[0]) #ou Plateau.nbCasesX
        posymax = len(plateau.Matrice)
        self.wasat = wasat        #le mob considere de base qu'il viens de la gauche
        #on attribue au mob une image
        mobImage = pygame.image.load("mob.png").convert_alpha()
        self.image = mobImage
        plateau.fenetre.blit(self.image, (self.posx, self.posy)) #on affiche le mob

        
    def move_to_next_pos(self, pygame, plateau):
        directiondispo = dict()
        for i in range(4):
            try:
                #on regarde tout autour du mob
                (y,x) = direction[i]
                if i == self.wasat :
                    #le mob ne peut pas reculer
                    pass
                elif plateau.Matrice[self.posymatrice + y][self.posxmatrice + x] == 3:
                    #force le mob finir si la case de fin est a coté
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
                #si il y a un IndexError, c'est que le mob regarde le coté de la map,
                #donc pas une direction valable
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
            return "mob is stuck"
                
