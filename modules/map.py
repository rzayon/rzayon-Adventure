import time
import keyboard

import audioEngine

import menus
import parametres
import saveSystem
import tutoriel
import battle
import tower
import misc

def afficheMap(map):
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
        else:
            mapAffichage.append(element)

    print(*mapAffichage)
    print()

def partie(player):
    tutoriel.mapTuto(player)

    audioEngine.musicPlay("ressources/map.mp3")

    afficheMap(player.map)

    positionPlayer = player.map.index('[J]')

    action = str(input("Gauche (G) / Droite (D) / Haut (H) / Bas (B)\nProfile (P) / Légende (L) / Menu Principal (M) / Fermer Le Jeu (F) ")).upper()
    while action != "G" and action != "D" and action != "H" and action != "B" and action != "P" and action != "L" and action != "M" and action != "F":
        action = str(input("\nGauche (G) / Droite (D) / Haut (H) / Bas (B)\nProfile (P) / Légende (L) / Menu Principal (M) / Fermer Le Jeu (F) ")).upper()

    if action == "G":
        caseDetecteur = positionPlayer - 1
        if collision(player, caseDetecteur) == True:
            deplacer(player, positionPlayer, - 1)

    elif action == "D":
        caseDetecteur = positionPlayer + 1
        if collision(player, caseDetecteur) == True:
            deplacer(player, positionPlayer, 1)

    elif action == "H":
        caseDetecteur = positionPlayer - player.deplacementHauteur
        if caseDetecteur > 0:
            if collision(player, caseDetecteur) == True:
                deplacer(player, positionPlayer, - player.deplacementHauteur)

    elif action == "B":
        caseDetecteur = positionPlayer + player.deplacementHauteur
        if caseDetecteur < len(player.map):
            if collision(player, caseDetecteur) == True:
                deplacer(player, positionPlayer, player.deplacementHauteur)

    elif action == "L":
        audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)
        legende()

    elif action == "P":
        audioEngine.sfxPlay("ressources/sfx/openProfile.ogg", 1)
        menus.profile(player)

    elif action == "M":
        audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)
        menuTrigger = input("\nVoulez vous vraiment aller sur le menu principal ? (O/N) ").upper()
        while menuTrigger != "O" and menuTrigger != "N":
            audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
            menuTrigger = input("Incorrect. Voulez vous vraiment aller sur le menu principal ? (O/N) ").upper()

        if menuTrigger == "O":
            audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)
            print()
            autoSaveDetect = parametres.autoSave(player)
            if autoSaveDetect == False:
                saveToMenu = input("Voulez vous sauvegarder ? Vous allez perdre votre sauvegarde si vous n'avez pas sauvegarder. (O/N) ").upper()
                while saveToMenu != "O" and saveToMenu != "N":
                    audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
                    saveToMenu = input("Incorrect. Voulez vous sauvegarder ? (O/N) ").upper()

                if saveToMenu == "O":
                    if saveSystem.save(player) == True:
                        print("Partie sauvegardé.")
                    else:
                        print("La sauvegarde a échoué.")

            elif autoSaveDetect == None:
                print("La sauvegarde automatique a échoué.")

            misc.transitionMenu(2)
            menus.mainMenu(player)
        else:
            audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)

    elif action == "F":
        audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)
        fermerTrigger = input("Voulez vous vraiment quitter ? (O/N) ").upper()
        while fermerTrigger != "O" and fermerTrigger != "N":
            audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
            fermerTrigger = input("Incorrect. Voulez vous vraiment quitter ? (O/N) ").upper()

        if fermerTrigger == "O":
            print()
            autoSaveDetect = parametres.autoSave(player)
            if autoSaveDetect == False:
                saveQuit = input("Voulez vous sauvegarder avant de quitter ? (O/N) ").upper()
                while saveQuit != "O" and saveQuit != "N":
                    audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
                    saveQuit = input("Incorrect. Voulez vous sauvegarder ? (O/N) ").upper()

                if saveQuit == "O":
                    if saveSystem.save(player) == True:
                        audioEngine.sfxPlay("ressources/sfx/saveQuitSuccess.ogg", 2)
                        print("Partie sauvegardé.")
                    else:
                        print("La sauvegarde a échoué.")

            elif autoSaveDetect == None:
                print("La sauvegarde automatique a échoué.")

            misc.fermerJeu()
        else:
            audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)

    if player.parametres["Auto-save"] == "Activé":
        saveSystem.save(player)

def collision(player, obj):
    if player.map[obj] == '[E]':
        audioEngine.musicStop()
        audioEngine.sfxPlay("ressources/sfx/battleStart.ogg", 1)

        time.sleep(0.85)

        player.statsEnnemi = [16, 8, 7, False, "Goomba"]

        if battle.fight(player, "ressources/mFight.mp3") == True:
            parametres.autoSave(player)
            time.sleep(2)
            return True
        else:
            return False

    elif player.map[obj] == '[T]':
        if tower.tower(player) == True:
            player.map[obj] = '[R]'

    elif player.map[obj] == '[.]':
        return True

    else:
        return False

def deplacer(player, positionPlayer, speed):
    player.map[positionPlayer + speed] = '[J]'
    player.map[positionPlayer] = '[.]'

def legende():
    print("\n\nLégende:\n"
          "\033[1;32mJ = joueur\033[0m\n"
          "\033[1;31mE = ennemi\033[0m\n"
          "\033[1;34mT = tour\033[0m\n"
          "\033[1;35mR = ruine (tour complétée)\033[0m\n"
          "\033[1;1mM = mur\n\nContinuer...\033[0m", end="")
    misc.dialogue()
    print()