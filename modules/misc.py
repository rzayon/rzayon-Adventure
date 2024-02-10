import os
import time
import sys
import keyboard

import audioEngine

# Save Misc
def closeRemove(file, saveTemp):
    file.close()
    os.remove(saveTemp)


# Battle Misc
def estMort(player):
    if player.stats[0] <= 0:
        return True
    else:
        return False

def verifStats(player):
    # Check PV
    if player.stats[0] > player.statsMax[0]:
        player.stats[0] = player.statsMax[0]
    elif player.stats[0] < 0:
        player.stats[0] = 0

    # Check PS
    if player.stats[3] > player.statsMax[1]:
        player.stats[3] = player.statsMax[1]
    elif player.stats[3] < 0:
        player.stats[3] = 0

def checkLifeWarning(player):
    if 2 < player.stats[0] < 7:
        return f"\033[1;33m{player.stats[0]}\033[0m"
    elif player.stats[0] < 2:
        return f"\033[1;31m⚠️ {player.stats[0]}\033[0m"
    else:
        return player.stats[0]

def rainbowText(texte):
    couleurs = ['\033[1;31m', '\033[1;33m', '\033[1;32m' '\033[1;36m', '\033[1;34m', '\033[1;35m']
    resetCoulor = '\033[0m'

    texteFinal = ""

    for charactere, couleur in zip(texte, couleurs * (len(texte) // len(couleurs) + 1)):
        texteFinal += couleur + charactere + resetCoulor

    return texteFinal

def regen(player):
    player.stats[0] = player.statsMax[0]
    player.stats[3] = player.statsMax[1]


# Menu Misc
def dialogue():
    keyboard.wait('space', suppress = True)
    audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)

def transitionMenu(temps):
    audioEngine.musicFadeOut(temps * 1000)
    time.sleep(temps)

def fermerJeu():
    print()
    audioEngine.musicFadeOut(3000)
    for point in range(0, 4):
        print("Vous allez quitter le jeu" + ("." * point), end = "")
        time.sleep(0.75)
        sys.stdout.write("\r")
    sys.exit()


    #TEMPO

'''def objet(self, obj, ennemi):
        if obj == "Champignon":
            self.stats[0] += 10
            misc.verifMaxStats(self)
            print("Vous avez regagner 10PV.")
        elif obj == "Pierre":
            ennemi[0] -= 1
            print("Vous avez enlever 1PV a l'ennemi. Ce n'est pas très efficace...")
        elif obj == "Fleur de feu":
            ennemi[0] -= 10
            bruleRNG = random.random()
            if bruleRNG > 0.2:
                print("Vous avez enlever 10PV a l'ennemi. C'est très efficace!")
            else:
                ennemi[3] = True
                print("Vous avez enlever 10PV a l'ennemi. C'est très efficace! L'ennemi est en feu")'''