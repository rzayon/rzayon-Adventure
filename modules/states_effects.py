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

def display_boosts(player_boosts):
    if all(boost_round[1] == 0 for boost_round in player_boosts.values()):
        return ""
    else:
        boost_list = ""
        for boost in player_boosts.keys():
            if player_boosts[boost][1] > 0:
                boost_list += player_boosts[boost][2]

        return boost_list

def detect_state(player):

    if player.states == {} and all(boost_round[1] == 0 for boost_round in player.stats_boost.values()) and player.stats_enemy == {}:
        return False

    if player.stats[0] > 0 and player.states != {}:
        for state in player.states.keys():
            if player.states[state][0] > 0:
                player.stats[0] = state_effects(state, player.stats[0], parametres.affichePseudoCouleur(player))
                player.states[state][0] = effect_duration_detect(player.states[state][0], state)

    if all(boost_round[1] == 0 for boost_round in player.stats_boost.values()) == False:
        for boost in player.stats_boost.keys():
            if player.stats_boost[boost][1] > 0:
                player.stats_boost[boost][1] = boost_duration_detect(player.stats_boost, boost)

    if player.stats_enemy[0] > 0 and player.states_enemy != {}:
        for state_enemy in player.states_enemy.keys():
            if player.states_enemy[state_enemy][0] > 0:
                player.stats_enemy[0] = state_effects(state_enemy, player.stats_enemy[0], player.stats_enemy[4])
                player.states_enemy[state_enemy][0] = effect_duration_detect(player.states_enemy[state_enemy][0], state_enemy)

def state_effects(state, vieCible, nomCible):
    if state == "feu":
        feuDegat = random.randint(5, 8)
        vieCible -= feuDegat
        print(nomCible, "brulé. \033[1;31m-", feuDegat, "dégats\033[0m")

    elif state == "poison":
        poisonDegat = random.randint(8, 10)
        vieCible -= poisonDegat
        print(nomCible, "empoisonné. \033[1;31m-", poisonDegat, "dégats\033[0m")

    elif state == "étourdis":
        etourdisDegat = random.randint(4, 6)
        vieCible -= etourdisDegat
        print(nomCible, "étourdis. \033[1;31m-", etourdisDegat, "dégats.\033[0m")

    time.sleep(1)
    return vieCible

def effect_duration_detect(tourEffet, state):

    tourEffet -= 1
    time.sleep(1)
    if tourEffet == 0:
        print("\x1B[3mFin", state + ".\x1B[0m")
    return tourEffet

def boost_duration_detect(player_boost, boost):

    boost_counter = player_boost[boost][1] - 1
    time.sleep(1)
    if boost_counter == 0:
        print("\x1B[3mFin", boost + " boost.\x1B[0m")
        player_boost[boost][0] = 0
    return boost_counter


# Pour tout reset (tah mbappe)
def reset_state(player):
    player.states = {}

    # oui c comme ça que je met ça par défaut pcq sinon c chiant jpp, fais cque tu veux avec pcq ya mieux mais turbo flemme pour l'instant
    player.stats_boost = {"att": [0, 0, "⚔️"], "déf": [0, 0, "🛡️"]}

    player.states_enemy = {}