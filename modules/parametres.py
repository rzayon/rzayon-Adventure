import time

import audioEngine
import saveSystem
import menus


#Pour Menu Paramètre
def afficheParametres(player):
    print("\n\t\033[4mParamètres:\033[0m\n")
    for parametre, etatParametre in player.parametres.items():

        if etatParametre == "Activé":
            etatParametre = f"\033[1;32m{etatParametre}\033[0m"
        elif etatParametre == "Desactivé":
            etatParametre = f"\033[1;31m{etatParametre}\033[0m"
        else:
            etatParametre = f"{etatParametre[0]}{etatParametre[1]}\033[0m"

        print(f"\033[4m{parametre}:\033[0m {etatParametre}")

def switchParametreClassic(player, stateParametre):
    if stateParametre == "Activé":
        return "Desactivé"
    elif stateParametre == "Desactivé":
        return "Activé"
    elif isinstance(stateParametre, list):
        return switchParametreCouleur(player)

def switchParametreCouleur(player):
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
def autoSave(playerInfo):
    if playerInfo.parametres["Auto-save"] == "Activé":
        if saveSystem.save(playerInfo) == True:
            print("\033[3m\033[1mSauvegarde automatique...\033[0m")
            audioEngine.sfxPlay("ressources/sfx/autoSave.ogg", 2)
            return True
        else:
            audioEngine.sfxPlay("ressources/sfx/wrongChoice.ogg", 2)
            print("\033[3m\033[1mÉchec de la sauvegarde automatique.\033[0m")
            return None
    else:
        return False

def affichePseudoCouleur(player):
    return player.parametres["Couleur du pseudo"][0] + player.nom + "\033[0m"