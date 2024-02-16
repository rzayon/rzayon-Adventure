""" Module contenant les différents menus du jeu ainsi que leurs options. """


import sys
import time
import random
import keyboard

from engines import audio_engine

from modules import save_system
from modules import settings
from modules import map
from modules import level_xp
from modules import objects
from modules import misc

#Title Screen

def title_screen(player, trigger):
    """Lance l'écran titre du jeu.

        Args:
            trigger (bool): définis si le joueur vient de lancer le jeu ou non
        """

    audio_engine.music_play("ressources/title.mp3")

    if trigger == False:
        time.sleep(1.2)
        print(f"\t  {player.game_name}")
        time.sleep(2)
        print("\n\t\033[4mAppuyez pour commencer\033[0m\n\t\t  "
              "\033[1;1mbeta", player.game_version + "\033[0m")
        keyboard.read_event(suppress=True)
        audio_engine.sfx_play("ressources/sfx/exitTitle.ogg", 1)
        misc.menu_transition(1)

    else:
        time.sleep(1.2)
        print(f"\n\t  {player.game_name}\n\n"
              "\t\033[4mAppuyez pour commencer\033[0m"
              "\n\t\t  \033[1;1mbeta", player.game_version + "\033[0m")
        keyboard.read_event(suppress = True)
        audio_engine.sfx_play("ressources/sfx/exitTitle.ogg", 1)
        misc.menu_transition(0.5)

    main_menu(player)

#Main Menu

def main_menu(player):

    audio_engine.music_play("ressources/mainMenu.mp3")

    print(f"\n\t  {player.game_name}\n\n"
          "\t  \033[4mNouvelle Partie (N)\033[0m\n" +

         ("\t     \033[4m\033[37mContinuer (C)\033[0m\n"
           if save_system.load(player) != True else
          "\t     \033[4mContinuer (C)\033[0m\n") +

          "\t     \033[4mParamètre (P)\033[0m\n"
          "\t    \033[4mÉcran Titre (T)\033[0m\n"
          "\t      \033[4mQuitter (Q)\033[0m")

    mainMenuChoix = input("\t\t\t   ").upper()
    while mainMenuChoix != "N" and mainMenuChoix != "C" and mainMenuChoix != "P" and mainMenuChoix != "T" and mainMenuChoix != "Q":
        mainMenuChoix = input("\t\t\t   ").upper()

    if mainMenuChoix == "N":
        new_game(player)
        audio_engine.sfx_play("ressources/sfx/gameStart.ogg", 1)
        print("\n\033[1;32m\033[1;1mNouvelle partie commencer !\033[0m")
        misc.menu_transition(3)
        while player.stats[0] > 0:
            map.game_start(player)

    elif mainMenuChoix == "C":

        continuer = save_system.load(player)

        if continuer == True:
            print("\n\033[1;32mVotre partie s'est chargée.\033[0m")
            audio_engine.sfx_play("ressources/sfx/autoSave.ogg", 2)
            misc.menu_transition(3)
            while player.stats[0] > 0:
                map.game_start(player)
        elif continuer == None:
            audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
            print("\n\033[1;1mAucune partie existante.\033[0m")
            time.sleep(2.5)
            main_menu(player)
        else:
            audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
            print("\n\033[1;31mLa partie n'a pas pu se charger.\033[0m")
            time.sleep(2.5)
            main_menu(player)

    elif mainMenuChoix == "P":
        audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
        settings_menu(player)
        main_menu(player)

    elif mainMenuChoix == "T":
        audio_engine.sfx_play("ressources/sfx/close.ogg", 1)
        misc.menu_transition(0.2)
        title_screen(player, True)

    elif mainMenuChoix == "Q":
        audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
        quitter = input("\nVoulez vous vraiment quitter ? (O/N) ").upper()
        while quitter != "O" and quitter != "N":
            quitter = input("\033[1;33mIncorrect. Voulez vous vraiment quitter ? (O/N)\033[0m ").upper()

        if quitter == "O":
            misc.close_game()
        else:
            audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
            main_menu(player)

