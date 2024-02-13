import sys
import time
import random
import keyboard

import audioEngine
import saveSystem
import parametres
import map
import levelXP
import misc

#Title Screen

def titleScreen(player, trigger):

    audioEngine.musicPlay("ressources/title.mp3")

    if trigger == False:
        time.sleep(1.2)
        print("\t\033[1;33m  \033[4mrzayon's Adventure\033[0m")
        time.sleep(2)
        print("\n\t\033[4mAppuyez pour commencer\033[0m\n\t\t  "
              "\033[1;1mbeta", player.gameVersion + "\033[0m")
        keyboard.read_event(suppress=True)
        audioEngine.sfxPlay("ressources/sfx/exitTitle.ogg", 1)
        misc.transitionMenu(1)

    else:
        time.sleep(1.2)
        print("\n\t\033[1;33m  \033[4mrzayon's Adventure\033[0m\n\n"
              "\t\033[4mAppuyez pour commencer\033[0m"
              "\n\t\t  \033[1;1mbeta", player.gameVersion + "\033[0m")
        keyboard.read_event(suppress = True)
        audioEngine.sfxPlay("ressources/sfx/exitTitle.ogg", 1)
        misc.transitionMenu(0.5)

    mainMenu(player)

#Main Menu

def mainMenu(player):

    audioEngine.musicPlay("ressources/mainMenu.mp3")

    print("\n\t\033[1;33m  \033[4mrzayon's Adventure\033[0m\n\n"
          "\t  \033[4mNouvelle Partie (N)\033[0m\n" +

         ("\t     \033[4m\033[37mContinuer (C)\033[0m\n"
           if saveSystem.load(player) != True else
          "\t     \033[4mContinuer (C)\033[0m\n") +

          "\t     \033[4mParamètre (P)\033[0m\n"
          "\t    \033[4mÉcran Titre (T)\033[0m\n"
          "\t      \033[4mQuitter (Q)\033[0m")

    mainMenuChoix = input("\t\t\t   ").upper()
    while mainMenuChoix != "N" and mainMenuChoix != "C" and mainMenuChoix != "P" and mainMenuChoix != "T" and mainMenuChoix != "Q":
        mainMenuChoix = input("\t\t\t   ").upper()

    if mainMenuChoix == "N":
        nouvellePartie(player)
        audioEngine.sfxPlay("ressources/sfx/gameStart.ogg", 1)
        print("\n\033[1;32m\033[1;1mNouvelle partie commencer !\033[0m")
        misc.transitionMenu(3)
        while player.stats[0] > 0:
            map.partie(player)

    elif mainMenuChoix == "C":

        continuer = saveSystem.load(player)

        if continuer == True:
            print("\n\033[1;32mVotre partie s'est chargée.\033[0m")
            audioEngine.sfxPlay("ressources/sfx/autoSave.ogg", 2)
            misc.transitionMenu(3)
            while player.stats[0] > 0:
                map.partie(player)
        elif continuer == None:
            audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
            print("\n\033[1;1mAucune partie existante.\033[0m")
            time.sleep(2.5)
            mainMenu(player)
        else:
            audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
            print("\n\033[1;31mLa partie n'a pas pu se charger.\033[0m")
            time.sleep(2.5)
            mainMenu(player)

    elif mainMenuChoix == "P":
        audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)
        parametreMenu(player)
        mainMenu(player)

    elif mainMenuChoix == "T":
        audioEngine.sfxPlay("ressources/sfx/close.ogg", 1)
        misc.transitionMenu(0.2)
        titleScreen(player, True)

    elif mainMenuChoix == "Q":
        audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)
        quitter = input("\nVoulez vous vraiment quitter ? (O/N) ").upper()
        while quitter != "O" and quitter != "N":
            quitter = input("\033[1;33mIncorrect. Voulez vous vraiment quitter ? (O/N)\033[0m ").upper()

        if quitter == "O":
            misc.fermerJeu()
        else:
            audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)
            mainMenu(player)

def nouvellePartie(player):
    player.nom = "Player"
    player.stats = [25, 12, 10, 10, 0, 1]
    player.statsMax = [25, 10]
    player.objets = {}
    player.map = []

    player.tutorielDone = {"fightFirstTime": True, "mapFirstTime": True}

    while "[J]" not in player.map:
        newMap(player, random.randint(7, 9), random.randint(11, 14))

