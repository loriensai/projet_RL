import os
import random


def get_random_images(folder_path: str, num_images: int = 5) -> list:
    """ Sélectionner aléatoirement des images dans un dossier.

    Args:
        folder_path (str): chemin du dossier.
        num_images (int, optional): nombre d'images à sélectionner. Valeur par défaut 5.

    Returns:
        list: liste des images sélectionnées.
    """

    # Initialisation
    random_images = []

    # Parcourir les fichiers dans le dossier
    files = os.listdir(folder_path)
    # Récupérer uniquement les fichiers JPG
    jpg_files = [f for f in files if f.lower().endswith('.jpg')]
    # Sélectionner num_images fichiers aléatoires
    random_files = random.sample(jpg_files, min(num_images, len(jpg_files)))

    # Ajouter les fichiers sélectionnés à la liste sous la forme "dossier/nom_fichier.jpg"
    for file_name in random_files:
        random_images.append(os.path.join(folder_path, file_name))

    return random_images


def create_images_recommendation_dict(folder_paths: list):
    """ Créer deux dictionnaires contenant respectivement les images à afficher à l'utilisateur et les images à recommander pour chaque thème. 

    Args:
        folder_paths (list): liste des dossiers / thèmes.

    Returns:
        images_dict : {dossier/thème : liste des images à afficher avant la recommandation}. 
        recommendation_dict : {dossier/thème : chemin de l'image à recommander}.
    """

    # Initialisation
    images_dict = {}
    recommendation_dict = {}

    # Parcourir les dossiers
    for folder_path in folder_paths:

        # Récupérer le nom du dossier uniquement en cas de chemin absolu
        folder_name = os.path.basename(folder_path)

        # Récupérer 5 images aléatoires dans le dossier
        images = get_random_images(folder_path)

        # Stocker une image parmi les 5 à recommander
        index = random.randint(0, len(images) - 1)
        recommendation_dict[folder_name] = images.pop(index)

        # Stocker les autres images
        images_dict[folder_name] = images

    return images_dict, recommendation_dict
