""" Module gérant le système de combat du jeu. """

import random
import time
import sys
import keyboard

from engines import audio_engine

from modules import settings
from modules import menus
from modules import tutorials
from modules import objects
from modules import level_xp
from modules import states_effects
from modules import misc

def fight(player, musicBattle):

    states_effects.reset_state(player)
    vieEnnemiTempo = player.stats_enemy[0]

    print()

    while player.stats[0] > 0 and player.stats_enemy[0] > 0:

        fightActionDone = False

        while fightActionDone == False:
            audio_engine.music_play(musicBattle)
            print(f"{settings.display_name_color(player)}\n{misc.check_life_warning(player)} \033[1;95mPV\033[0m | {player.stats[3]} \033[1;33mPS\033[0m\n" +
                (states_effects.display_effects(player.states) if states_effects.display_effects(player.states) != False else ""))
            print("\033[1;1mVS\033[0m\n")
            print(f"\033[37m{player.stats_enemy[4]}\033[0m" + (" " + states_effects.display_effects(player.states_enemy) if states_effects.display_effects(player.states_enemy) != False else " ") + f"\n\033[1;95mPV:\033[0m {player.stats_enemy[0]}\n\033[1;31mAtt:\033[0m {player.stats_enemy[1]}\n")

            low_hp_detect(player)
            attaqueTrigger = input("\033[1;31mAttaquer (A)\033[0m / \033[1;32mObjets (O)\033[0m / \033[1;33mSpécial (S) [WIP]\033[0m / \033[1;36mFuir (F)\033[0m / \033[37mNe rien faire (R)\033[0m ").upper()

            while attaqueTrigger != "A" and attaqueTrigger != "O" and attaqueTrigger != "S" and attaqueTrigger != "F" and attaqueTrigger != "R":
                audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
                attaqueTrigger = input("\033[1;31mAttaquer (A)\033[0m / \033[1;32mObjets (O)\033[0m / \033[1;33mSpécial (S) [WIP]\033[0m / \033[1;36mFuir (F)\033[0m / \033[37mNe rien faire (R)\033[0m ").upper()

            if attaqueTrigger == "A":
                audio_engine.sfx_stop(3)
                audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)

                if tutorials.fight_tutorial(player) == True:
                    tutorials.fight_tutorial(player)

                    audio_engine.music_play(musicBattle)
                    attaqueRandom = int((player.stats[1] - player.stats_enemy[2]) * random.uniform(1.5, 1.9))
                    player.stats_enemy[0] -= attaqueRandom
                    print(f"\nVous avez mis \033[1;31m{attaqueRandom}\033[0m de dégats à l'ennemi.")

                else:
                    print(f"\nVous avez mis \033[1;31m{player_attaque(player)}\033[0m de dégats à l'ennemi.")

                time.sleep(2)
                fightActionDone = True

            elif attaqueTrigger == "O":
                audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
                if menus.objects_menu(player, True) == True:
                    fightActionDone = True
                    time.sleep(2)
                else:
                    print()

            elif attaqueTrigger == "S":
                audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
                if special_attack(player) == True:
                    fightActionDone = True

            elif attaqueTrigger == "F":
                fightActionDone = True
                if flee() == True:
                    return False

            elif attaqueTrigger == "R":
                audio_engine.sfx_stop(3)
                fightActionDone = True
                audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
                nothing()

                time.sleep(1)

        states_effects.detect_state(player)

        if player.stats_enemy[0] > 0:
            print(f"{player.stats_enemy[4]} vous a mis \033[1;31m{enemy_attack(player)}\033[0m de dégats.\n")
            audio_engine.sfx_play("ressources/sfx/damageToPlayer.ogg", 1)
            time.sleep(2.5)

        if misc.is_dead(player) == True:
            player_death(player)

    if player.stats_enemy[0] <= 0:
        fight_end(player, vieEnnemiTempo)
        return True

def low_hp_detect(player):
    if 2 < player.stats[0] <= 7:
        audio_engine.sfx_play_loop("ressources/sfx/lowHP.ogg", 3)
    elif player.stats[0] <= 2:
        audio_engine.sfx_play_loop("ressources/sfx/veryLowHP.ogg", 3)
    else:
        audio_engine.sfx_stop(3)

# Action Player

