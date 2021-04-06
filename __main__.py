"""
Module principal du package pymafia.
C'est ici le point d'entrée du programme.
Ce module définit 3 fonctions ainsi que les commandes principales qui lancent le jeu.
"""
from pymafia.partie import Partie

def demander_nombre_joueurs():
    """
    Fonction qui demande à l'utilisateur combien de joueurs entre 2 et 8 vont jouer une partie de pymafia.
    Les validations sont faites sur la valeur entrée par l'utilisateur et le programme redemande un nombre
    si la valeur entrée est invalide.
    Returns:
        int: le nombre de joueurs choisi par l'utilisateur
    """
    nombre_total = input("À combien de joueurs voulez-vous jouer la partie de pymafia? (entre 2 et 8) ")
    while not (nombre_total.isnumeric() and int(nombre_total) <= 8 and int(nombre_total) >= 2):
        nombre_total = input("Erreur! Veuillez entrez un nombre de joueur entre 2 et 8 seulement: ")
    return int(nombre_total)


def demander_nombre_joueurs_humains(nombre_joueurs):
    """
    Fonction qui demande le nombre de joueurs humains qui seront parmi les joueurs. Les autres joueurs
    seront contrôlés par l'ordinateur. Les validations sont faites sur la valeur entrée par l'utilisateur
    et le programme redemande un nombre si la valeur entrée est invalide. Cette valeur doit bien sûr être
    inférieure ou égale au nombre de joueurs.
    Args:
        nombre_joueurs (int): nombre de joueurs voulu par l'utilisateur.
    Returns:
        int: le nombre de joueurs humains choisi par l'utilisateur
    """
    nombre_joueur_humain = input("Parmis ces " + str(nombre_joueurs) + " joueurs, combien y a-t-il d'humains?  ")
    while not (nombre_joueur_humain.isnumeric() and int(nombre_joueur_humain) <= nombre_joueurs and int(
            nombre_joueur_humain) >= 1):
        nombre_joueur_humain = input("Erreur! Veuillez entrez un nombre de joueur entre 1 et " + str(nombre_joueurs) +
                                     " seulement: ")
    return int(nombre_joueur_humain)


def afficher_instructions():
    """
    Fonction qui affiche les instructions du jeu.
    """
    print("""Voici les instruction du jeux!

Vous pouvez jouer entre 2 et 8 joueurs, mais le jeu est plus enlevant entre 3 et 5 joueurs.
Au départ, chaque joueur dispose de 5 dés traditionnels à 6 faces et un total de 100
points

Le jeu comporte 10 ronde. Avant le début de la première ronde, chaque joueur 
joue deux dés. Le joueur ayant le plus haut résultat commencera. Tant qu’il y a égalité au plus haut score entre 
plusieurs joueurs, ces derniers relancent les dés. Le jeu peut se jouer autant dans 
le sens horaire (1) qu’anti-horaire (-1). C’est le premier joueur qui décide.

Lorsque c’est son tour, un joueur roule tous ses dés. Les dés ayant la valeur 6 sont passés
au prochain joueur. Les dés de valeur 1 sont retirés du jeu.

Le jeu continue jusqu’à ce qu’un joueur n’ait plus aucun dé. Ceci termine la ronde. Les
autres joueurs roulent alors leurs dés restants et comptent le total des dés. Ils perdent alors
le nombre de points obtenus sur les dés et donnent ces points au gagnant de la ronde.
Si un joueur vient à ne plus avoir de point, il se retire du jeu. Dans ce cas, il donne le
nombre de points qu’il lui restait plutôt que la somme des dés joués.

Lorsqu’on recommence une ronde, tous les joueurs retrouvent 5 dés. Le gagnant de la
ronde précédente est celui qui commence la nouvelle ronde.

À la fin du nombre de rondes prévues, le joueur ayant le plus de points gagne. Si deux
joueurs ou plus sont à égalité avec le plus grand nombre de points (événement peu probable), ils sont tous déclarés gagnants.
        """)


if __name__ == '__main__':

    print("Jouons une partie de pyMafia!\n")
    # Afficher les instruction
    afficher_instructions()
    # Demander le nombre de joueurs voulu par l'utilisateur
    nombre_joueur = demander_nombre_joueurs()
    # Demander le nombre de joueurs humains
    nombre_joueur_humain = demander_nombre_joueurs_humains(nombre_joueur)
    # Création de l'objet partie avec le nombre de joueurs spécifiés
    partie = Partie(nombre_joueur, nombre_joueur_humain)
    # Démarrage de cette partie.
    partie.jouer()
    input('Appuyer sur ENTER pour quitter.')