def newMap(player, nbLigne, nbElement):

    mapLigne = []
    nbEnnemi = 0

    while nbEnnemi <= 15:
        player.map = []
        nbEnnemi = 0

        for ligne in range(nbLigne):
            mapLigne.append("[M]")

            for element in range(nbElement):
                if random.random() < 0.09:
                    mapLigne.append("[E]")
                    nbEnnemi += 1
                elif int(nbLigne / 2) == ligne and int(nbElement / 2) == element:
                    mapLigne.append("[J]")
                else:
                    mapLigne.append("[.]")

            mapLigne.append("[M]")
            player.map += ["\n"] + mapLigne
            player.deplacementHauteur = len(mapLigne) + 1
            mapLigne = []

    selectedTower = random.randint(0, len(player.map) - 1)

    while player.map[selectedTower] != "[.]":
        selectedTower = random.randint(0, len(player.map) - 1)
    player.map[selectedTower] = "[T]"

def parametreMenu(player):

    audioEngine.musicVolumeLower()

    parametres.afficheParametres(player)

    actionParametre = input("\nChanger un paramètre (C) / Quitter (Q) ").upper()
    while actionParametre != "C" and actionParametre != "Q":
        audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
        actionParametre = input("Changer un paramètre (C) / Quitter (Q) ").upper()

    if actionParametre == "C":
        audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)
        choixTrigger = False
        choixChangement = input("Quel paramètre voulez changer ? ").lower()

        while choixTrigger == False:
            for parametre in player.parametres.keys():
                if parametre.lower().startswith(choixChangement):
                    choixChangement = parametre
                    choixTrigger = True
                    audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)
            if choixTrigger == False:
                audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
                choixChangement = input("Parametre incorrect. Quel paramètre voulez changer ? ").lower()

        player.parametres[choixChangement] = parametres.switchParametreClassic(player, player.parametres[choixChangement])

        audioEngine.sfxPlay("ressources/sfx/changeApplied.ogg", 1)
        print("\n\033[1;32mParamètre changé.\033[0m")
        time.sleep(2)

        parametreMenu(player)

    elif actionParametre == "Q":
        audioEngine.musicVolumeReset()
        audioEngine.sfxPlay("ressources/sfx/close.ogg", 1)
        return False

#Profile Menu

def profile(player):

    audioEngine.musicPlay("ressources/profile.mp3")

    quitTrigger = False
    while quitTrigger == False:

        print(f"\n{parametres.affichePseudoCouleur(player)}\n\n"
              f"Level {player.stats[5]} | EXP: {player.stats[4]}\n"
              f"\033[1;1mProchain niveau dans: \033[1;33m{levelXP.levels[player.stats[5] + 1] - player.stats[4]}\033[0m \033[1;1mEXP\033[0m\n\n"
              f"Vie: {player.stats[0]}/{str(player.statsMax[0])}\n"
              f"Attaque: {player.stats[1]}\n"
              f"Défense: {player.stats[2]}\n"
              f"PS: {player.stats[3]}/{player.statsMax[1]}\n")

        profileAction = input("Objet (O) / Changer de nom (C) / Sauvegarder (S) / Load (L) / Paramètres (P) / Quitter (Q) ").upper()
        while profileAction != "O" and profileAction != "C" and profileAction != "S" and profileAction != "L" and profileAction != "P" and profileAction != "Q" and profileAction != "DB":
            profileAction = input("Objet (O) / Changer de nom (C) / Sauvegarder (S) / Load (L) / Paramètres (P) / Quitter (Q) ").upper()

        if profileAction == "O":
            audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)
            print("wip (pitié que j'ai pas la flemme ptdrr)")
            time.sleep(3)

        elif profileAction == "C":
            audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)
            changeNom = input("Voulez vous changer de nom ? (O/N) ").upper()
            while changeNom != "O" and changeNom != "N":
                audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
                changeNom = input("Reponse incorrecte. Voulez vous changer de nom ? (O/N) ").upper()
            if changeNom == "O":
                changementNom(player)
            else:
                audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)

        elif profileAction == "S":

            audioEngine.sfxPlay("ressources/sfx/saveAsk.ogg", 1)
            demandeSave = input("Voulez vous vraiment sauvegarder ? Cela écrasera votre ancienne sauvegarde. (O/N) ").upper()
            while demandeSave != "O" and demandeSave != "N":
                audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
                demandeSave = input("Reponse incorrecte. Voulez vous vraiment sauvegarder ? (O/N) ").upper()

            if demandeSave == "O":
                saveSauvegarde = saveSystem.save(player)

                if saveSauvegarde == True:
                    audioEngine.sfxPlay("ressources/sfx/saveSuccess.ogg", 2)
                    print("\n\033[1;32mLa partie a été sauvegardée.\033[0m")
                    time.sleep(1.5)
                else:
                    audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
                    print("\n\033[1;31mErreur. La partie n'a pas pu être sauvegardé.\033[0m")
                    time.sleep(0.5)
            else:
                audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)

        elif profileAction == "L":

            audioEngine.sfxPlay("ressources/sfx/saveAsk.ogg", 1)
            demandeLoad = input("Voulez vous vraiment charger la sauvegarde ? Cela écrasera votre progression actuelle. (O/N) ").upper()
            while demandeLoad != "O" and demandeLoad != "N":
                audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
                demandeLoad = input("Reponse incorrecte. Voulez vous vraiment charger la sauvegarde ? (O/N) ").upper()

            if demandeLoad == "O":
                loadSauvegarde = saveSystem.load(player)

                if loadSauvegarde == True:
                    audioEngine.sfxPlay("ressources/sfx/autoSave.ogg", 2)
                    print("\n\033[1;32mLa sauvegarde a été chargée avec succès.\033[0m")
                    time.sleep(1.5)
                elif loadSauvegarde == None:
                    audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
                    print("\n\033[1;31mErreur. Aucune sauvegarde existante.\033[0m")
                    time.sleep(2)
                elif loadSauvegarde == False:
                    audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
                    print("\n\033[1;31mErreur. La sauvegarde n'a pas pu être chargée.\033[0m")
                    time.sleep(1.5)
                elif loadSauvegarde == 5:
                    audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
                    print("\n\033[1;33mVous avez modifié votre sauvegarde. Elle n'est plus valide.\033[0m")
                    time.sleep(2)
            else:
                audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)

        elif profileAction == "P":
            audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)
            parametreMenu(player)

        elif profileAction == "Q":
            audioEngine.sfxPlay("ressources/sfx/closeProfile.ogg", 1)
            quitTrigger = True

        elif profileAction == "DB":
            oui = str(input("(O/N) ")).upper()
            while oui == "O":
                debug(player)
                oui = str(input("(O/N) ")).upper()

