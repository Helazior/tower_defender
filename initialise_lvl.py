class lvl_1:
    vague = 0
    def __init__(self):
        self.maptxt  = "map.txt"
        self.ordreMobs = ["AppleBloom", "RainbowDash", "Scootaloo", "RainbowDash", "AppleBloom", "Scootaloo", "AppleBloom", "RainbowDash", "Scootaloo", "AppleBloom", "RainbowDash"]
        self.nbMobs = [8, 3, 20, 8, 15, 10, 10, 10, 10, 10, 10]
        self.pvMob = [30, 1, 20, 1, 45, 50, 100, 100, 100, 100, 100]
        self.tempsEntreMobs = [0.5, 1, 0.4, 0.5, 0.5, 0.1, 0.5, 0.5, 0.5, 0.5, 0.5]
        self.tempsAvantVague = [6, 6, 3, 1, 1, 0, 0, 0, 0, 0, 999] 
        self.tempsFinVague = 0
