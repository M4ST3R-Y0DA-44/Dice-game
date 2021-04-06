"""
Module de la classe Joueur
"""

from pymafia.de import Dé


class Joueur:
    """
    Classe pour un joueur du jeu pymafia

    Attributes:
        identifiant (int): Numéro d'identification du joueur
        dés (liste): liste contenant les dés du joueur
        score (int): nombre de points du joueur
    """

    def __init__(self, identifiant, dés=[Dé(), Dé()], score=100):
        """
        Constructeur de la classe Joueur.
        Note: Lorsqu'un joueur est créé en début de partie, on lui donne deux dés.
        Args:
            identifiant (int): Identifiant du joueur à être instancié
        """
        self.identifiant = identifiant
        self.dés = dés
        self.score = score

    def rouler_dés(self):
        """
        Méthode qui modifie aléatoirement la valeur de tous les dés du joueur.
        """
        for chaque_dé in self.dés:
            chaque_dé.rouler()

    def compter_1_et_6(self):
        """
        Méthode qui fait le décompte des dés du joueur qui ont la valeur 1 et la valeur 6.
        Returns:
            nombre_1 (int): Nombre de dés du joueur ayant la valeur 1
            nombre_6 (int): Nombre de dés du joueur ayant la valeur 6
        """
        nombre_1 = 0
        nombre_6 = 0
        for chaque_dé in self.dés:
            if chaque_dé.valeur == 1:
                nombre_1 += 1
            elif chaque_dé.valeur == 6:
                nombre_6 += 1
        return nombre_1, nombre_6

    def retirer_dé(self, valeur):
        """
        Méthode qui retire tous les dés du joueur ayant une certaine valeur.
        Args:
            valeur (int): Nombre entre 1 et 6 du ou des dés à retirer
        """
        copie_self_list = self.dés.copy()
        self.dés.clear()
        for chaque_dé in copie_self_list:
            if chaque_dé.valeur != valeur:
                self.dés.append(chaque_dé)

    def retirer_dés(self):
        """
        Méthode qui retire tous les dés du joueurs
        """
        self.dés.clear()

    def ajouter_un_dé(self):
        """
        Méthode qui ajoute un dé de valeur 6 aux dés du joueur
        """
        self.dés.append(Dé(6))

    def reinitialiser_dés(self):
        """
        Méthode qui réinitialise les dés du joueur en lui remettant 5 dés en main.
        """
        self.dés = [Dé(), Dé(), Dé(), Dé(), Dé()]

    def calculer_points(self):
        """
        Méthode qui calcule le total de la valeur des dés du joueur.
        Returns:
            int: Total de la valeur des dés
        """
        total_valeur_dé = 0
        for element in self.dés:
            total_valeur_dé += element.valeur
        return total_valeur_dé

    def ajuster_score_en_fin_de_tour(self):
        """
        Méthode qui modifie le score du joueur selon la valeurs des dés du joueur.
        Si la valeur des dés est inférieure ou égale au score actuel du joueur, le score du joueur est
        réduit de cette valeur, qui est aussi retournée. Autrement, le score est mis à 0 et la valeur du
        score qui restait est retournée.
        Returns:
            int: Nombre de points perdus par le joueur en fin de tour et donnés au gagnant.
        """
        if Joueur.calculer_points(self) <= self.score:
            self.score -= Joueur.calculer_points(self)
            return Joueur.calculer_points(self)
        else:
            nombre_point_donner_gagnant = self.score
            self.score = 0
            return nombre_point_donner_gagnant

    def __eq__(self, other):
        """
        Méthode qui définit l'opérateur == pour la classe joueur
        Args:
            other (Joueur): autre objet joueur pour la comparaison
        Returns:
            bool: True si c'est le même joueur, False autrement
        """
        if not isinstance(other, type(self)):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Méthode qui définit l'opérateur != pour la classe joueur
        Args:
            other (Joueur): autre objet joueur pour la comparaison
        Returns:
            bool: True si ce n'est pas le même joueur, False autrement
        """
        return not self == other

    def __len__(self):
        """
        Méthode qui retourne le nombre de dés du joueur.
        Returns:
            int: Nombre de dés du joueur
        """
        return len(self.dés)

    def __str__(self):
        """
        Méthode qui retourne une chaîne de caractères représentant les dés du joueur. Celle-ci prend la forme d'une
        chaîne composée des dés. Par exemple, '⚀ ⚃ ⚃'.
        Returns:
            str: Représentation des dés du joueur.
        """
        return ' '.join(str(d) for d in self.dés)

    ## code de test unitaire
    def __repr__(self):
        return str(self)