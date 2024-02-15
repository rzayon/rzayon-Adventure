""" Module contenant des fonctions et variables utiles pour le jeu. """


import os
import time
import sys
import keyboard

from engines import audio_engine

# Save Misc
def close_remove(file, saveTemp):
    file.close()
    os.remove(saveTemp)


# Battle Misc
def is_dead(player):
    if player.stats[0] <= 0:
        return True
    else:
        return False

def check_stats(player):
    # Check PV
    if player.stats[0] > player.stats_max[0]:
        player.stats[0] = player.stats_max[0]

    # Check PS
    if player.stats[3] > player.stats_max[1]:
        player.stats[3] = player.stats_max[1]
    elif player.stats[3] < 0:
        player.stats[3] = 0

def check_life_warning(player):
    if 2 < player.stats[0] <= 7:
        return f"\033[1;33m{player.stats[0]}\033[0m"
    elif player.stats[0] <= 2:
        return f"\033[1;31m⚠️ {player.stats[0]}\033[0m"
    else:
        return player.stats[0]

def rainbow_text(texte):
    couleurs = ['\033[1;31m', '\033[1;33m', '\033[1;32m' '\033[1;36m', '\033[1;34m', '\033[1;35m']
    resetCoulor = '\033[0m'

    texteFinal = ""

    for charactere, couleur in zip(texte, couleurs * (len(texte) // len(couleurs) + 1)):
        texteFinal += couleur + charactere + resetCoulor

    return texteFinal

def regen(player):
    player.stats[0] = player.stats_max[0]
    player.stats[3] = player.stats_max[1]


# Menu Misc
def dialogue():
    keyboard.wait('space', suppress = True)
    audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)

def menu_transition(temps):
    audio_engine.music_fade_out(temps * 1000)
    time.sleep(temps)

def close_game():
    print()
    audio_engine.music_fade_out(3000)
    for point in range(0, 4):
        print("Vous allez quitter le jeu" + ("." * point), end = "")
        time.sleep(0.75)
        sys.stdout.write("\r")
    sys.exit()