def new_game(player):
    player.player_name = "Player"
    player.stats = [25, 12, 10, 10, 0, 1, 0]
    player.stats_max = [25, 10]
    player.objects = {"Champignon": [4, True, 10],
          "Champi Doré": [4, True, 25],
          "Champi Ultime": [4, True, 50],
          "Champi Max": [4, True, player.stats_max[0]],

          "Totem": [2, None],
          "Totem Gardien": [2, None],

          "Fleur Carnovore": [3, False, 20],
          "Gross pierre": [2, False, 3],

          "Potion du Dragon": [3, False, 15],
          "Potion de Toute Puissance": [3, False, 30],

          "Bouclier naturel": [2, False, 10],
          "Bouclier Max": [2, False, 25]}
    #player.objects = {}
    player.map = []

    player.tutorial_triggers = {"fightFirstTime": True, "mapFirstTime": True, "shopFirstTime": True}

    new_map(player, random.randint(7, 9), random.randint(12, 15))

def new_map(player, nbLigne, nbElement):

    mapLigne = []
    nbEnnemi = 0

    while nbEnnemi <= 15 and "[J]" not in player.map:
        player.map = []
        nbEnnemi = 0

        for ligne in range(nbLigne):
            mapLigne = []
            mapLigne.append("[M]")

            for element in range(nbElement):
                elementRandom = random.random()

                if int(nbLigne / 2) == ligne and int(nbElement / 2) == element:
                    mapLigne.append("[J]")
                    continue

                if 0.025 < elementRandom <= 0.095:
                    mapLigne.append("[E]")
                    nbEnnemi += 1
                elif elementRandom <= 0.025:
                    mapLigne.append("[?]")
                else:
                    mapLigne.append("[.]")

            mapLigne.append("[M]")
            player.map += ["\n"] + mapLigne

    tower = random.randint(0, len(player.map) - 1)
    shop = random.randint(0, len(player.map) - 1)

    while player.map[tower] != "[.]":
        tower = random.randint(0, len(player.map) - 1)
    player.map[tower] = "[T]"

    while player.map[shop] != "[.]" != "[T]":
        shop = random.randint(0, len(player.map) - 1)
    player.map[shop] = "[S]"

    player.y_movement = len(mapLigne) + 1

def settings_menu(player):

    audio_engine.music_volume_lower()

    settings.display_settings(player)

    actionParametre = input("\nChanger un paramètre (C) / Quitter (Q) ").upper()
    while actionParametre != "C" and actionParametre != "Q":
        audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
        actionParametre = input("Changer un paramètre (C) / Quitter (Q) ").upper()

    if actionParametre == "C":
        audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
        choixTrigger = False
        choixChangement = input("Quel paramètre voulez-vous changer ? ").lower()

        while choixTrigger == False:
            for parametre in player.settings.keys():
                if parametre.lower().startswith(choixChangement):
                    choixChangement = parametre
                    choixTrigger = True
                    audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
            if choixTrigger == False:
                audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
                choixChangement = input("Parametre incorrect. Quel paramètre voulez-vous changer ? ").lower()

        player.settings[choixChangement] = settings.switch_setting_classic(player, player.settings[choixChangement])

        audio_engine.sfx_play("ressources/sfx/changeApplied.ogg", 1)
        print("\n\033[1;32mParamètre changé.\033[0m")
        time.sleep(2)

        settings_menu(player)

    elif actionParametre == "Q":
        audio_engine.music_volume_reset()
        audio_engine.sfx_play("ressources/sfx/close.ogg", 1)
        return False

#Profile Menu

