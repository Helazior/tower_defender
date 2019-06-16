from random import randint
direction = [(-1,0),(0,1),(1,0),(0,-1)]

class Mob:

    def __init__(self ,matrice ,name = "mobBase",speed = 100 ,pv = 100 ,wasat = 3):
        self.matrice = matrice #le mob a en memoire la map, y'a surement mieux en vrai
        for posy in range(len(matrice)):
            for posx in range(len(matrice[posy])):
                if matrice[posy][posx] == 2:
                    self.posxmatrice = posx
                    self.posymatrice = posy
                    self.posx = posx * 30 + 15
                    self.posy = posy * 30 + 15
        self.speed = speed 
        self.pv = pv
        self.name = name
        posxmax = len(matrice[0])
        posymax = len(matrice)
        self.wasat = wasat
        
    def move_to_next_pos(self):
        directiondispo = dict()
        for i in range(4):
            (y,x) = direction[i]
            if i == self.wasat :
                pass
            elif self.matrice[self.posymatrice + y][self.posxmatrice + x] == 3:
                self.posxmatrice += x
                self.posymatrice += y
                self.posx = self.posxmatrice * 30 - 15
                self.posy = self.posymatrice * 30 - 15
                #self.finnishthematrice
            elif self.matrice[self.posymatrice + y][self.posxmatrice + x] == 1:
                directiondispo[i] = direction[i]
            else:
                pass
        try:
            randomdirection = randint(0,len(directiondispo)-1)
            (y,x) = list(directiondispo.values())[randomdirection]
            self.posxmatrice += x
            self.posymatrice += y
            self.posx = self.posxmatrice * 30 - 15
            self.posy = self.posymatrice * 30 - 15
            wasat = list(directiondispo.keys())[randomdirection]     
        except ValueError:
            print(f"{self.name} is stuck at ({self.posxmatrice},{self.posymatrice})")
                
