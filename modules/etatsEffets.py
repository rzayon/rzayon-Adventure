import random
import time

import parametres

def afficheEffets(effetCible):
    if effetCible == {} or all(tourEtat[0] == 0 for tourEtat in effetCible.values()):
        return False
    else:
        listeEffets = ""
        for i in effetCible.keys():
            if effetCible[i][0] > 0:
                listeEffets += effetCible[i][1]

        listeEffets += "\n"
        return listeEffets

def detectEtat(player):

    if player.etats == {} and player.statsEnnemi == {}:
        return False

    if player.stats[0] > 0 and player.etats != {}:
        for etat in player.etats.keys():
            if player.etats[etat][0] > 0:
                player.stats[0] = etatsEffets(etat, player.stats[0], parametres.affichePseudoCouleur(player))
                player.etats[etat][0] = effetTourDetect(player.etats[etat][0], etat)

    if player.statsEnnemi[0] > 0 and player.etatsEnnemi != {}:
        for etatEnnemi in player.etatsEnnemi.keys():
            if player.etatsEnnemi[etatEnnemi][0] > 0:
                player.statsEnnemi[0] = etatsEffets(etatEnnemi, player.statsEnnemi[0], player.statsEnnemi[4])
                player.etatsEnnemi[etatEnnemi][0] = effetTourDetect(player.etatsEnnemi[etatEnnemi][0], etatEnnemi)

def etatsEffets(etat, vieCible, nomCible):
    if etat == "feu":
        feuDegat = random.randint(4, 6)
        vieCible -= feuDegat
        print(nomCible, "brulé. -", feuDegat, "dégats.")
        return vieCible

    elif etat == "poison":
        poisonDegat = random.randint(8, 10)
        vieCible -= poisonDegat
        print(nomCible, "empoisonné. -", poisonDegat, "dégats.")
        return vieCible

    elif etat == "étourdis":
        etourdisDegat = random.randint(6, 12)
        vieCible -= etourdisDegat
        print(nomCible, "étourdis. -", etourdisDegat, "dégats. (GG)")
        return vieCible

def effetTourDetect(tourEffet, etat):

    tourEffet -= 1
    time.sleep(1)
    if tourEffet == 0:
        print("\x1B[3mFin", etat + ".\x1B[0m")
    return tourEffet

def resetEtats(player):
    player.etats = {}
    player.etatsEnnemi = {}