def player_attaque(player):
    time.sleep(0.5)
    attaqueCharge = prepare_attaque()

    if attaqueCharge:
        attaqueRandom = int((player.stats[1] - player.stats_enemy[2]) * random.uniform(1.45, 1.75))
        if attaqueRandom <= 0:
            attaqueRandom = random.randint(2, player.stats[1] - 1)

    elif attaqueCharge == False:
        attaqueRandom = int((player.stats[1] - player.stats_enemy[2]) * random.uniform(1.1, 1.3))
        if attaqueRandom <= 0:
            attaqueRandom = random.randint(2, player.stats[1] - 1)

    elif attaqueCharge == None:
        attaqueRandom = int((player.stats[1] * 0.15 * random.uniform(1.05, 1.1)))
        print("\033[3m\nraté...\033[0m")

    player.stats_enemy[0] -= attaqueRandom
    return attaqueRandom

def prepare_attaque():
    print()

    for i in reversed(range(3)):
        timer = time.time()
        audio_engine.sfx_play("ressources/sfx/prepareAttack.ogg", 4)
        print(i + 1)
        while time.time() - timer < 0.5:
            if keyboard.is_pressed("space"):
                return None

    timer = time.time()
    audio_engine.sfx_play("ressources/sfx/attaqueGo.ogg", 4)
    print("\n\033[1;32m\033[1;1mGO !\033[0m")

    while True:
        if keyboard.is_pressed("space"):
            audio_engine.sfx_play("ressources/sfx/attaqueBien.ogg", 2)
            print("\033[1;1m\033[1;33m\nBien !")
            time.sleep(0.5)
            audio_engine.sfx_play("ressources/sfx/attaqueGo.ogg", 4)
            print("\n\033[1;32m\033[1;1mGO !\033[0m")
            timer = time.time()

            while True:
                if keyboard.is_pressed("space"):
                    audio_engine.sfx_play("ressources/sfx/attaqueSuccess.ogg", 1)
                    print(f"\033[1;1m\n{misc.rainbow_text('Excellent !')}")
                    return True

                if time.time() - timer > 0.65:
                    return False

        if time.time() - timer > 1.10:
            return None

def special_attack(player):
    print("wip (pour combien de temps, ca jsp du tout jpp)")
    time.sleep(4)

def flee():
    if random.random() > 0.25:
        audio_engine.sfx_play("ressources/sfx/leaveBattle.ogg", 2)
        print("\n\033[3mVous avez fuis...\033[0m")
        audio_engine.sfx_stop(3)
        misc.menu_transition(3)
        return True
    else:
        audio_engine.sfx_play("ressources/sfx/trebucher.ogg", 2)
        print("\nVous avez trébucher, vous êtes toujours dans le combat.\n")
        time.sleep(2)
        return False

def nothing():
    print()
    for point in range(0, 4):
        print("\033[3mVous attendez patiement" + ("." * point) + "\033[0m", end="")
        time.sleep(0.6)
        if point != 3:
            sys.stdout.write("\r")

    print("\n")

# Ennemi action(s ?)
def enemy_attack(player):
    attaqueEnnemi = int(player.stats_enemy[1] * random.uniform(1.1, 1.2) - player.stats[2] / 2)

    if attaqueEnnemi <= 0:
        attaqueEnnemi = random.randint(4, player.stats_enemy[1] - 1)

    player.stats[0] -= attaqueEnnemi
    misc.check_stats(player)
    return attaqueEnnemi

# Combat fin GG...ou pas ?
def fight_end(player, vieEnnemiTempo):
    audio_engine.sfx_stop(3)
    audio_engine.music_stop()

    audio_engine.sfx_play("ressources/victoryBattle.mp3", 1)

    expGagner = level_xp.exp(player, vieEnnemiTempo)
    print(f"{player.stats_enemy[4]} vaincu! Vous avez gagné \033[1;32m{expGagner} points d'expérience.\033[0m\n")

    time.sleep(1.5)
    audio_engine.sfx_play("ressources/sfx/battleWinClap.ogg", 2)
    time.sleep(2)
    level_xp.check_level(player)
    states_effects.reset_state(player)


def player_death(player):
    checkMort = objects.totem_regen(player)
    if checkMort != False:
        audio_engine.sfx_stop(3)
        audio_engine.music_stop()
        audio_engine.sfx_play("ressources/sfx/death.ogg", 2)

        print("...")
        time.sleep(1.45)

        audio_engine.sfx_play("ressources/sfx/fullRegen.ogg", 2)
        print(f"Le \033[1;32m{checkMort}\033[0m vous a sauvé !\n")
        time.sleep(2)
        return False
    else:
        audio_engine.sfx_stop(3)
        audio_engine.music_stop()
        audio_engine.sfx_play("ressources/sfx/death.ogg", 2)

        print("...")
        time.sleep(1.5)

        print("💀💀💀")
        time.sleep(1.5)

        audio_engine.sfx_play("ressources/gameOver.mp3", 2)
        print("\n\033[1;31mGAME OVER !\033[0m")
        time.sleep(6)
        menus.game_over_menu(player)