import time
import os
import shutil
import json

import misc

def save(playerInfo):
    if len(playerInfo.stats) != 6 or len(playerInfo.statsMax) != 2:
        return False

    saveData = str(playerInfo.nom) + "\n" + ",".join(map(str, playerInfo.stats)) + '\n' + ",".join(map(str, playerInfo.statsMax)) + '\n' + str(playerInfo.deplacementHauteur) + '\n' + str(playerInfo.parametres) + '\n' + str(playerInfo.tutorielDone) + '\n'

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
    if len(save.readlines()) != 8:
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

        if len(saveView.readlines()) != 8:
            misc.closeRemove(saveView, 'saves/saveTemp.txt')
            return False

        saveView = open('saves/saveTemp.txt', "r")

        nomTemp = ""
        statsTemp = []
        statsMaxTemp = []
        delacementHauteurTemp = 0
        mapTemp = []
        parametresTemp = {}
        tutorielDoneTemp = {}

        nomTemp = saveView.readline().strip()

        for stat in saveView.readline().strip().split(','):
            try:
                int(stat)
                statsTemp.append(int(stat))
            except ValueError:
                misc.closeRemove(saveView, 'saves/saveTemp.txt')
                return False

        for maxStats in saveView.readline().strip().split(','):
            try:
                int(maxStats)
                statsMaxTemp.append(int(maxStats))
            except ValueError:
                misc.closeRemove(saveView, 'saves/saveTemp.txt')
                return False

        delacementHauteurTemp = saveView.readline().strip()
        try:
            int(delacementHauteurTemp)
            delacementHauteurTemp = int(delacementHauteurTemp)
        except ValueError:
            misc.closeRemove(saveView, 'saves/saveTemp.txt')
            return False

        parametresTemp = eval(saveView.readline().strip())
        if len(parametresTemp) != 2:
            misc.closeRemove(saveView, 'saves/saveTemp.txt')
            return False

        tutorielDoneTemp = eval(saveView.readline().strip())
        if len(tutorielDoneTemp) != 2:
            misc.closeRemove(saveView, 'saves/saveTemp.txt')
            return False

        for elementMap in saveView.readline().strip().split(","):
            mapTemp.append(elementMap)
            if mapTemp[len(mapTemp) - 1] == "\\n":
                mapTemp[len(mapTemp) - 1] = "\n"

        if int(saveView.readline()) != int(os.path.getmtime("saves/save.sav") / 4.628154):
            misc.closeRemove(saveView, 'saves/saveTemp.txt')
            return 5

        if len(nomTemp) != 0 and len(statsTemp) == 6 and len(statsMaxTemp) == 2 and delacementHauteurTemp > 1 and len(parametresTemp) == 2 and len(tutorielDoneTemp) == 2:
            playerInfo.nom = nomTemp
            playerInfo.stats = statsTemp
            playerInfo.statsMax = statsMaxTemp
            playerInfo.deplacementHauteur = delacementHauteurTemp
            playerInfo.parametres = parametresTemp
            playerInfo.tutorielDone = tutorielDoneTemp
            playerInfo.map = mapTemp
        else:
            misc.closeRemove(saveView, 'saves/saveTemp.txt')
            return False

        misc.closeRemove(saveView, 'saves/saveTemp.txt')

        misc.verifStats(playerInfo)
        return True
    else:
        return None