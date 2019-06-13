from math import sqrt

class Build :

    def  __init__(self,name,posx,posy,brange,damage):
        self.name = name
        self.posx = posx
        self.posy = posy
        self.ticsincelastaction = 1
        self.range = brange
        self.dmg = damage

    def attack(self,listfoes):
        if listfoes == []:
            pass
        else:
            for foe in listfoes :
                    distance = sqrt(((self.posx - foe.posx)**2)+((self.posy - foe.posy)**2))
                    if  distance <= self.range :
                        foe.pv -= self.dmg
                        print("{} deal {} dmg to {}".format(self.name,self.dmg,foe.name))
                        foe.isitdead()
                        break