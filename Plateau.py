from random import randint

def initFenetre(pygame, nbCasesX, nbCasesY, tailleFenetre, Matrice): #crée et affiche la fenêtre
    pygame.display.set_caption("Tower Defender !")

    fenetre = pygame.display.set_mode(tailleFenetre)

    #je charge et convertis les images dans des variables
    fond = pygame.image.load("fond.png").convert()
    fond2 = pygame.image.load("fond2.png").convert()
    chemin = pygame.image.load("chemin.png").convert()
    start = pygame.image.load("start.png").convert_alpha()
    end = pygame.image.load("end.png").convert_alpha()
    imageStalker = pygame.image.load("stalker.png").convert_alpha()
    imageStalkerMenu = pygame.image.load("stalkerMenu.png").convert_alpha()
    imageSentry = pygame.image.load("sentry.png").convert_alpha()
    imageSentryMenu = pygame.image.load("sentryMenu.png").convert_alpha()
    imageTank = pygame.image.load("tank.png").convert_alpha()
    imageTankMenu = pygame.image.load("tankMenu.png").convert_alpha()

    fondMenu = pygame.image.load("fondMenu.png").convert_alpha()

    fenetre.blit(pygame.transform.scale(fondMenu, (1280, 680)), (0, 0))

    fenetre.blit(imageStalkerMenu, (1200, 100))
    fenetre.blit(imageSentryMenu, (1200, 200))
    fenetre.blit(imageTankMenu, (1200, 300))

    for i in range(nbCasesX):
        for j in range(nbCasesY):
            if Matrice[j][i] != 0:
                fenetre.blit(chemin, (30*i, 30*j)) #on place un chemin quand c'est pas le fond
            else:
                if (i+j)%2:
                    fenetre.blit(fond, (30*i, 30*j))
                else:
                    fenetre.blit(fond2, (30*i, 30*j))
            if Matrice[j][i] == 2:
                fenetre.blit(start, (30*i, 30*j)) #on place le start
            elif Matrice[j][i] == 3:
                fenetre.blit(end, (30*i, 30*j))  #on place l'arrivé des mobs

    pygame.display.flip() #rafraichit l'image !

    copy_fond = pygame.display.get_surface().copy() #Copie du fond pour faire bouger les trucs devant
    return fenetre, copy_fond, imageStalker, imageSentry, imageTank



def creationMatrice(tailleFenetre, nbCasesX, nbCasesY, fileName):
    Matrice = [0]*nbCasesY #on met des O sur toute la hauteur de la future matrice
    for i in range (nbCasesY):
        Matrice[i] = [0]*nbCasesX
        #on crait la matrice de la map avec des 0

    #On fait la map à partir du fichier texte
    with open(fileName,"r") as fichier:    #ouverture du fichier texte
        texte_grille = fichier.read()
        liste_grille = texte_grille.split("\n") #On fait une liste du fichier texte, qui sséparée à chaque saut à la ligne

        messageErreur = False
        for i in range(nbCasesX):
            for j in range(nbCasesY):
                try:
                    Matrice[j][i] = int(liste_grille[j][i])
                except:
                    if not(messageErreur):
                        if texte_grille == "":
                            print("Nouvelle map")
                        else:
                            print("ERROR: fichier txt de mauvaise dim")
                        messageErreur = 1
                
    return Matrice
    




class Plateau: #classe de la map attributs: Matrice, nbCasesX, nbCasesY, tailleFenetre, fenetre

    def __init__(self, pygame, fileName):
        nbCasesX = 40
        nbCasesY = 20
        tailleFenetre = (nbCasesX*30 + 80,nbCasesY*30 + 80)
        
        self.nbCasesX = nbCasesX
        self.nbCasesY = nbCasesY
        self.tailleFenetre = tailleFenetre
        Matrice = creationMatrice(tailleFenetre, nbCasesX, nbCasesY, fileName)
        self.Matrice = Matrice

        margeFenetreGauche = 15
        margeFenetreHaut = 15
        
        self.fenetre, self.copy_fond, self.imageStalker, self.imageSentry, self.imageTank  = initFenetre(pygame, nbCasesX, nbCasesY,tailleFenetre, Matrice)
