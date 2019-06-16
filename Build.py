from math import sqrt
#test
class Build :
#test2
    #lalali je fais un test
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
            for i in range(len(listfoes)) :
                foe = listfoes[i]
                distance = sqrt(((self.posx - foe.posx)**2)+((self.posy - foe.posy)**2))
                if  distance <= self.range :
                    
                    foe.pv -= self.dmg
                    print("{} deal {} dmg to {}".format(self.name,self.dmg,foe.name))
                    print(i)
                    #super test

                    
                    if foe.isitdead():
                         listfoes.pop(i)
                    break
