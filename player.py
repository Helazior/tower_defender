from random import randint

class player:

    def __init__(self,name):
        self.name = name
        self.pv = 250

    def attack(self,foe):
        try:
            attempt = bool(randint(0,1))
            if attempt:
                print("{} fail to attack.".format(self.name))
            else:
                atck = randint(0,100)
                foe.pv -= atck
                print("{} attack {} for {} damage".format(self.name,foe.name,atck))
        except AttributeError:
            print("Error: foe is not a player")


            
if __name__ == "__main__":
    p1 = player("cali")
    print(p1.name)
    print(p1.pv)
    p1.attack(p1)
    
