from thompson_sampling import ThompsonSampling

def test():
    """ Fontion permettant de tester l'aspect exploration/exploitation du Thompson Sampling. """

    # Paramètres
    pourcentage_likes = {'franceolympique_images' : 0.25,
                         'incroyable_nourriture_images' : 0.5,
                         'les_animaux_droles_images' : 0.0, 
                         'yvesrocherfr_images' : 0.25}
    nb_iterations = 500
    taux_exploration = 0.1
    
    # Lancement du Thompson Sampling 50 fois 
    for i in range(100):
        ts = ThompsonSampling(pourcentage_likes, nb_iterations, taux_exploration)
        res = ts.appliquer(infos_supplementaires=True)
        print(f"Essai {i} \n")
        print(res, "\n")

if __name__ == "__main__":
    test()