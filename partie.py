"""
Module de la classe Partie
"""

from pymafia.joueur_humain import JoueurHumain
from pymafia.joueur_ordinateur import JoueurOrdinateur
from random import shuffle

# Variable globale spécifiant le nombre maximale de rondes d'une partie du jeu pymafia
RONDEMAX = 10


class Partie:
    """
    Documentation de la classe Partie
    Attributes:
        joueurs (list): Liste des joueurs au départ de la partie
        joueurs_actifs (list): Liste des joueurs qui ont encore des points (score supérieur à 0)
        premier_joueur (Joueur): Premier joueur de la ronde
        joueur_courant (Joueur): Joueur dont c'est le tour
        joueur_suivant (Joueur): Joueur dont ce sera le tour lorsque le joueur_courant aura joué (prochain joueur actif)
        ronde (int): Nombre de la ronde actuelle
        sens (int): Nombre qui indique le sens du tour (1, croissant; -1, décroissant)
        gagnant (Joueur): Joueur qui sera déclaré gagnant de la partie, initialisé à None
    """
    def __init__(self, nombre_joueurs, nombre_joueurs_humains):
        """
        Constructeur de la classe Partie
        Args:
            nombre_joueurs (int): Nombre de joueurs de la partie
            nombre_joueurs_humains (int): Nombre de joueurs humains de la partie
        """
        self.joueurs = Partie.creer_joueurs(nombre_joueurs, nombre_joueurs_humains)
        self.joueurs_actifs = self.joueurs.copy()
        self.premier_joueur = self.joueurs_actifs[0]
        self.joueur_courant = self.joueurs_actifs[0]
        self.joueur_suivant = self.joueurs_actifs[1]
        self.ronde = 1
        self.sens = 1
        self.gagnant = None

    @staticmethod
    def creer_joueurs(nombre_joueurs, nombre_joueurs_humains):
        """
        Méthode statique qui crée la liste de joueurs de la partie.
        Dans le cas où des joueurs ordinateurs sont permis, les joueurs humains et ordinateurs sont
        mélangés au hasard dans la liste de joueurs.
        Args:
            nombre_joueurs (int): Nombre de joueurs de la partie
            nombre_joueurs_humains (int): Nombre de joueurs humains de la partie

        Returns:
            list: Liste des joueurs
        """
        liste_des_joueurs = []
        total_cpu = nombre_joueurs - nombre_joueurs_humains
        if total_cpu <= 0:
            for i in range(1, nombre_joueurs + 1):
                liste_des_joueurs.append(JoueurHumain(i))
        else:
            for i in range(1, nombre_joueurs_humains + 1):
                liste_des_joueurs.append(JoueurHumain(i))
            for i in range(nombre_joueurs_humains + 1, nombre_joueurs + 1):
                liste_des_joueurs.append(JoueurOrdinateur(i))
            shuffle(liste_des_joueurs)
            identifiant = 0
            for player in liste_des_joueurs:
                identifiant += 1
                player.identifiant = identifiant
        return liste_des_joueurs

    def preparer_une_partie(self):
        """
        Méthode qui accomplit les actions nécessaires pour débuter une partie.
        """
        # Afficher les joueurs.
        Partie.afficher_joueurs(self)
        # Trouver le premier joueur.
        Partie.trouver_premier_joueur(self)
        # Déterminer le sens de la partie voulue par le premier joueur.
        Partie.determiner_sens(self)
        # Affecter à l'attribut du joueur_courant le premier joueur.
        self.joueur_courant = self.premier_joueur
        # Déterminer qui est le joueur suivant.
        Partie.determiner_joueur_suivant(self)
        # Réinitialiser les dés des joueurs pour que chaque joueur ait 5 dés.
        Partie.reinitialiser_dés_joueurs(self)

    def afficher_joueurs(self):
        """
        Méthode qui affiche quels joueurs sont humains et quels joueurs sont l'ordinateur.
        La version simple de cette méthode peut se limiter à lister les joueurs.
        Par exemple, "Le joueur 6 est prêt à jouer!"
        """
        # Lister l'identifiant des joueurs humains
        identifiants_joueurs_humains = []
        for joueur in self.joueurs:
            if isinstance(joueur, JoueurHumain):
                identifiants_joueurs_humains.append(str(joueur.identifiant))

        # Afficher les identifiants des joueurs humains (la chaîne est différente selon le nombre)
        if len(identifiants_joueurs_humains) == 1:
            print("Le joueur {} est le joueur humain.".format(identifiants_joueurs_humains[0]))
        elif len(identifiants_joueurs_humains) == len(self.joueurs):
            print('Tous les joueurs sont des joueurs humains!')
        elif len(identifiants_joueurs_humains) == 2:
            print("Les joueurs {} et {} sont des joueurs humains.".format(identifiants_joueurs_humains[0],
                                                                          identifiants_joueurs_humains[1]))
        else:
            liste_joueurs_humains = ", ".join(identifiants_joueurs_humains[:-1])
            print("Les joueurs {} et {} sont des joueurs humains.".format(liste_joueurs_humains,
                                                                          identifiants_joueurs_humains[-1]))
        # Si nécessaire, indiquer que l'autre joueur ou les autres joueurs sont des ordinateurs.
        nombre_joueurs_ordinateur = len(self.joueurs) - len(identifiants_joueurs_humains)
        if nombre_joueurs_ordinateur == 1:
            print("L'autre joueur est un ordinateur.\n")
        elif nombre_joueurs_ordinateur > 1:
            print("Les autres joueurs sont des ordinateurs.\n")

    def trouver_premier_joueur(self):
        """
        Méthode qui sert à déterminer qui sera le premier joueur de la première ronde. Ce joueur est celui qui obtient
        le plus haut score lorsque les joueurs lancent deux dés. En cas d'égalité, les joueurs à égalité relancent
        leurs dés jusqu'à ce qu'un seul joueurs aient le plus haut résultat.
        """
        list_comparaison = []
        print("Déterminons quel joueur débutera la partie!\n")
        for joueur in self.joueurs:
            input("Joueur " + str(joueur.identifiant) + " : Appuyer sur enter pour rouler les dés")
            joueur.rouler_dés()
            print("Joueur " + str(joueur.identifiant) + " : " + str(joueur) + " Total des dés: " +
                  str(joueur.calculer_points()) + "\n")
            list_comparaison.append(joueur.calculer_points())
        matrice_index_plus_haut = Partie.trouver_indices_max(list_comparaison)
        while len(matrice_index_plus_haut) > 1:
            print("Bris d'égalité!\n")
            joueur_restant = []
            for index in matrice_index_plus_haut:
                joueur_restant.append(self.joueurs_actifs[index])
            self.joueurs_actifs.clear()
            self.joueurs_actifs = joueur_restant.copy()
            list_comparaison = []
            for joueur in self.joueurs_actifs:
                input("Joueur " + str(joueur.identifiant) + " : Appuyer sur enter pour rouler les dés")
                joueur.rouler_dés()
                print("Joueur " + str(joueur.identifiant) + " : " + str(joueur) + " Total des dés: " +
                      str(joueur.calculer_points()) + "\n")
                list_comparaison.append(joueur.calculer_points())
            matrice_index_plus_haut = Partie.trouver_indices_max(list_comparaison)
        identifiant_premier = self.joueurs_actifs[matrice_index_plus_haut[0]].identifiant
        self.premier_joueur = self.joueurs[identifiant_premier - 1]
        self.joueurs_actifs = self.joueurs.copy()
        print("Le joueur " + str(self.premier_joueur.identifiant) + ": commencera la partie!" + "\n")

    def trouver_joueurs_au_plus_haut_total(self, liste_joueurs):
        """
        Cette méthode trouve le ou les joueurs ayant le plus haut score à leurs dés.
        Args:
            liste_joueurs (list): Liste des joueurs parmi lesquels il faut identifier ceux qui ont le plus score aux dés

        Returns:
            list: Liste des joueurs ayant eu le plus haut score. Cette liste contient plus qu'un joueur s'il y a eu
            égalité lors du lancer.
        """
        list_score_dé = []
        list_gagnant = []
        for joueur in liste_joueurs:
            list_score_dé.append(joueur.calculer_points())
        vecteur_index_valeur_plus = Partie.trouver_indices_max(list_score_dé)
        for index in vecteur_index_valeur_plus:
            list_gagnant.append(liste_joueurs[index])
        return list_gagnant

    @staticmethod
    def trouver_indices_max(vecteur):
        """
        Méthode statique qui trouve les index des nombres d'un vecteur d'entiers correspondants à la valeur maximale du
        vecteur.
        Args:
            vecteur (list): Vecteur de nombre d'entiers dont il faut trouver les index des maximum
        Returns:
            list: Liste des index des éléments du vecteur ayant la valeur la plus élevée
        """
        valeur_max = max(vecteur)
        index_avec_plus_haute_valeur = []
        for i, j in enumerate(vecteur):
            if j == valeur_max:
                index_avec_plus_haute_valeur.append(i)
        return index_avec_plus_haute_valeur

    def determiner_sens(self):
        """
        Méthode qui demande au premier joueur le sens dans lequel il souhaite bouger. Cette méthode vérifie si le
        premier joueur est un humain ou l'ordinateur. Dans le cas de l'humain, une demande est faite à la console.
        L'attribut sens de la partie est modifié selon la réponse. Dans le cas de l'ordinateur, on affiche son choix.
        """
        if isinstance(self.premier_joueur, JoueurHumain):
            self.sens = input("Joueur: " + str(self.premier_joueur.identifiant) +
                              " Dans quel sens voulez vous que la partie tourne? (1 pour un ordre croissant, "
                              "-1 pour un ordre décroissant)\n")
            verification = self.sens
            verification.lstrip("-")
            while not (verification.isnumeric() and int(verification) == 1):
                self.sens = input("Erreur, veuillez entrez 1 (ordre croissant) ou -1 (ordre décroissant) seulement.\n")
                verification = self.sens.lstrip("-")
            self.sens = int(self.sens)
        else:
            sens = self.premier_joueur.demander_sens()
            print(sens)
            self.sens = sens[0]

    def determiner_joueur_suivant(self):
        """
        Méthode qui trouve qui est le joueur suivant et qui modifie l'attribut joueur_suivant de la partie.
        """
        plus_gros_index = len(self.joueurs_actifs) - 1
        if plus_gros_index > 0:
            index_joueur_courant = self.joueurs_actifs.index(self.joueur_courant)
            if self.sens == 1:
                if index_joueur_courant < plus_gros_index:
                    i = 1
                elif index_joueur_courant == plus_gros_index:
                    i = -plus_gros_index
            elif self.sens == -1:
                if index_joueur_courant > 0:
                    i = -1
                else:
                    i = plus_gros_index
            self.joueur_suivant = self.joueurs_actifs[index_joueur_courant + i]

    def reinitialiser_dés_joueurs(self):
        """
        Méthode qui réinitialise les dés des joueurs actifs en leur donnant 5 dés chacun.
        """
        for joueur in self.joueurs:
            joueur.reinitialiser_dés()

    def jouer_une_partie(self):
        """
        Méthode qui accomplit les actions pour jouer une partie de pymafia.
        """
        # Cette méthode contient une grande boucle qui vérifie que le numéro de la ronde actuelle est inférieure ou
        # égale au nombre maximal de ronde. Chacune des itérations de la boucle permet de jouer une ronde.
        # Les étapes pour une ronde sont:
        # 1. Jouer une ronde.
        global RONDEMAX
        while RONDEMAX >= self.ronde:
            Partie.jouer_une_ronde(self)
            # 2. Terminer la ronde
            Partie.terminer_ronde(self)
            # 3. Afficher un message donnant les points en fin de ronde.
            print(Partie.message_points_des_joueurs(self))
            # 4. Réinitialiser les dés des joueurs.
            Partie.reinitialiser_dés_joueurs(self)
            # 5. Passer à la prochaine ronde.
            if len(self.joueurs_actifs) > 1:
                Partie.passer_a_la_ronde_suivante(self)
            else:
                self.ronde = 100

    def jouer_une_ronde(self):
        """
        Méthode qui permet de jouer une ronde. Un message de début de ronde est affiché. Ensuite faire une boucle pour
        jouer une succession de tour. On sort de la boucle lorsqu'un joueur gagne le tour.
        """
        print("début de ronde: " + str(self.ronde) + "\n")
        while not Partie.verifier_si_fin_de_ronde(self):
            Partie.jouer_un_tour(self)

    def jouer_un_tour(self):
        """
        Méthode qui permet à un joueur de jouer un tour:
        Returns:
            Joueur: Le joueur gagnant, si le joueur courant gagne le tour, None autrement.
        """
        # Les étapes pour jouer un tour sont:
        # 1) Le joueur courant roule ses dés.
        print("C'est a votre tour joueur ", self.joueur_courant.identifiant)
        input("Appuyer sur une touche pour rouler les dés")
        self.joueur_courant.rouler_dés()
        # 2) Le résultat du lancer est affiché.
        print("Joueur ", str(self.joueur_courant.identifiant), ": ", self.joueur_courant, " Total des dés: ",
              self.joueur_courant.calculer_points())
        # 3) On gère les dés de valeur 1 et 6.
        Partie.gerer_dés_1_et_6(self)
        # 4) On vérifie si le joueur courant a gagné la ronde en n'ayant plus de dé. S'il gagne, on affiche un message
        # qui indique qu'il n'a plus de dé. Sinon, on passe au joueur suivant.
        # qui indique qu'il n'a plus de dé. Sinon, on passe au joueur suivant.
        if Partie.verifier_si_fin_de_ronde(self):
            print("Félicitation joueur", self.joueur_courant.identifiant, " vous avez plus aucun dés!")
            return self.joueur_courant
        else:
            Partie.passer_au_prochain_joueur(self)
            return None

    def gerer_dés_1_et_6(self):
        """
        Méthode qui gère le contenu des dés du joueur courant suite à un lancer pour traiter la présence de 1 et de 6
        selon les étapes suivantes:
        """
        # Les étapes de cette méthode sont:
        # 1. Vérifier si les dés du joueur courant contiennent des 1 et des 6 et obtenir le nombre de 1 et de 6.
        resultat_1_6 = Partie.verifier_dés_joueur_courant_pour_1_et_6(self)
        # 2. Afficher les messages pour ces dés.
        Partie.afficher_messages_dés_1_et_6(self, resultat_1_6[0], resultat_1_6[1])
        # 3. Déplacer les dés 1 et 6.
        Partie.deplacer_les_dés_1_et_6(self, resultat_1_6[0], resultat_1_6[1])

    def verifier_dés_joueur_courant_pour_1_et_6(self):
        """
        Méthode qui vérifie le nombre de dés de valeur 1 et 6 du joueur courant.
        Returns:
            int, int: nombre de dés de valeur 1 et 6
        """
        return self.joueur_courant.compter_1_et_6()

    def afficher_messages_dés_1_et_6(self, nombre_1, nombre_6):
        """
        Méthode qui affiche les messages de la présence de dés de valeur 1 et de dés de valeur 6 dans les dés du joueur
        courant. On affiche les messages que si le joueur a un dé de la valeur désignée.
        Args:
            nombre_1 (int): Nombre de dé(s) de valeur 1
            nombre_6 (int): Nombre de dé(s) de valeur 6
        """
        if nombre_1:
            print(self.message_pour_dé_1(nombre_1))
        if nombre_6:
            print(self.message_pour_dé_6(nombre_6))
        if nombre_1 or nombre_6:
            print()  # Affiche un ligne vide si le joueur a des 1 ou des 6

    def message_pour_dé_1(self, nombre_1):
        """
        Méthode qui retourne le message sur le nombre de dé(s) de valeur 1. Par exemple, "Le joueur 2 a roulé 2 dés de
        valeur 1 et les retire du jeu."
        Args:
            nombre_1 (int): Nombre de dé(s) de valeur 1
        Returns:
            str: Message contenant le nombre de dé(s) retiré
        """
        return 'Le joueur {} a roulé {} dé{} de valeur 1 et le{} retire du jeu.'.format(
                self.joueur_courant.identifiant, nombre_1, 's' if nombre_1 > 1 else '', 's' if nombre_1 > 1 else '')

    def message_pour_dé_6(self, nombre_6):
        """
        Méthode qui retourne le message sur le nombre de dé(s) de valeur 6. Par exemple, "Le joueur 4 a roulé 1 dé de
        valeur 6 et le passe au joueur suivant."
        Args:
            nombre_6 (int): Nombre de dé(s) de valeur 6
        Returns:
            str: Message contenant le nombre de dé(s) passé au suivant
        """
        return 'Le joueur {} a roulé {} dé{} de valeur 6 et le{} passe au joueur suivant.'.format(
                self.joueur_courant.identifiant, nombre_6, 's' if nombre_6 > 1 else '', 's' if nombre_6 > 1 else '')

    def deplacer_les_dés_1_et_6(self, nombre_1, nombre_6):
        """
        Méthode qui déplace les dés de valeur 1 et de valeur 6 roulés par le joueur courant. Les dés de valeur 1 sont
        retirés du jeu (penser à une méthode de la classe joueur). Les dés de valeur 6 sont passés au joueur suivant.
        Args:
            nombre_1 (int): Nombre de dé(s) de valeur 1
            nombre_6 (int): Nombre de dé(s) de valeur 6
        """
        self.joueur_courant.retirer_dé(1)
        if nombre_6 > 0:
            for i in range(0, nombre_6):
                Partie.passer_dé_joueur_suivant(self)

    def passer_dé_joueur_suivant(self):
        """
        Méthode qui passe un dé en ajoutant un dé au joueur suivant et en retirant un dé de valeur 6 du joueur courant.
        """
        self.joueur_courant.retirer_dé(6)
        self.joueur_suivant.ajouter_un_dé()

    def verifier_si_fin_de_ronde(self):
        """
        Méthode qui vérifie si le joueur courant n'a plus de dé. Ceci signifie la fin de la ronde.
        Returns:
            bool: True, si le joueur courant n'a plus de dé. False autrement.
        """
        if not self.joueur_courant.dés:
            return True
        return False

    def passer_au_prochain_joueur(self):
        """
        Méthode qui change la valeur de l'attribut du joueur_courant et qui détermine le joueur suivant.
        """
        if self.joueur_suivant.score > 0:
            self.joueur_courant = self.joueur_suivant
            Partie.determiner_joueur_suivant(self)

    def passer_a_la_ronde_suivante(self):
        """
        Méthode qui incrémente le numéro de la ronde.
        """
        self.ronde += 1

    def terminer_ronde(self):
        """
        Méthode qui accomplit les actions de jeu en fin de ronde à l'aide d'autres méthodes de la classe.
        """
        # 1. Tous les joueurs qui n'ont pas gagné la ronde jouent les dés qui leur restent.
        Partie.jouer_dés_en_fin_de_ronde(self)
        # 2. Afficher les messages des points donnés par les joueurs.
        Partie.messages_pour_points_fin_de_ronde(self)
        # 3. Ajuster les points de perdants de la ronde et compter la somme des points destinés au gagnant.
        point_gagnant = Partie.ajuster_points_des_perdants_en_fin_de_ronde(self)
        # 4. Ajuster les points du gagnant avec les points des perdants.
        Partie.ajuster_points_du_gagnant(self, point_gagnant)
        # 5. Afficher le message qui annonce le nouveau score du gagnant.
        Partie.message_pour_points_du_gagnant(self, point_gagnant)
        Partie.reinitialiser_dés_joueurs(self)
        Partie.retirer_joueurs_sans_points(self)

    def jouer_dés_en_fin_de_ronde(self):
        """
        Méthode qui fait rouler les dés des joueurs qui sont encore actifs (sauf le gagnant)
        """
        self.gagnant = self.joueur_courant
        for joueur in self.joueurs_actifs:
            if joueur != self.gagnant:
                joueur.rouler_dés()

    def messages_pour_points_fin_de_ronde(self):
        """
        Méthode qui assemble le message qui informe de la quantité de points donnés par chacun des joueurs qui ont perdu
        la ronde. Si la somme des dés donne un nombre de points inférieurs au score actuel du joueur, le nombre de
        points donnés correspond au résultat du lancer. Sinon, le nombre des points donnés correspond au score du
        joueur. Dans le premier cas, le message pourrait être : "Le joueur 2 joue les dés suivants: ⚅ ⚁ . Il donne 8
        points au gagnant de la ronde." Dans le deuxième cas, le message pourrait être: "Le joueur 5 joue les dés
        suivants: ⚅ ⚃ . La somme des dés est égale ou supérieure à son nombre de points. Il donne 7 points au gagnant
        de la ronde et se retire de la partie.
        Returns:
            str: Le message qui indique le nombre de points par chaque joueur perdant de la ronde.
        """
        for joueur in self.joueurs_actifs:
            if joueur != self.gagnant:
                if joueur.score > joueur.calculer_points():
                    print("Le joueur " + str(joueur.identifiant) + " joue les dés suivants: " + str(joueur) +
                          ". Il donne " + str(joueur.calculer_points()) + " points au gagnant de la ronde.")
                else:
                    print("Le joueur " + str(joueur.identifiant) + " joue les dés suivants: " + str(joueur) +
                          ". La somme des dés est égale ou supérieure à son nombre de points. Il donne " + str(
                        joueur.score) + " points au gagnant de la ronde et se retire de la partie.")

    def ajuster_points_des_perdants_en_fin_de_ronde(self):
        """
        Méthode qui ajuste les points des perdants en fin de ronde. (en utilisant la méthode appropriée de la classe
        joueur). La méthode fait aussi la somme des points ainsi retirés à ces joueurs.
        Returns:
            int: Somme des points retirés aux joueurs.
        """
        point_gagnant = 0
        for joueur in self.joueurs_actifs:
            point = joueur.calculer_points()
            if point <= joueur.score:
                joueur.ajuster_score_en_fin_de_tour()
                point_gagnant += point
            else:
                point_gagnant += joueur.score
                joueur.ajuster_score_en_fin_de_tour()
        return point_gagnant

    def ajuster_points_du_gagnant(self, score):
        """
        Méthode qui ajuste le score du gagnant de la ronde (le joueur courant).
        Args:
            score (int): Le nombre de points à ajouter au score du joueur courant.
        """
        self.joueur_courant.score += score

    def message_pour_points_du_gagnant(self, points_au_gagnant):
        """
        Méthode qui retourne un message annonçant le nombre de points donnés au gagnant. Par exemple: "Le joueur 3
        obtient 18 points.
        Args:
            points_au_gagnant (int): Nombre de points donnés au gagnant.
        Returns:
            str: Chaîne de caractères contenant le message.
        """
        return "Le joueur " + str(self.gagnant.identifiant) + " obtient " + str(points_au_gagnant) + " points!"

    def retirer_joueurs_sans_points(self):
        """
        Méthode qui vérifie si des joueurs actifs ont maintenant un score de 0. Seuls les joueurs ayant un score plus
        grand que zéro demeurent actifs. Advenant que le joueur suivant ne soit plus actif, le prochain joueur actif
        devient le nouveau joueur suivant.

        returns: (list): list des joueur qui n'ont plus de points.
        """
        list_joueur_enlever = []
        list_joueur_fin_ronde = self.joueurs_actifs.copy()
        self.joueurs_actifs.clear()
        for joueur in list_joueur_fin_ronde:
            if joueur.score > 0:
                self.joueurs_actifs.append(joueur)
            else:
                list_joueur_enlever.append(joueur)
        Partie.determiner_joueur_suivant(self)
        return list_joueur_enlever

    def terminer_une_partie(self):
        """
        Méthode qui fait les affichages de fin de partie en déterminant le gagnant.
        """
        # On informe les joueurs que le nombre maximal de rondes est atteint.
        print("le nombre de ronde maximal a été atteinte... voyons voir qui est l'heureux gagnant...")
        # Ensuite, on affiche le bilan des points des joueurs de la partie.
        print(Partie.message_points_en_fin_de_partie(self))
        # On détermine le gagnant et on en informe les utilisateurs
        list_gagnant = Partie.determiner_liste_gagnants(self)
        print(Partie.message_gagnants(self, list_gagnant))
        print("Merci d'avoir joué à pymafia!")

    def message_points_en_fin_de_partie(self):
        """
        Méthode qui assemble un message sur les points des joueurs en fin de partie. Par exemple, "À la fin de la partie
        ronde, les joueurs ont les points suivants: Le joueur 1 a 16 points. ..." Et ainsi de suite pour tous les
        joueurs.
        Returns:
            str: Le message qui donne les points en fin de partie.
        """
        message = "À la fin de la partie, les joueurs ont les points suivants:\n"
        message += self.message_points_des_joueurs()
        return message

    def message_points_des_joueurs(self):
        """
        Méthode qui assemble un message indiquant les points de tous les joueurs. Par exemple, "Le joueur 1 a 16
        points. ..." Et ainsi de suite pour tous les joueurs.
        Returns:
            str: Les message donnant les points des joueurs.
        """
        message = ""
        for joueur in self.joueurs:
            message += "Le joueur {} a {} point{}.\n".format(
                joueur.identifiant, joueur.score, 's' if joueur.score > 0 else '')
        return message

    def determiner_liste_gagnants(self):
        """
        Méthode qui détermine l'index des joueurs ayant le score le plus élevé.
        Returns:
            list: Liste contenant les indices des joueurs ayant le plus haut score. Il y a plus d'un joueur dans cette
            liste seulement s'il y a égalité.
        """
        liste_points_joueurs = []
        for joueur in self.joueurs:
            liste_points_joueurs.append(joueur.score)
        return Partie.trouver_indices_max(liste_points_joueurs)

    def message_gagnants(self, liste_index_gagnants):
        """
        Méthode qui assemble le message annonçant le gagnant (ou les gagnant en cas d'égalité). Par exemple, "Le joueur
        3 a gagné la partie!"
        Args:
            liste_index_gagnants (list): Liste contenant l'index (qui est l'identifiant) du ou des joueurs gagnants
        Returns:
            str: Message annonçant le gagnant.
        """
        if len(liste_index_gagnants) == 1:
            message = "Le joueur {} a gagné à la partie!\n".format(self.joueurs[liste_index_gagnants[0]].identifiant)
        else:
            message = "Il y a égalité entre les joueurs {}.\n".format(" et ").join(
                str(self.joueurs[gagnant].identifiant) for gagnant in liste_index_gagnants)
        return message

    def jouer(self):
        """
        Méthode principale de la classe qui spécifie le déroulement d'une partie.
        """
        # Les étapes sont:
        # 1) préparer une partie;
        Partie.preparer_une_partie(self)
        # 2) jouer une partie et
        Partie.jouer_une_partie(self)
        # 3) terminer une partie.
        Partie.terminer_une_partie(self)


