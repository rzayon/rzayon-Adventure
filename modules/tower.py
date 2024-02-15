import time

from engines import audio_engine

from modules import battle
from modules import misc

def tower(player):
    entrer = input("Vous êtes arrivé a une tour. Voulez vous y entrer ? (O/N) ").upper()
    while entrer != "O" and entrer != "N":
        audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
        entrer = input("Réponse incorrecte. Voulez vous entrer dans la tour ? (O/N) ").upper()

    if player.tower_floor <= 0:
        player.tower_floor = 1

    if entrer == "O":
        audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 2)
        misc.menu_transition(1.5)
        while player.tower_floor < 11:
            time.sleep(0.5)
            choose_tower_boss(player, player.tower_floor)
            audio_engine.sfx_play("ressources/sfx/bossStart.ogg", 4)
            time.sleep(2)

            print(f"\033[1;31mVS {player.stats_enemy[4]}\033[0m !")

            audio_engine.sfx_play("ressources/sfx/bossStartRideau.ogg", 2)
            time.sleep(1.5)

            if battle.fight(player, f"ressources/mboss{player.tower_floor}.mp3") == True:
                player.tower_floor += 1
            else:
                return False

            if player.tower_floor == 11:
                print("Bravo ! Vous avez éléminé les monstres de la tour !")
                return True

def choose_tower_boss(player, currentEtage):
    listeBoss = {1: [40, 15, 15, True, "\033[1;31mLithorok\033[0m"],
                 2: [65, 20, 25, True, "\033[1;31mHinox\033[0m"],
                 3: [85, 35, 30, True, "\033[1;31mFury Bowser\033[0m"],
                 4: [115, 55, 45, True, "\033[1;31mFlowey\033[0m"],
                 5: [135, 70, 60, False, "\033[1;31mBowser\033[0m"],
                 6: [175, 90, 75, False, "\033[1;31mToriel\033[0m"],
                 7: [210, 115, 90, True, "\033[1;31mLobotomy Face\033[0m"],
                 8: [240, 130, 105, False, "\033[1;31mDimensio\033[0m"],
                 9: [280, 155, 120, False, "\033[1;31mNiark\033[0m"],
                 10: [325, 175, 140, False, "\033[1;31mAntasma\033[0m"]}

    for boss in listeBoss.keys():
        if boss == currentEtage:
            player.stats_enemy = listeBoss[boss]
            print(f"\n\033[1;1mVous êtes a l'étage {currentEtage}.\033[0m")