def profile(player):

    audio_engine.music_play("ressources/profile.mp3")

    quitTrigger = False
    while quitTrigger == False:

        print(f"\n{settings.display_name_color(player)}\n\n"
              f"Niveau {player.stats[5]} | EXP: {player.stats[4]}\n"
              f"\033[1;1mProchain niveau dans: \033[1;33m{level_xp.levels[player.stats[5] + 1] - player.stats[4]}\033[0m \033[1;1mEXP\033[0m\n\n"
              f"Vie: {player.stats[0]}/{str(player.stats_max[0])}\n"
              f"Attaque: {player.stats[1]}\n"
              f"Défense: {player.stats[2]}\n"
              f"PS: {player.stats[3]}/{player.stats_max[1]}\n\n"
              f"\033[1;33mArgent:\033[0m {player.stats[6]}$\n")

        profileAction = input("Objet (O) / Changer de nom (C) / Sauvegarder (S) / Load (L) / Paramètres (P) / Quitter (Q) ").upper()
        while profileAction != "O" and profileAction != "C" and profileAction != "S" and profileAction != "L" and profileAction != "P" and profileAction != "Q" and profileAction != "DB":
            profileAction = input("Objet (O) / Changer de nom (C) / Sauvegarder (S) / Load (L) / Paramètres (P) / Quitter (Q) ").upper()

        if profileAction == "O":
            audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
            objects_menu(player, False)

        elif profileAction == "C":
            audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
            changeNom = input("Voulez vous changer de nom ? (O/N) ").upper()
            while changeNom != "O" and changeNom != "N":
                audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
                changeNom = input("Reponse incorrecte. Voulez vous changer de nom ? (O/N) ").upper()
            if changeNom == "O":
                change_name(player)
            else:
                audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)

        elif profileAction == "S":

            audio_engine.sfx_play("ressources/sfx/saveAsk.ogg", 1)
            demandeSave = input("Voulez vous vraiment sauvegarder ? Cela écrasera votre ancienne sauvegarde. (O/N) ").upper()
            while demandeSave != "O" and demandeSave != "N":
                audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
                demandeSave = input("Reponse incorrecte. Voulez vous vraiment sauvegarder ? (O/N) ").upper()

            if demandeSave == "O":
                saveSauvegarde = save_system.save(player)

                if saveSauvegarde == True:
                    audio_engine.sfx_play("ressources/sfx/saveSuccess.ogg", 2)
                    print("\n\033[1;32mLa partie a été sauvegardée.\033[0m")
                    time.sleep(1.5)
                else:
                    audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
                    print("\n\033[1;31mErreur. La partie n'a pas pu être sauvegardé.\033[0m")
                    time.sleep(0.5)
            else:
                audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)

        elif profileAction == "L":

            audio_engine.sfx_play("ressources/sfx/saveAsk.ogg", 1)
            demandeLoad = input("Voulez vous vraiment charger la sauvegarde ? Cela écrasera votre progression actuelle. (O/N) ").upper()
            while demandeLoad != "O" and demandeLoad != "N":
                audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
                demandeLoad = input("Reponse incorrecte. Voulez vous vraiment charger la sauvegarde ? (O/N) ").upper()

            if demandeLoad == "O":
                loadSauvegarde = save_system.load(player)

                if loadSauvegarde == True:
                    audio_engine.sfx_play("ressources/sfx/autoSave.ogg", 2)
                    print("\n\033[1;32mLa sauvegarde a été chargée avec succès.\033[0m")
                    time.sleep(1.5)
                elif loadSauvegarde == None:
                    audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
                    print("\n\033[1;31mErreur. Aucune sauvegarde existante.\033[0m")
                    time.sleep(2)
                elif loadSauvegarde == False:
                    audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
                    print("\n\033[1;31mErreur. La sauvegarde n'a pas pu être chargée.\033[0m")
                    time.sleep(1.5)
                elif loadSauvegarde == 5:
                    audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
                    print("\n\033[1;33mVous avez modifié votre sauvegarde. Elle n'est plus valide.\033[0m")
                    time.sleep(2)
            else:
                audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)

        elif profileAction == "P":
            audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
            settings_menu(player)

        elif profileAction == "Q":
            audio_engine.sfx_play("ressources/sfx/closeProfile.ogg", 1)
            quitTrigger = True

        elif profileAction == "DB":
            oui = str(input("(O/N) ")).upper()
            while oui == "O":
                debug(player)
                oui = str(input("(O/N) ")).upper()

