import time
import keyboard

from engines import audio_engine

from modules import menus
from modules import settings
from modules import save_system
from modules import tutorials
from modules import battle
from modules import tower
from modules import misc

def display_map(map):
    mapAffichage = []

    for element in map:

        if element == "[J]":
            mapAffichage.append("\033[1;32m[J]\033[0m")
        elif element == "[E]":
            mapAffichage.append("\033[1;31m[E]\033[0m")
        elif element == "[T]":
            mapAffichage.append("\033[1;34m[T]\033[0m")
        elif element == "[M]":
            mapAffichage.append("\033[1;1m[M]\033[0m")
        elif element == "[R]":
            mapAffichage.append("\033[1;35m[R]\033[0m")
        elif element == "[S]":
            mapAffichage.append("\033[1;95m[S]\033[0m")
        elif element == "[?]":
            mapAffichage.append("\033[37m[?]\033[0m")
        else:
            mapAffichage.append(element)

    print(*mapAffichage)
    print()

def game_start(player):
    tutorials.map_tutorial(player)

    audio_engine.music_play("ressources/map.mp3")

    display_map(player.map)

    positionPlayer = player.map.index('[J]')

    action = str(input("Gauche (G) / Droite (D) / Haut (H) / Bas (B)\nProfile (P) / Légende (L) / Menu Principal (M) / Fermer Le Jeu (F) ")).upper()
    while action != "G" and action != "D" and action != "H" and action != "B" and action != "P" and action != "L" and action != "M" and action != "F":
        action = str(input("\nGauche (G) / Droite (D) / Haut (H) / Bas (B)\nProfile (P) / Légende (L) / Menu Principal (M) / Fermer Le Jeu (F) ")).upper()

    if action == "G":
        caseDetecteur = positionPlayer - 1
        if collision(player, caseDetecteur) == True:
            move(player, positionPlayer, - 1)

    elif action == "D":
        caseDetecteur = positionPlayer + 1
        if collision(player, caseDetecteur) == True:
            move(player, positionPlayer, 1)

    elif action == "H":
        caseDetecteur = positionPlayer - player.y_movement
        if caseDetecteur > 0:
            if collision(player, caseDetecteur) == True:
                move(player, positionPlayer, - player.y_movement)

    elif action == "B":
        caseDetecteur = positionPlayer + player.y_movement
        if caseDetecteur < len(player.map):
            if collision(player, caseDetecteur) == True:
                move(player, positionPlayer, player.y_movement)

    elif action == "L":
        audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
        legend()

    elif action == "P":
        audio_engine.sfx_play("ressources/sfx/openProfile.ogg", 1)
        menus.profile(player)

    elif action == "M":
        audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
        menuTrigger = input("\nVoulez vous vraiment aller sur le menu principal ? (O/N) ").upper()
        while menuTrigger != "O" and menuTrigger != "N":
            audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
            menuTrigger = input("Incorrect. Voulez vous vraiment aller sur le menu principal ? (O/N) ").upper()

        if menuTrigger == "O":
            audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
            print()
            autoSaveDetect = settings.auto_save(player)
            if autoSaveDetect == False:
                saveToMenu = input("Voulez vous sauvegarder ? Vous allez perdre votre sauvegarde si vous n'avez pas sauvegarder. (O/N) ").upper()
                while saveToMenu != "O" and saveToMenu != "N":
                    audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
                    saveToMenu = input("Incorrect. Voulez vous sauvegarder ? (O/N) ").upper()

                if saveToMenu == "O":
                    if save_system.save(player) == True:
                        print("Partie sauvegardé.")
                    else:
                        print("La sauvegarde a échoué.")

            elif autoSaveDetect == None:
                print("La sauvegarde automatique a échoué.")

            misc.menu_transition(2)
            menus.main_menu(player)
        else:
            audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)

    elif action == "F":
        audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
        fermerTrigger = input("Voulez vous vraiment quitter ? (O/N) ").upper()
        while fermerTrigger != "O" and fermerTrigger != "N":
            audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
            fermerTrigger = input("Incorrect. Voulez vous vraiment quitter ? (O/N) ").upper()

        if fermerTrigger == "O":
            print()
            autoSaveDetect = settings.auto_save(player)
            if autoSaveDetect == False:
                saveQuit = input("Voulez vous sauvegarder avant de quitter ? (O/N) ").upper()
                while saveQuit != "O" and saveQuit != "N":
                    audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
                    saveQuit = input("Incorrect. Voulez vous sauvegarder ? (O/N) ").upper()

                if saveQuit == "O":
                    if save_system.save(player) == True:
                        audio_engine.sfx_play("ressources/sfx/saveQuitSuccess.ogg", 2)
                        print("Partie sauvegardé.")
                    else:
                        print("La sauvegarde a échoué.")

            elif autoSaveDetect == None:
                print("La sauvegarde automatique a échoué.")

            misc.close_game()
        else:
            audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)

    if player.settings["Auto-save"] == "Activé":
        save_system.save(player)

def collision(player, obj):
    if player.map[obj] == '[E]':
        audio_engine.music_stop()
        audio_engine.sfx_play("ressources/sfx/battleStart.ogg", 1)

        time.sleep(0.85)

        player.stats_enemy = [16, 8, 7, False, "Goomba"]

        if battle.fight(player, "ressources/mFight.mp3") == True:
            settings.auto_save(player)
            time.sleep(2)
            return True
        else:
            return False

    elif player.map[obj] == '[T]':
        if tower.tower(player) == True:
            player.map[obj] = '[R]'

    elif player.map[obj] == '[S]':
        print("SHOP (wip)")
        time.sleep(2)

    elif player.map[obj] == '[?]':
        print("mystère  .. ..  (wip aussi)")
        time.sleep(2)

    elif player.map[obj] == '[.]':
        return True

    else:
        return False

def move(player, positionPlayer, speed):
    player.map[positionPlayer + speed] = '[J]'
    player.map[positionPlayer] = '[.]'

def legend():
    print("\n\nLégende:\n"
          "\033[1;32mJ = joueur\n"
          "\033[1;31mE = ennemi\n"
          "\033[1;34mT = tour\n"
          "\033[1;35mR = ruine (tour complétée)\n"
          "\033[1;95mS = magasin\033[0m\n"
          "\033[37m? = mystère...\033[0m\n"
          "\033[1;1mM = mur\n\nContinuer ⭐\033[0m", end="")
    misc.dialogue()
    print()