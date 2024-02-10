import time

import audioEngine
import battle
import misc

def tower(player):
    entrer = input("Vous êtes arrivé a une tour. Voulez vous y entrer ? (O/N) ").upper()
    while entrer != "O" and entrer != "N":
        audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
        entrer = input("Réponse incorrecte. Voulez vous entrer dans la tour ? (O/N) ").upper()

    etage = 1
    if entrer == "O":
        audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 2)
        misc.transitionMenu(1.5)
        while etage < 11:
            time.sleep(0.5)
            chooseTowerBoss(player, etage)
            audioEngine.sfxPlay("ressources/sfx/bossStart.ogg", 4)
            time.sleep(2)

            print(f"\033[1;31mVS {player.statsEnnemi[4]}\033[0m !")

            audioEngine.sfxPlay("ressources/sfx/bossStartRideau.ogg", 2)
            time.sleep(1.5)

            if battle.fight(player, f"ressources/mboss{etage}.mp3") == True:
                etage += 1
            else:
                return False

            if etage == 11:
                print("Bravo ! Vous avez éléminé les monstres de la tour !")
                return True

def chooseTowerBoss(player, currentEtage):
    listeBoss = {1: [40, 15, 15, True, "\033[1;31mLithorok\033[0m"],
                 2: [65, 25, 25, True, "\033[1;31mHinox\033[0m"],
                 3: [85, 40, 30, True, "\033[1;31mFury Bowser\033[0m"],
                 4: [115, 65, 45, True, "\033[1;31mFlowey\033[0m"],
                 5: [135, 85, 60, False, "\033[1;31mBowser\033[0m"],
                 6: [175, 110, 75, False, "\033[1;31mToriel\033[0m"],
                 7: [210, 130, 90, True, "\033[1;31mLobotomy Face\033[0m"],
                 8: [240, 150, 105, False, "\033[1;31mDimensio\033[0m"],
                 9: [280, 170, 120, False, "\033[1;31mNiark\033[0m"],
                 10: [325, 190, 140, False, "\033[1;31mAntasma\033[0m"]}

    for boss in listeBoss.keys():
        if boss == currentEtage:
            player.statsEnnemi = listeBoss[boss]
            print(f"\n\033[1;1mVous êtes a l'étage {currentEtage}.\033[0m")