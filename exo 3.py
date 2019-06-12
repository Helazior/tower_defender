from player import player

def jeu():
    pseudoj1 = input("joueur 1, quel est votre nom? ")
    pseudoj2 = input("joueur 2, quel est votre nom? ")
    if pseudoj1 == "":
        pseudoj1 = "j1"
    if pseudoj2 == "":
        pseudoj2 = "j2"
    p1 = player(pseudoj1)
    p2 = player(pseudoj2)
    print()

    for i in range(0,4,1):
        if p1.pv > 0 and p2.pv > 0 :
            p1.attack(p2)
            p2.attack(p1)
            print("{} now have {} pv\n{} now have {} pv\n".format(p1.name,p1.pv,p2.name,p2.pv))
        else:
            break

    if p1.pv == p2.pv or (p1.pv <= 0 and p2.pv <= 0):
        print("DRAW")
    elif p1.pv > p2.pv:
        print("{} win!".format(pseudoj1))
    else:
        print("{} win!".format(pseudoj2))
                  
              
jeu()
    
