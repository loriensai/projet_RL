from instaloader import Instaloader, Profile
import random
import os


def load_images(profiles=["les_animaux_droles", "incroyable_nourriture", "franceolympique", "yvesrocherfr"]):
    """ Télécharger des images à partir d'une liste de profils Instagram.

    Args:
        profiles (list, optional): liste des profils. Valeur par défaut ["les_animaux_droles", "incroyable_nourriture", "franceolympique", "yvesrocherfr"].
    """

    # Initialiser Instaloader
    L = Instaloader()

    # Parcourir les profils
    for profile in profiles:

        # Créer un répertoire pour stocker les images téléchargées
        download_dir = f"{profile}_images"
        os.makedirs(download_dir, exist_ok=True)

        # Récupérer le profil Instagram
        profile = Profile.from_username(L.context, profile)

        # Récupérer les publications associées au profil
        posts = profile.get_posts()

        # Tirer aléatoirement 10 publications
        random_posts = random.sample(list(posts), 10)

        # Télécharger les images
        for post in random_posts:
            try:
                L.download_post(post, download_dir)
                print("Image téléchargée avec succès.")
            except Exception as e:
                print(f"Erreur lors du téléchargement de l'image : {e}")
