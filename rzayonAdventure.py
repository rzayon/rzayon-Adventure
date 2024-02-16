import sys
sys.dont_write_bytecode = True

from modules import menus

class Game:

    def __init__(self):
        self.game_name = "\033[1;33m\033[4mrzayon's Adventure\033[0m"
        self.game_version = "0.6071"

        self.player_name = ""

        self.stats = [1, 1, 1, 1, 0, 1]                                         # Vie[0] Attaque[1], Défense[2], PS[3], EXP[4], Level[5], Argent[6]
        self.stats_name = ["PV", "Attaque", "Défense", "PS", "EXP", "Level"]
        self.stats_max = [1, 1]                                                 # Vie Max[0], PS Max[1]
        self.stats_boost = [0, 0]

        self.objects = {}
        self.states = {}

        self.map = []
        self.y_movement = 0
        self.tower_floor = 1

        self.stats_enemy = [5, 5, 5, False, "D"]                                # Vie[0] Attaque[1] Défense[2] Est affecter par les effets[3] Nom[4]
        self.states_enemy = {}

        self.settings = {"Auto-save": "Activé",
                         "Couleur du pseudo": ["\033[1;34m", "Bleu"]}
        self.tutorial_triggers = {"fightFirstTime": True, "mapFirstTime": True, "shopFirstTime": True}

player = Game()
menus.title_screen(player, False)