import random
import time
import keyboard

import audioEngine
import map
import misc

def mapTuto(player):
    if player.tutorielDone["mapFirstTime"] == True:
        audioEngine.musicPlay("ressources/tutorial.mp3")
        print("\n\033[1;1mEspace pour passer les dialogues. ⭐\033[0m", end = "")
        misc.dialogue()
        time.sleep(0.25)
        map.legende()
        misc.transitionMenu(2)
        player.tutorielDone["mapFirstTime"] = False

def fightTuto(player):
    if player.tutorielDone["fightFirstTime"] == True:
        time.sleep(0.5)
        audioEngine.sfxPlay("ressources/sfx/tutoStopLong.ogg", 2)
        print("\n\033[1;1mSTOOOOP !!!!\033[0m ⭐")
        time.sleep(0.5)
        misc.dialogue()

        tutoFightDemande = input("Sire ! Cela fait quand même bien longtemps que vous ne vous êtes pas battu...vous voulez que je vous réexplique ? (O/N) ").upper()

        while tutoFightDemande != "O" and tutoFightDemande != "N":
            audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
            tutoFightDemande = input("Je n'ai pas bien compris si vous vouliez de l'aide. (O/N) ").upper()

        if tutoFightDemande == "O":
            audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)
            misc.transitionMenu(0.5)
            print("\nD'accord, c'est un honneur de pouvoir vous aidez Sire ! Alors, c'est très simple...continuez. ⭐")
            audioEngine.musicPlay("ressources/tutorial.mp3")
            misc.dialogue()
            time.sleep(0.5)
            print()

            for i in reversed(range(3)):
                audioEngine.sfxPlay("ressources/sfx/prepareAttack.ogg", 4)
                print(i + 1)
                time.sleep(0.5)
            audioEngine.sfxPlay("ressources/sfx/tutoStop.ogg", 2)
            print("\n\033[1;31mSTOP\033[0m ⭐")
            time.sleep(0.5)
            misc.dialogue()

            print("Un compte à rebourd va commencer à partir de 3, et lorsque vous voyez \033[1;32mGO !\033[0m, c'est là où vous devez attaquer... ⭐")
            misc.dialogue()

            audioEngine.sfxPlay("ressources/sfx/attaqueGo.ogg", 4)
            print("\n\033[1;32m\033[1mGO !\033[0m")
            keyboard.wait('space', suppress=True)

            audioEngine.sfxPlay("ressources/sfx/attaqueBien.ogg", 2)
            print("\033[1m\033[1;33m\nBien !\033[0m")
            time.sleep(0.5)

            print(f"...et vous pouvez enchainé juste après pour faire un combo {misc.rainbowText('Excellent')} et faire plus de dégat ! ⭐")
            misc.dialogue()

            audioEngine.sfxPlay("ressources/sfx/attaqueGo.ogg", 4)
            print("\n\033[1;32m\033[1mGO !\033[0m")
            keyboard.wait('space', suppress=True)

            audioEngine.sfxPlay("ressources/sfx/attaqueSuccess.ogg", 1)
            print(f"\033[1m\n{misc.rainbowText('Excellent !')}")
            time.sleep(2)

            print("\nBravo Sire ! Vous vous débrouiller comme un AS. Bon, j'y retourne, je dois aller surveiller les poules du château. Bon courage ! ⭐")
            misc.dialogue()

            misc.transitionMenu(1)
            player.tutorielDone["fightFirstTime"] = False
            return True

        elif tutoFightDemande == "N":
            audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)
            print("Pas de soucis ! C'est vous le Roi après tout ! ⭐")
            misc.dialogue()
            player.tutorielDone["fightFirstTime"] = False
            return False

    else:
        return False