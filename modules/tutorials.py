import random
import time
import keyboard

from engines import audio_engine

from modules import map
from modules import misc

def map_tutorial(player):
    if player.tutorial_triggers["mapFirstTime"] == True:
        audio_engine.music_play("ressources/tutorial.mp3")
        print("\n\033[1;1mEspace pour passer les dialogues. ⭐\033[0m", end = "")
        misc.dialogue()
        time.sleep(0.25)
        map.legend()
        misc.menu_transition(2)
        player.tutorial_triggers["mapFirstTime"] = False

def fight_tutorial(player):
    if player.tutorial_triggers["fightFirstTime"] == True:
        time.sleep(0.5)
        audio_engine.sfx_play("ressources/sfx/tutoStopLong.ogg", 2)
        print("\n\033[1;1mSTOOOOP !!!! ATTENDEZ !!!\033[0m ⭐")
        time.sleep(0.5)
        misc.dialogue()

        tutoFightDemande = input("Sire ! Cela fait quand même bien longtemps que vous ne vous êtes pas battu...vous voulez que je vous réexplique ? (O/N) ").upper()

        while tutoFightDemande != "O" and tutoFightDemande != "N":
            audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
            tutoFightDemande = input("Je n'ai pas bien compris si vous vouliez de l'aide. (O/N) ").upper()

        if tutoFightDemande == "O":
            audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
            misc.menu_transition(0.5)
            print("\nD'accord, c'est un honneur de pouvoir vous aidez Sire ! Alors, c'est très simple...continuez. ⭐")
            audio_engine.music_play("ressources/tutorial.mp3")
            misc.dialogue()
            time.sleep(0.5)
            print()

            for i in reversed(range(3)):
                audio_engine.sfx_play("ressources/sfx/prepareAttack.ogg", 4)
                print(i + 1)
                time.sleep(0.5)
            audio_engine.sfx_play("ressources/sfx/tutoStop.ogg", 2)
            print("\n\033[1;31mSTOP\033[0m ⭐")
            time.sleep(0.5)
            misc.dialogue()

            print("Un compte à rebourd va commencer à partir de 3, et lorsque vous voyez \033[1;32mGO !\033[0m, c'est là où vous devez attaquer... ⭐")
            misc.dialogue()

            audio_engine.sfx_play("ressources/sfx/attaqueGo.ogg", 4)
            print("\n\033[1;32m\033[1mGO !\033[0m")
            keyboard.wait('space', suppress=True)

            audio_engine.sfx_play("ressources/sfx/attaqueBien.ogg", 2)
            print("\033[1m\033[1;33m\nBien !\033[0m")
            time.sleep(0.5)

            print(f"...et vous pouvez enchainé juste après pour faire un combo {misc.rainbow_text('Excellent')} et faire plus de dégat ! ⭐")
            misc.dialogue()

            audio_engine.sfx_play("ressources/sfx/attaqueGo.ogg", 4)
            print("\n\033[1;32m\033[1mGO !\033[0m")
            keyboard.wait('space', suppress=True)

            audio_engine.sfx_play("ressources/sfx/attaqueSuccess.ogg", 1)
            print(f"\033[1m\n{misc.rainbow_text('Excellent !')}")
            time.sleep(2)

            print("\nBravo Sire ! Vous vous débrouiller comme un AS. Bon, j'y retourne, je dois aller surveiller les poules du château. Bon courage ! ⭐")
            misc.dialogue()

            misc.menu_transition(1)
            player.tutorial_triggers["fightFirstTime"] = False
            return True

        elif tutoFightDemande == "N":
            audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
            print("Pas de soucis ! C'est vous le Roi après tout ! ⭐")
            misc.dialogue()
            player.tutorial_triggers["fightFirstTime"] = False
            return False

    else:
        return False