def objects_menu(player, inFight):
    while True:
        print("\n\033[1;34mObjets:\033[0m\n")

        if player.objects == {}:
            print("\033[3m\033[1mVide.\033[0m")
        else:
            for objet in player.objects.keys():
                if (inFight == False and player.objects[objet][1] == False) or player.objects[objet][1] == None:
                    print(f"\033[37m{objet} x{player.objects[objet][0]}\033[0m")
                else:
                    print(f"{objet} \033[1;31mx{player.objects[objet][0]}\033[0m")

        objetAction = input("\nUtiliser (U) / Quitter (Q) ").upper()
        while objetAction != "U" and objetAction != "Q":
            objetAction = input("Utiliser (U) / Quitter (Q) ").upper()

        if objetAction == "U" and player.objects != {}:
            objetChoose = input("Choisissez un objet: ").lower()

            objetChoisis = False
            while objetChoisis == False:
                for objet in player.objects.keys():
                    if objet.lower().startswith(objetChoose):
                        objetChoose = objet
                        objetChoisis = True
                        audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
                if objetChoisis == False:
                    audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
                    objetChoose = input("Incorrect. Quel objet voulez vous utiliser ? ").lower()

            if objects.use_objet(player, objetChoose, inFight) == True and inFight == True:
                return True
            else:
                time.sleep(2)

        elif objetAction == "Q":
            return False
        else:
            print("\n\033[3mAucun objet à utiliser.\033[0m")
            time.sleep(2)

def change_name(player):
    audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
    nameTemp = str(input("Choisissez un nouveau nom. "))
    while len(nameTemp) > 15 or len(nameTemp) < 3 or nameTemp == player.player_name:

        if len(nameTemp) > 15:
            nameTemp = str(input("Le nom est trop long (15 caractères max). Choisissez un nouveau nom. "))
        if len(nameTemp) < 3:
            nameTemp = str(input("Le nom est trop court (3 caractères min). Choisissez un nouveau nom. "))
        if nameTemp == player.player_name:
            nameTemp = str(input("Vous avez choisis le même nom. Choisissez un nom différent du précédent. "))
        audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)

    player.player_name = nameTemp
    print("\n\033[1;32mVotre nom a été changé.\033[0m")
    audio_engine.sfx_play("ressources/sfx/changeApplied.ogg", 1)
    time.sleep(2)

def debug(player):
    audio_engine.music_play('ressources/debug.mp3')
    debugChange = int(input("music easter egg :)\nstats a change Vie[0] Attaque[1], Défense[2], PS[3], EXP[4], Level[5] "))
    while debugChange < 0 or debugChange > 6:
        debugChange = int(input("stats a change Vie[0] Attaque[1], Défense[2], PS[3], EXP[4], Level[5] "))
    if debugChange == 6:
        all = int(input("stat change ALL: "))
        for i in range(len(player.stats)):
            player.stats[i - 1] = all
        for i in range(len(player.stats_max)):
            player.stats_max[i - 1] = all
        return True
    player.stats[debugChange] = int(input("stat change: "))
    if debugChange == 0:
        player.stats_max[0] = player.stats[0]
    elif debugChange == 3:
        player.stats_max[1] = player.stats[3]

# Game Over Screen

def game_over_menu(player):
    audio_engine.sfx_play("ressources/sfx/saveAsk.ogg", 1)
    print(("\n\t \033[4m\033[37mContinuer (C)\033[0m\n"
           if save_system.load(player) != True else
           "\n\t   \033[4mContinuer (C)\033[0m\n") +
          "\t\033[4mMenu Principal (M)\033[0m")

    choixGameOver = input("\t\t\t").upper()

    while choixGameOver != "C" and choixGameOver != "M":
        audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
        choixGameOver = input("\t\t\t").upper()

    if choixGameOver == "C":
        continuer = save_system.load(player)

        if continuer == True:
            print("\n\033[1;32mC'est reparti !\033[0m")
            audio_engine.sfx_play("ressources/sfx/exitTitle.ogg", 2)
            time.sleep(1.25)
        elif continuer == None:
            audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
            print("\n\033[1;1mAucune sauvegarde existante.\033[0m")
            time.sleep(2)
            main_menu(player)

        while player.stats[0] > 0:
            map.game_start(player)
    elif choixGameOver == "M":
        audio_engine.sfx_play("ressources/sfx/selectOption.ogg", 1)
        time.sleep(0.5)
        main_menu(player)