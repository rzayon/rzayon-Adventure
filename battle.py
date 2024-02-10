import random
import time
import keyboard

import audioEngine
import parametres
import menus
import tutoriel
import levelXP
import etatsEffets
import misc

def fight(player, musicBattle):

    audioEngine.musicPlay(musicBattle)

    vieEnnemiTempo = player.statsEnnemi[0]

    print()

    while player.stats[0] > 0 and player.statsEnnemi[0] > 0:
        print(f"{parametres.affichePseudoCouleur(player)}\n{misc.checkLifeWarning(player)} \033[1;95mPV\033[0m | {player.stats[3]} \033[1;33mPS\033[0m\n" +
              (etatsEffets.afficheEffets(player.etats) if etatsEffets.afficheEffets(player.etats) != False else ""))
        print("\033[1;1mVS\033[0m\n")
        print(f"\033[37m{player.statsEnnemi[4]}\033[0m" + (etatsEffets.afficheEffets(player.etatsEnnemi) if etatsEffets.afficheEffets(player.etatsEnnemi) != False else " ") + f"\n\033[1;95mPV:\033[0m {player.statsEnnemi[0]}\n\033[1;31mAtt:\033[0m {player.statsEnnemi[1]}\n")

        fightActionDone = False

        while fightActionDone == False:
            lowHpDetect(player)
            attaqueTrigger = input("\033[1;31mAttaquer (Att)\033[0m / \033[1;32mObjets (Obj)\033[0m / \033[1;33mSpécial (Spé) [WIP]\033[0m / \033[1;36mFuir \033[0m").capitalize()

            while attaqueTrigger != "Att" and attaqueTrigger != "Obj" and attaqueTrigger != "Spé" and attaqueTrigger != "Fuir":
                audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
                attaqueTrigger = input("\033[1;31m\033[1;1mAttaquer (Att)\033[0m / \033[1;32mObjets (Obj)\033[0m / \033[1;33mSpécial (Spé) [WIP]\033[0m / \033[1;36mFuir \033[0m").capitalize()

            if attaqueTrigger == "Att":
                audioEngine.sfxStop(3)
                audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)

                if tutoriel.fightTuto(player) == True:
                    tutoriel.fightTuto(player)

                    audioEngine.musicPlay(musicBattle)
                    attaqueRandom = int((player.stats[1] - player.statsEnnemi[2]) * random.uniform(1.5, 1.9))
                    player.statsEnnemi[0] -= attaqueRandom
                    print(f"\nVous avez mis \033[1;31m{attaqueRandom}\033[0m de dégats à l'ennemi.")

                else:
                    print(f"\nVous avez mis \033[1;31m{playerAttaque(player)}\033[0m de dégats à l'ennemi.")

                time.sleep(2)
                fightActionDone = True

            elif attaqueTrigger == "Obj":
                audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)
                player.stats[0] += 10
                if objets(player) == True:
                    fightActionDone = True

            elif attaqueTrigger == "Spé":
                audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)
                if attaqueSpe(player) == True:
                    fightActionDone = True

            elif attaqueTrigger == "Fuir":
                fightActionDone = True
                if fuir() == True:
                    return False

        etatsEffets.detectEtat(player)

        if player.statsEnnemi[0] > 0:
            print(f"{player.statsEnnemi[4]} vous a mis \033[1;31m{ennemiAttaque(player)}\033[0m de dégats.\n")
            audioEngine.sfxPlay("ressources/sfx/damageToPlayer.ogg", 1)
            time.sleep(2.5)

        if misc.estMort(player) == True:
            audioEngine.musicStop()
            audioEngine.sfxStop(3)
            audioEngine.sfxPlay("ressources/sfx/death.ogg", 2)

            print("...")
            time.sleep(1.5)

            print("💀💀💀")
            time.sleep(1.5)

            audioEngine.sfxPlay("ressources/gameOver.mp3", 2)
            print("\n\033[1;31mGAME OVER !\033[0m")
            time.sleep(6)
            menus.gameOverChoice(player)

    if player.statsEnnemi[0] <= 0:
        finCombat(player, vieEnnemiTempo)
        return True

def lowHpDetect(player):
    if 2 < player.stats[0] <= 7:
        audioEngine.sfxPlayLoop("ressources/sfx/lowHP.ogg", 3)
    elif player.stats[0] <= 2:
        audioEngine.sfxPlayLoop("ressources/sfx/veryLowHP.ogg", 3)
    else:
        audioEngine.sfxStop(3)

# Action Player

