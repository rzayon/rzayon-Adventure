import sys
sys.dont_write_bytecode = True

sys.path.insert(1, 'engines/')
sys.path.insert(2, 'modules/')

from modules import menus

class Game:

    def __init__(self):
        self.gameVersion = "0.601"

        self.nom = ""
        self.map = []
        self.deplacementHauteur = 0
        self.objets = {}

        # Vie[0] Attaque[1], Défense[2], PS[3], EXP[4], Level[5]
        self.stats = [1, 1, 1, 1, 0, 1]
        self.statsName = ["PV", "Attaque", "Défense", "PS", "EXP", "Level"]
        self.etats = {}

        # Vie Max[0], PS Max[1]
        self.statsMax = []

        # Vie[0] Attaque[1] Défense[2] Affecter Par les effets[3] Nom[4]
        self.statsEnnemi = [5, 5, 5, False, "D"]
        self.etatsEnnemi = {}

        self.parametres = {"Auto-save": "Activé",
                           "Couleur du pseudo": ["\033[1;34m", "Bleu"]}
        self.tutorielDone = {"fightFirstTime": True, "mapFirstTime": True}

player = Game()
menus.titleScreen(player, False)
