"""
Module de la classe JoueurHumain
"""

from pymafia.joueur import Joueur


class JoueurHumain(Joueur):
    """
    Classe pour un joueur humain au jeu pymafia. Cette classe hérite de la classe Joueur.

    Cette classe n'a pas de méthode spécifique, mais servira à distinguer les joueurs humains des
    joueurs ordinateurs.
    """

    def __init__(self, identifiant):
        """
        Constructeur de la classe JoueurHumain
        Args:
            identifiant (int): Numéro d'identification du joueur
        """
        super().__init__(identifiant)

