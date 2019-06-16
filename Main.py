from random import randint
from Mob import Mob
from Build import Build

mobliste = []

for i in range(30):
    posx = randint(0,100)
    posy = randint(0,100)
    name = "mobtest"
    mobliste.append(Mob(name,posx,posy,20))
    
Tower = Build("Tower",50,50,30,20)

print(len(mobliste))
Tower.attack(mobliste)
print(len(mobliste))

#trop bien
