""" Module gérant la gestion des objets. """

import random
import time

from engines import audio_engine

from modules import objects_list
from modules import misc

def delete_item(player, objetUsed):
    player.objects[objetUsed][0] -= 1
    if player.objects[objetUsed][0] == 0:
        player.objects.pop(objetUsed)

def use_objet(player, objetUsed, inFight):
    if player.objects[objetUsed][1] == True or (player.objects[objetUsed][1] == False and inFight == True):
        if objets_effects(player, objetUsed, inFight) == True:
            delete_item(player, objetUsed)
            return True
    else:
        print("\n\033[1mVous ne pouvez pas utiliser cet objet maintenant.\033[0m")
        return False

    time.sleep(1)

def objets_effects(player, objet, inFight):
    objetCheck = objet.lower()

    # Objets Heal
    if objetCheck.startswith("champi"):
        if player.stats[0] != player.stats_max[0]:
            player.stats[0] += player.objects[objet][2]
            if objetCheck == "champi prodige":
                audio_engine.sfx_play("ressources/sfx/fullRegen.ogg", 2)
                print("\nVous avez regagné \033[1;32mtout vos PV\033[0m.")
            else:
                audio_engine.sfx_play("ressources/sfx/champiRegen.ogg", 2)
                print(f"\nPV \033[1;32m+ {player.objects[objet][2]}\033[0m")
            misc.check_stats(player)
            return True
        else:
            print("Vous êtes déjà au maximum de PV.")

    # Objets Attack
    elif objetCheck == "fleur carnivore" or objetCheck == "grosse pierre":
        player.stats_enemy[0] -= player.objects[objet][2]
        print(f"Votre \033[1;33m{objet}\033[0m a infligé \033[1;31m{player.objects[objet][2]}\033[0m de dégats à l'ennemi.")
        time.sleep(1.5)

        if player.stats_enemy[0] > 0:
            state_trigger = random.random()

            if objetCheck == "fleur carnivore" and state_trigger < 0.95:
                player.states_enemy["poison"] = [random.randint(2, 5), "🧪"]
                print("L'ennemi est empoisonné.")
                time.sleep(2)

            elif objetCheck == "grosse pierre" and state_trigger < 0.92:
                player.states_enemy["étourdis"] = [random.randint(2, 3), "💫"]
                print("L'ennemi est étourdis.")
                time.sleep(2)

        return True

    # Objets Boost
    elif objetCheck.startswith("potion") or objetCheck.startswith("bouclier"):
        player.stats_boost[player.objects[objet][3]][0] = player.objects[objet][2]
        player.stats_boost[player.objects[objet][3]][1] = 4

        if objetCheck.startswith("potion"):
            print("\n\033[1;32m\033[1;1m\033[1;3mAtt ++\033[0m\n")
        else:
            print("\n\033[1;32m\033[1;1m\033[1;3mDéf ++\033[0m\n")

        return True

    else:
        print("debug, ca existe pas, aucun objet bg")

def totem_regen(player):
    if "Totem Gardien" in player.objects.keys():
        player.stats[0] = player.stats_max[0]
        delete_item(player, "Totem Gardien")
        return "Totem Gardien"
    elif "Totem" in player.objects.keys():
        player.stats[0] = int(player.stats_max[0] / 2)
        delete_item(player, "Totem")
        return "Totem"

    else:
        return False

def objects_infos(player):
    if player.objects != {}:
        print()
        for object in player.objects.keys():
            print(f"{object}: \033[1;33m{objects_list.objects_info[object]}\033[0m")