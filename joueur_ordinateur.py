"""
Module de la classe JoueurOrdinateur
"""

from pymafia.joueur import Joueur
from random import randrange


class JoueurOrdinateur(Joueur):
    """
    Classe pour un joueur ordinateur au jeu pymafia. Cette classe hérite de la classe Joueur.
    """
    def __init__(self, identifiant):
        """
        Constructeur de la classe JoueurOrdinateur
        Args:
            identifiant (int): Numéro d'identification du joueur
        """
        super().__init__(identifiant)

    def demander_sens(self):
        """
        Méthode qui fait un choix aléatoire pour le sens du jeu (ordre croissant ou décroissant).
        Returns:
            tuple: contenant un entier (1 pour la gauche (croissant) ou -1 pour la droite (décroissant))
            et un string (message qui indique le choix du joueur ordinateur,
            par exemple: Le joueur X choisit de jouer vers la gauche (en ordre croissant)).
        """
        orientation = randrange(-1, 2, 2)
        if orientation == 1:
            message = ("Le joueur " + str(self.identifiant)
                       + " à choisit de jouer vers la gauche (en ordre croissant)")
        else:
            message = str("Le joueur " + str(self.identifiant)
                       + " à choisit de jouer vers la droite (en ordre décroissant).")
        return (orientation, message)

