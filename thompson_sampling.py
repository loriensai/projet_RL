import numpy as np
import matplotlib.pyplot as plt


class ThompsonSampling:
    """ Algorithme du Thompson Sampling """

    def __init__(self, pourcentage_likes, nb_iterations, taux_exploration):

        # Informations issues du pourcentage de likes de chaque thème
        self.dict_likes = pourcentage_likes
        self.pourcentage_likes = list(pourcentage_likes.values())
        self.nb_themes = len(pourcentage_likes)

        # Paramètres spécifiques au Thompson Sampling
        self.nb_iterations = nb_iterations
        self.taux_exploration = taux_exploration  # Contrôle la probabilité d'explorer

        # Initialisation d'autres paramètres
        self.rewards = [0]*self.nb_themes
        self.penalties = [0]*self.nb_themes
        # Utile pour afficher des informations supplémentaires dans test.py
        self.themes_selectionnes = []
        self.exploration = False

    def selectionner_action(self) -> int:
        """ Choisir une action à exécuter, soit exploitante soit exploratoire.

        Returns:
            int: action à exécuter.
        """

        if np.random.rand() < self.taux_exploration:
            # Action exploratoire : choisir aléatoirement une action
            self.exploration = True
            return np.random.randint(self.nb_themes)
        else:
            # Action exploitante : choisir l'action avec le taux de succès échantillonné le plus élevé
            self.exploration = False
            samples = [np.random.beta(r+1, p+1)
                       for r, p in zip(self.rewards, self.penalties)]
            return np.argmax(samples)

    def update(self, meilleure_action: int):
        """ Mettre à jour les récompenses suite aux résultats de l'action exécutée.

        Args:
            meilleure_action (int): action exécutée. 
        """

        if np.random.uniform() < self.pourcentage_likes[meilleure_action]:
            self.rewards[meilleure_action] += 1  # like
        else:
            self.penalties[meilleure_action] += 1  # dislike

    def appliquer(self, infos_supplementaires: bool = False):
        """ Exécution de l'algorithme Thompson Sampling. 

        Args:
            infos_supplementaires (bool, optional): True si on souhaite avoir davantage d'informations. Valeur par défaut False.

        Returns: 
            Union[str, dict]: Si `infos_supplementaires` est False, retourne le nom du thème choisi pour la prochaine action.
                              Sinon, retourne un dictionnaire contenant des informations sur l'exécution de l'algorithme.
        """

        # Itérer sur chaque itération
        for _ in range(self.nb_iterations):

            # Sélectionner une action : recommander le post d'un thème
            meilleure_action = self.selectionner_action()
            self.themes_selectionnes.append(meilleure_action)

            # Exécuter l'action, observer la récompense et mettre à jour les distributions
            self.update(meilleure_action)

        # Choix final de l'action
        action_finale = self.selectionner_action()

        if infos_supplementaires:
            return {"Rewards par thème de posts": self.rewards,
                    "Penalités par thème de posts": self.penalties,
                    "Thèmes sélectionnés à chaque itération": self.themes_selectionnes,
                    "Action finale choisie": [action_finale, list(self.dict_likes.keys())[action_finale]],
                    "Exploration": self.exploration}
        else:
            return list(self.dict_likes.keys())[action_finale]