def playerAttaque(player):
    time.sleep(0.5)
    attaqueCharge = prepareAttaque()

    if attaqueCharge:
        attaqueRandom = int((player.stats[1] - player.statsEnnemi[2]) * random.uniform(1.45, 1.75))
        if attaqueRandom <= 0:
            attaqueRandom = random.randint(2, player.stats[1] - 1)

    elif attaqueCharge == False:
        attaqueRandom = int((player.stats[1] - player.statsEnnemi[2]) * random.uniform(1.1, 1.3))
        if attaqueRandom <= 0:
            attaqueRandom = random.randint(2, player.stats[1] - 1)

    elif attaqueCharge == None:
        attaqueRandom = int((player.stats[1] * 0.15 * random.uniform(1.05, 1.1)))
        print("\033[3m\nraté...\033[0m")

    player.statsEnnemi[0] -= attaqueRandom
    return attaqueRandom

def prepareAttaque():
    print()

    for i in reversed(range(3)):
        timer = time.time()
        audioEngine.sfxPlay("ressources/sfx/prepareAttack.ogg", 4)
        print(i + 1)
        while time.time() - timer < 0.5:
            if keyboard.is_pressed("space"):
                return None

    timer = time.time()
    audioEngine.sfxPlay("ressources/sfx/attaqueGo.ogg", 4)
    print("\n\033[1;32m\033[1;1mGO !\033[0m")

    while True:
        if keyboard.is_pressed("space"):
            audioEngine.sfxPlay("ressources/sfx/attaqueBien.ogg", 2)
            print("\033[1;1m\033[1;33m\nBien !")
            time.sleep(0.5)
            audioEngine.sfxPlay("ressources/sfx/attaqueGo.ogg", 4)
            print("\n\033[1;32m\033[1;1mGO !\033[0m")
            timer = time.time()

            while True:
                if keyboard.is_pressed("space"):
                    audioEngine.sfxPlay("ressources/sfx/attaqueSuccess.ogg", 1)
                    print(f"\033[1;1m\n{misc.rainbowText('Excellent !')}")
                    return True

                if time.time() - timer > 0.65:
                    return False

        if time.time() - timer > 1.10:
            return None

def objets(player):
    '''print("Voici vos objets:")
    if player.objets == []:
        print("\033[3mVide.\033[0m\n")
    else:
        print(*player.objets, sep=", ")
        objetUtiliser = int(input("Quel objet voulez vous utiliser ? "))
        while objetUtiliser > len(player.objets) or objetUtiliser <= 0:
            objetUtiliser = int(input("Le choix est invalide. Quel objet voulez vous utiliser ? "))
        objetChoix = objetUtiliser
        objetUtiliser = player.objets[objetUtiliser - 1]
        player.objet(objetUtiliser, player.statsEnnemi)
        player.objets.pop(objetChoix - 1)'''
    print("disable """"""""temporairement""""""""")
    time.sleep(3)

def attaqueSpe(player):
    print("wip (pour combien de temps, ca jsp du tout jpp)")
    time.sleep(4)

def fuir():
    if random.random() > 0.25:
        audioEngine.sfxPlay("ressources/sfx/leaveBattle.ogg", 2)
        print("\n\033[3mVous avez fuis...\033[0m")
        audioEngine.sfxStop(3)
        misc.transitionMenu(3)
        return True
    else:
        audioEngine.sfxPlay("ressources/sfx/trebucher.ogg", 2)
        print("\nVous avez trébucher, vous êtes toujours dans le combat.\n")
        time.sleep(2)
        return False

# Ennemi action(s ?)
def ennemiAttaque(player):
    attaqueEnnemi = int(player.statsEnnemi[1] * random.uniform(1.1, 1.2) - player.stats[2] / 2)

    if attaqueEnnemi <= 0:
        attaqueEnnemi = random.randint(4, player.statsEnnemi[1] - 1)

    player.stats[0] -= attaqueEnnemi
    misc.verifStats(player)
    return attaqueEnnemi

# Combat fin GG
def finCombat(player, vieEnnemiTempo):
    audioEngine.sfxStop(3)
    audioEngine.musicStop()

    audioEngine.sfxPlay("ressources/victoryBattle.mp3", 1)

    expGagner = levelXP.exp(player, vieEnnemiTempo)
    print(f"{player.statsEnnemi[4]} vaincu! Vous avez gagné \033[1;32m{expGagner} points d'expérience.\033[0m\n")

    time.sleep(1.5)
    audioEngine.sfxPlay("ressources/sfx/battleWinClap.ogg", 2)
    time.sleep(2)
    levelXP.levelCheck(player)
    etatsEffets.resetEtats(player)