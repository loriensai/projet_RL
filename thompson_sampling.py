import numpy as np
import matplotlib.pyplot as plt


class ThompsonSampling : 

    def __init__(self, nb_themes, pourcentage_likes, nb_iterations, taux_exploration):
        self.nb_themes = nb_themes
        self.pourcentage_likes = pourcentage_likes
        self.nb_iterations = nb_iterations
        self.taux_exploration = taux_exploration
        self.rewards = [0]*nb_themes
        self.penalties = [0]*nb_themes
        self.themes_selectionnes = []
        self.test = False
 
    def selectionner_action(self):

        # Choisir une action exploitante ou exploratoire
        if np.random.rand() < self.taux_exploration:
            self.test = True
            # Action exploratoire : choisir aléatoirement une action
            return np.random.randint(self.nb_themes)
        else:
            self.test = False
            # Action exploitante : choisir l'action avec le taux de succès échantillonné le plus élevé
            samples = [np.random.beta(r+1,p+1) for r,p in zip(self.rewards, self.penalties)]
            return np.argmax(samples)
    
    def update(self, meilleure_action):

        # Exécuter l'action, observer la récompense et mettre à jour les distributions
        if np.random.uniform() < self.pourcentage_likes[meilleure_action] :
            self.rewards[meilleure_action] += 1 # like
        else : 
            self.penalties[meilleure_action] += 1 # dislike

    def appliquer(self):

        for _ in range(self.nb_iterations):

            # Sélectionner une action : recommander le post d'un thème
            meilleure_action = self.selectionner_action()
            self.themes_selectionnes.append(meilleure_action)

            # Exécuter l'action, observer la récompense et mettre à jour les distributions
            self.update(meilleure_action)
        
        print(f"Rewards par thème de posts : {self.rewards} \n")
        print(f"Penalités par thème de posts : {self.penalties} \n")
        print(f"Thèmes sélectionnés à chaque itération : {self.themes_selectionnes} \n")

        # Choix final de l'action 
        action_finale = self.selectionner_action()
        print("Action finale choisie :", action_finale)
        print(self.test)

if __name__=="__main__":
    # Paramètres 
    nb_themes = 4
    nb_iterations = 500
    pourcentage_likes = [0.1, 0.6, 0.2, 0.1]
    taux_exploration = 0.1

    for i in range(100):
        print(f"Essai {i} \n")
        ts = ThompsonSampling(nb_themes, pourcentage_likes, nb_iterations, taux_exploration)
        ts.appliquer()