"""
Module de la classe Dé
"""

import random


class Dé:
    """
    Classe pour un dé à joueur de 6 faces.

    Attributes:
        valeur (int): valeur actuelle du dé
    """

    def __init__(self, valeur=1):
        """
        Constructeur de la classe Dé
        Args:
            valeur (int, optional): valeur initiale du dé
        """
        self.valeur = valeur

    def rouler(self):
        """
        Méthode qui modifie la valeur actuelle du dé en choisissant aléatoirement une valeur entre 1 et 6.
        """
        self.valeur = random.randint(1, 6)

    def __str__(self):
        """
        Méthode qui retourne une représentation de l'objet en chaîne de caractères.
        Par exemple, si dé1 est un objet de la classe Dé, str(dé1) lancera un appel à cette fonction.
        Nous vous suggérons les caractères ⚀ ⚁ ⚂ ⚃ ⚄ ⚅ , dont les codes unicode sont 9856 à 9861 respectivement.
        On peut obtenir ces caractères avec la fonction chr(#valeur du code).
        Returns:
            str: Le caractère représentant l'objet
        """
        if self.valeur == 1:
            return str(chr(9856))
        elif self.valeur == 2:
            return str(chr(9857))
        elif self.valeur == 3:
            return str(chr(9858))
        elif self.valeur == 4:
            return str(chr(9859))
        elif self.valeur == 5:
            return str(chr(9860))
        elif self.valeur == 6:
            return str(chr(9861))

     # code de test unitaire
    def __repr__(self):
         return str(self)