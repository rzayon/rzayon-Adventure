import random
import time

import audioEngine
import misc

# Ajout d'EXP
def exp(player, vieEnnemi):
    expMultiplicateur = random.uniform(1.2, 1.5)
    player.stats[4] += int(expMultiplicateur * (vieEnnemi / 1.5))
    return int(expMultiplicateur * (vieEnnemi / 2))

# Check changment de level
def levelCheck(player):

    firstUpgrade = True
    newLevel = player.stats[5]
    levels = {2: 50, 3: 125, 4: 250, 5: 400, 6: 650, 7: 800, 8: 1000, 9: 1250, 10: 1700, 11: 2000, 12: 2500, 13: 3200, 14: 4000, 15: 4600, 16: 5250}
    ameliorationInfo = {"pv": 0, "att": 1, "déf": 2, "ps": 3}
    choixAmelioration = False

    for level, experience in reversed(levels.items()):
        if player.stats[4] >= experience and player.stats[5] <= level and newLevel == player.stats[5]:
            newLevel = level

    while player.stats[5] != newLevel:
        if newLevel != player.stats[5]:
            player.stats[5] += 1
            audioEngine.musicPlay("ressources/levelUp.mp3")
            print("\t\t\033[1;32m\033[1;1m\033[4mVous êtes passer niveau", player.stats[5], "!\033[0m")

            if firstUpgrade == True:
                time.sleep(6.25)
                firstUpgrade = False
            else:
                time.sleep(1.5)

            amelioration = input("Quel stat voulez vous plus améliorer ? (\033[1;95mPV\033[0m/\033[1;31mAtt\033[0m/\033[1;32mDéf\033[0m/\033[1;33mPS\033[0m) ").lower()

            while choixAmelioration == False:
                for stat in ameliorationInfo.keys():
                    if amelioration == stat:
                        amelioration = ameliorationInfo[stat]
                        choixAmelioration = True
                if choixAmelioration == False:
                    audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
                    amelioration = input("Réponse incorrecte. Quel stats voulez vous plus améliorer ? (\033[1;95mPV\033[0m/\033[1;31mAtt\033[0m/\033[1;32mDéf\033[0m/\033[1;33mPS\033[0m) ").lower()

        audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)
        ameliorationStat(player, amelioration)
        audioEngine.sfxPlay("ressources/sfx/fullRegen.ogg", 3)

        print("\033[1mPV et PS régéneré !\033[0m\n")

        time.sleep(1.5)
        misc.transitionMenu(3)

# Amélioration des stats
def ameliorationStat(player, indiceStat):

    changeStatsLog = "\n"
    for i in range (0, 4):
        if i == indiceStat:
            player.stats[i] += 10
            if i == 0:
                player.statsMax[0] += 10
            elif i == 3:
                player.statsMax[1] += 10
        else:
            player.stats[i] += 5
            if i == 0:
                player.statsMax[0] += 5
            elif i == 3:
                player.statsMax[1] += 5

    misc.regen(player)

    for i in range(0, 4):
        if i == indiceStat:
            changeStatsLog += player.statsName[i] + " \033[1;31m+ 10\033[0m\n"
        else:
            changeStatsLog += player.statsName[i] + " \033[1;32m+ 5\033[0m\n"

    audioEngine.sfxPlay("ressources/sfx/levelUpSfx.ogg", 2)
    print(changeStatsLog)