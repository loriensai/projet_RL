from interface import InterfaceGraphique
from load_images import load_images


if __name__ == "__main__":
    # Télécharger les images via les profils Instagram
    # load_images(["les_animaux_droles", "incroyable_nourriture", "franceolympique", "yvesrocherfr"])

    # Paramètres de l'interface
    folder_paths = ['franceolympique_images', 'incroyable_nourriture_images',
                    'les_animaux_droles_images', 'yvesrocherfr_images']
    nb_iterations = 500
    taux_exploration = 0.1

    # Lancer l'application
    app = InterfaceGraphique(folder_paths, nb_iterations, taux_exploration)
    app.mainloop()
