""" Module pour les effets de statut (états) du joueur et de l'ennemi. """


import random
import time

def display_effects(effetCible):
    if effetCible == {} or all(tourEtat[0] == 0 for tourEtat in effetCible.values()):
        return False
    else:
        listeEffets = ""
        for i in effetCible.keys():
            if effetCible[i][0] > 0:
                listeEffets += effetCible[i][1]

        listeEffets += "\n"
        return listeEffets

def detect_state(player):

    if player.states == {} and player.stats_enemy == {}:
        return False

    if player.stats[0] > 0 and player.states != {}:
        for state in player.states.keys():
            if player.states[state][0] > 0:
                player.stats[0] = state_effects(state, player.stats[0], parametres.affichePseudoCouleur(player))
                player.states[state][0] = effect_duration_detect(player.states[state][0], state)

    if player.stats_enemy[0] > 0 and player.states_enemy != {}:
        for state_enemy in player.states_enemy.keys():
            if player.states_enemy[state_enemy][0] > 0:
                player.stats_enemy[0] = state_effects(state_enemy, player.stats_enemy[0], player.stats_enemy[4])
                player.states_enemy[state_enemy][0] = effect_duration_detect(player.states_enemy[state_enemy][0], state_enemy)

def state_effects(state, vieCible, nomCible):
    if state == "feu":
        feuDegat = random.randint(4, 6)
        vieCible -= feuDegat
        print(nomCible, "brulé. -", feuDegat, "dégats.")
        return vieCible

    elif state == "poison":
        poisonDegat = random.randint(8, 10)
        vieCible -= poisonDegat
        print(nomCible, "empoisonné. -", poisonDegat, "dégats.")
        return vieCible

    elif state == "étourdis":
        etourdisDegat = random.randint(6, 12)
        vieCible -= etourdisDegat
        print(nomCible, "étourdis. -", etourdisDegat, "dégats. (GG)")
        return vieCible

def effect_duration_detect(tourEffet, state):

    tourEffet -= 1
    time.sleep(1)
    if tourEffet == 0:
        print("\x1B[3mFin", state + ".\x1B[0m")
    return tourEffet

def reset_state(player):
    player.states = {}
    player.states_enemy = {}