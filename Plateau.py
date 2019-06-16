def initFenetre(Plateau, pygame): #crée et affiche la fenêtre
    pygame.display.set_caption("Tower Defender !")
    fenetre = pygame.display.set_mode(Plateau.tailleFenetre, pygame.RESIZABLE)

    #je charge et convertis les images dans des variables
    fond = pygame.image.load("fond.png").convert()
    chemin = pygame.image.load("chemin.png").convert()
    start = pygame.image.load("start.png").convert_alpha()
    end = pygame.image.load("end.png").convert_alpha()


    fond = pygame.transform.scale(fond, Plateau.tailleFenetre) #l'image de fond fait la taille de la fenêtre
    fenetre.blit(fond, (0,0)) #affiche le fond à la position (0,0)
    for i in range(Plateau.nbCasesX):
        for j in range(Plateau.nbCasesY):
            if Plateau.Matrice[j][i] != 0:
                fenetre.blit(chemin, (30*i,30*j)) #on place un chemin quand c'est pas le fond
            if Plateau.Matrice[j][i] == 2:
                fenetre.blit(start, (30*i,30*j)) #on place le start
            elif Plateau.Matrice[j][i] == 3:
                fenetre.blit(end, (30*i,30*j))  #on place l'arrivé des mobs

    fenetre_fond = pygame.display.get_surface().copy() #Copie du fond pour faire bouger les trucs devant

    pygame.display.flip() #rafraichit l'image !




def creationMatrice(tailleFenetre, nbCasesX, nbCasesY):
    Matrice = [0]*nbCasesY #on met des O sur toute la hauteur de la future matrice
    for i in range (nbCasesY):
        Matrice[i] = [0]*nbCasesX
        #on crait la matrice de la map avec des 0

    #On fait la map à partir du fichier texte
    with open("map.txt","r") as fichier:    #ouverture du fichier texte
        texte_grille = fichier.read()
        liste_grille = texte_grille.split("\n") #On fait une liste du fichier texte, qui sséparée à chaque saut à la ligne

        for i in range(nbCasesX):
            for j in range(nbCasesY):
                Matrice[j][i] = int(liste_grille[j][i])
                
    return Matrice
    




class Plateau: #classe de la map attributs: Matrice, nbCasesX, nbCasesY, tailleFenetre

    def __init__(self):
        nbCasesX = 41
        nbCasesY = 21
        tailleFenetre = (nbCasesX*30 + 50,nbCasesY*30 + 50)
        
        self.nbCasesX = nbCasesX
        self.nbCasesY = nbCasesY
        self.tailleFenetre = tailleFenetre
        
        self.Matrice = creationMatrice(tailleFenetre, nbCasesX, nbCasesY)
        