def changementNom(player):
    audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)
    nameTemp = str(input("Choisissez un nouveau nom. "))
    while len(nameTemp) > 15 or len(nameTemp) < 3 or nameTemp == player.nom:

        if len(nameTemp) > 15:
            nameTemp = str(input("Le nom est trop long (15 caractères max). Choisissez un nouveau nom. "))
        if len(nameTemp) < 3:
            nameTemp = str(input("Le nom est trop court (3 caractères min). Choisissez un nouveau nom. "))
        if nameTemp == player.nom:
            nameTemp = str(input("Vous avez choisis le même nom. Choisissez un nom différent du précédent. "))
        audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)

    player.nom = nameTemp
    print("\n\033[1;32mVotre nom a été changé.\033[0m")
    audioEngine.sfxPlay("ressources/sfx/changeApplied.ogg", 1)
    time.sleep(2)

def debug(player):
    audioEngine.musicPlay('ressources/debug.mp3')
    debugChange = int(input("music easter egg :)\nstats a change Vie[0] Attaque[1], Défense[2], PS[3], EXP[4], Level[5] "))
    while debugChange < 0 or debugChange > 6:
        debugChange = int(input("stats a change Vie[0] Attaque[1], Défense[2], PS[3], EXP[4], Level[5] "))
    if debugChange == 6:
        all = int(input("stat change ALL: "))
        for i in range(len(player.stats)):
            player.stats[i - 1] = all
        for i in range(len(player.statsMax)):
            player.statsMax[i - 1] = all
        return True
    player.stats[debugChange] = int(input("stat change: "))
    if debugChange == 0:
        player.statsMax[0] = player.stats[0]
    elif debugChange == 3:
        player.statsMax[1] = player.stats[3]

# Game Over

def gameOverChoice(player):
    audioEngine.sfxPlay("ressources/sfx/saveAsk.ogg", 1)
    print(("\n\t \033[4m\033[37mContinuer (C)\033[0m\n"
           if saveSystem.load(player) != True else
           "\n\t   \033[4mContinuer (C)\033[0m\n") +
          "\t\033[4mMenu Principal (M)\033[0m")

    choixGameOver = input("\t\t\t").upper()

    while choixGameOver != "C" and choixGameOver != "M":
        audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
        choixGameOver = input("\t\t\t").upper()

    if choixGameOver == "C":
        continuer = saveSystem.load(player)

        if continuer == True:
            print("\n\033[1;32mC'est reparti !\033[0m")
            audioEngine.sfxPlay("ressources/sfx/exitTitle.ogg", 2)
            time.sleep(1.25)
        elif continuer == None:
            audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
            print("\n\033[1;1mAucune sauvegarde existante.\033[0m")
            time.sleep(2)
            mainMenu(player)

        while player.stats[0] > 0:
            map.partie(player)
    elif choixGameOver == "M":
        audioEngine.sfxPlay("ressources/sfx/selectOption.ogg", 1)
        time.sleep(0.5)
        mainMenu(player)