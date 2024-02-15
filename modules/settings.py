import time

from engines import audio_engine

from modules import save_system


#Pour Menu Paramètre
def display_settings(player):
    print("\n\t\033[4mParamètres:\033[0m\n")
    for parametre, etatParametre in player.settings.items():

        if etatParametre == "Activé":
            etatParametre = f"\033[1;32m{etatParametre}\033[0m"
        elif etatParametre == "Desactivé":
            etatParametre = f"\033[1;31m{etatParametre}\033[0m"
        else:
            etatParametre = f"{etatParametre[0]}{etatParametre[1]}\033[0m"

        print(f"\033[4m{parametre}:\033[0m {etatParametre}")

def switch_setting_classic(player, stateParametre):
    if stateParametre == "Activé":
        return "Desactivé"
    elif stateParametre == "Desactivé":
        return "Activé"
    elif isinstance(stateParametre, list):
        return switch_setting_color(player)

def switch_setting_color(player):
    couleurs = {"Bleu": "\033[1;34m",
                "Rouge": "\033[1;31m",
                "Vert": "\033[1;32m",
                "Jaune": "\033[1;33m",
                "Violet": "\033[1;35m",
                "Cyan": "\033[1;36m"}

    affichageCouleurs = ""
    for couleur in couleurs.keys():
        affichageCouleurs += f"{couleurs[couleur]}{couleur}\033[0m, "

    demandeCouleur = input(f"Quel couleur voulez vous choisir ?\n\n{affichageCouleurs}").capitalize()

    choixCouleur = False
    while choixCouleur == False:
        for couleur in couleurs.keys():
            if couleur.startswith(demandeCouleur):
                demandeCouleur = couleur
                choixCouleur = True
        if choixCouleur == False:
            demandeCouleur = input(f"Quel couleur voulez vous choisir ?\n\n{affichageCouleurs}").capitalize()

    return [couleurs[demandeCouleur], demandeCouleur]


#Application des paramètres
def auto_save(playerInfo):
    if playerInfo.settings["Auto-save"] == "Activé":
        if save_system.save(playerInfo) == True:
            print("\033[3m\033[1mSauvegarde automatique...\033[0m")
            audio_engine.sfx_play("ressources/sfx/autoSave.ogg", 2)
            return True
        else:
            audio_engine.sfx_play("ressources/sfx/wrongChoice.ogg", 2)
            print("\033[3m\033[1mÉchec de la sauvegarde automatique.\033[0m")
            return None
    else:
        return False

def display_name_color(player):
    return player.settings["Couleur du pseudo"][0] + player.player_name + "\033[0m"