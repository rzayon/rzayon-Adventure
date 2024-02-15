""" Ce module comporte des fonctions pour sauvegarder et charger la partie du joueur. """


import time
import os
import shutil
import json

from modules import misc

def save(playerInfo):
    if len(playerInfo.stats) != 7 or len(playerInfo.stats_max) != 2:
        return False

    saveData = str(playerInfo.player_name) + "\n" + ",".join(map(str, playerInfo.stats)) + '\n' + ",".join(map(str, playerInfo.stats_max)) + '\n' + str(playerInfo.y_movement) + '\n' + str(playerInfo.objects) + '\n' + str(playerInfo.settings) + '\n' + str(playerInfo.tutorial_triggers) + '\n'

    for e in str(playerInfo.map)[1:-1]:
        if e != "'":
            saveData += e.strip()

    saveData += "\n" + str(int(time.time() / 4.628154))

    if not os.path.exists("saves"):
        os.makedirs("saves")

    if os.path.exists("saves/saveTemp.txt"):
        os.remove("saves/saveTemp.txt")

    save = open("saves/saveTemp.txt", "a")
    save.write(saveData)

    save = open("saves/saveTemp.txt", "r")
    if len(save.readlines()) != 9:
        return False

    if os.path.exists("saves/save.sav"):
        os.remove("saves/save.sav")

    save.close()
    os.rename("saves/saveTemp.txt", "saves/save.sav")
    return True

def load(playerInfo):
    if os.path.exists("saves/save.sav"):
        shutil.copy('saves/save.sav', 'saves/saveTemp.txt')
        saveView = open('saves/saveTemp.txt', "r")

        if len(saveView.readlines()) != 9:
            misc.close_remove(saveView, 'saves/saveTemp.txt')
            return False

        saveView = open('saves/saveTemp.txt', "r")

        player_nom_temp = ""
        stats_temp = []
        stats_max_temp = []
        y_movement_temp = 0
        objects_temp = {}
        settings_temp = {}
        tutorial_triggers_temp = {}
        map_temp = []

        # Load Nom
        player_nom_temp = saveView.readline().strip()

        # Load Stats
        for stat in saveView.readline().strip().split(','):
            try:
                int(stat)
                stats_temp.append(int(stat))
            except ValueError:
                misc.close_remove(saveView, 'saves/saveTemp.txt')
                return False

        # Load Max Stats
        for maxStats in saveView.readline().strip().split(','):
            try:
                int(maxStats)
                stats_max_temp.append(int(maxStats))
            except ValueError:
                misc.close_remove(saveView, 'saves/saveTemp.txt')
                return False

        # Load Déplacement Hauteur
        y_movement_temp = saveView.readline().strip()
        try:
            int(y_movement_temp)
            y_movement_temp = int(y_movement_temp)
        except ValueError:
            misc.close_remove(saveView, 'saves/saveTemp.txt')
            return False

        # Load Objets
        try:
            objects_temp = eval(saveView.readline().strip())
        except ValueError:
            misc.close_remove(saveView, 'saves/saveTemp.txt')
            return False

        # Load Paramètres
        try:
            settings_temp = eval(saveView.readline().strip())
        except ValueError:
            misc.close_remove(saveView, 'saves/saveTemp.txt')
            return False

        # Load Tutoriel Info
        try:
            tutorial_triggers_temp = eval(saveView.readline().strip())
        except ValueError:
            misc.close_remove(saveView, 'saves/saveTemp.txt')
            return False

        # Load Map
        for elementMap in saveView.readline().strip().split(","):
            map_temp.append(elementMap)
            if map_temp[len(map_temp) - 1] == "\\n":
                map_temp[len(map_temp) - 1] = "\n"

        # Check Anti Cheat
        if int(saveView.readline()) != int(os.path.getmtime("saves/save.sav") / 4.628154):
            misc.close_remove(saveView, 'saves/saveTemp.txt')
            return 5

        # Load in player
        if len(player_nom_temp) != 0 and len(stats_temp) == 6 and len(stats_max_temp) == 2 and y_movement_temp > 1 and len(settings_temp) == 2 and len(tutorial_triggers_temp) == 2:
            playerInfo.player_name = player_nom_temp
            playerInfo.stats = stats_temp
            playerInfo.stats_max = stats_max_temp
            playerInfo.y_movement = y_movement_temp
            playerInfo.objects = objects_temp
            playerInfo.settings = settings_temp
            playerInfo.tutorial_triggers = tutorial_triggers_temp
            playerInfo.map = map_temp
        else:
            misc.close_remove(saveView, 'saves/saveTemp.txt')
            return False

        misc.close_remove(saveView, 'saves/saveTemp.txt')

        misc.check_stats(playerInfo)
        return True
    else:
        return None