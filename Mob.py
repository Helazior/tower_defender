

class Mob:

    def __init__(self,name,posx,posy,pv):
        self.name = name
        self.posx = posx
        self.posy = posy
        self.pv = pv

    def isitdead(self):
        if self.pv <= 0 :
            print("{} is dead".format(self.name))
            return True
        else:
            return False
