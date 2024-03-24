import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import random
from get_images import create_images_recommendation_dict
from thompson_sampling import ThompsonSampling


class InterfaceGraphique(tk.Tk):
    """ Interface graphique de l'application de recommandations de posts Instagram """

    def __init__(self, folder_paths, nb_iterations, taux_exploration):
        super().__init__()

        # Paramètres pour le Thompson Sampling
        self.nb_iterations = nb_iterations
        self.taux_exploration = taux_exploration

        # Titre de l'application
        self.title("Recommandation de Posts Instagram")

        # Récupérer les images à afficher et à recommander pour chaque thème
        self.folder_paths = folder_paths
        self.images_dict, self.recommendation_dict = create_images_recommendation_dict(
            self.folder_paths)

        # Initialiser le suivi des ressentis pour chaque post
        self.likes = {key: False for images in self.images_dict.values()
                      for key in images}

        # Initialiser l'index de la page courante
        self.current_page_index = -1

        # Initialiser les pages pour la collecte des ressentis de l'utilisateur pour les posts proposés
        self.pages = self.create_image_pages()

        # Créer une page d'accueil
        self.create_homepage()

    def create_homepage(self):
        """ Page d'accueil """

        # Créer un cadre pour la page d'accueil
        self.home_frame = ttk.Frame(self)
        self.home_frame.pack(padx=20, pady=20)

        # Ajouter le nom de l'application
        label_title = ttk.Label(
            self.home_frame, text="Bienvenue dans notre application de recommandation de posts Instagram! \n Par DAVID-QUILLOT Mathis, LE GROGNEC Lenaig et NOUZILLE Lorie")
        label_title.pack(pady=10)

        # Ajouter un bouton "Commencer"
        start_button = ttk.Button(
            self.home_frame, text="Commencer", command=self.start_and_destroy_homepage)
        start_button.pack()

    def start_and_destroy_homepage(self):
        """ Détruire la page d'accueil suite à un clic sur le bouton 'Commencer' et lancer la collecte des ressentis de l'utilisateur pour la recommandation. """

        self.home_frame.destroy()
        self.show_next_page()

    def create_image_pages(self) -> list:
        """ Créer des lots d'images à afficher sur chaque page pour la collecte des ressentis. 

        Returns:
            list: liste des images à afficher à chaque page.
        """

        # Récupérer toutes les images
        all_images = [image for images in self.images_dict.values()
                      for image in images]

        # Les mélanger
        random.shuffle(all_images)

        # Créer des lots de 4 pour afficher 4 images par page
        return [all_images[i:i+4] for i in range(0, len(all_images), 4)]

    def show_next_page(self):
        """ Gérer l'enchaînement des pages à afficher : 
            - Soit une page contenant des images pour collecter les "J'aime"/"Je n'aime pas" des images de l'utilisateur.
            - Soit la page de la recommandation faite pour l'utilisateur suite à ses réponses. 
        """

        # Toutes les images n'ont pas encore été montrées à l'utilisateur : collecte des likes non terminée
        if self.current_page_index < len(self.pages) - 1:
            self.current_page_index += 1
            self.show_page(self.current_page_index)
        # Collecte terminée, on passe à la recommandation
        else:
            self.show_recommandation_page()

    def show_page(self, page_index: int):
        """ Affichage d'une page contenant 4 images pour collecter le ressenti de l'utilisateur sur ces images. 

        Args:
            page_index (int): numéro de la page à afficher.
        """
        # Détruire le cadre de la page précédente s'il existe
        if hasattr(self, 'recommendation_frame'):
            self.recommendation_frame.destroy()
        # Créer un nouveau cadre
        self.recommendation_frame = ttk.Frame(self)
        self.recommendation_frame.pack(padx=20, pady=20)

        # Parcourir les images de la page actuelle
        for i, image_path in enumerate(self.pages[page_index]):

            # Créer un cadre pour chaque image
            frame = ttk.Frame(self.recommendation_frame)
            frame.grid(row=0, column=i, padx=10, pady=10)

            # Charger l'image et la redimensionner
            image = Image.open(image_path)
            image = image.resize((400, 400))
            photo = ImageTk.PhotoImage(image)

            # Afficher l'image
            label_image = tk.Label(frame, image=photo)
            label_image.image = photo
            label_image.pack()

            # Ajouter un bouton "Je n'aime pas" sous chaque image
            like_button = ttk.Button(
                frame, text="Je n'aime pas", command=lambda idx=i: self.like_post(idx))
            like_button.pack(pady=5)
            # Initialiser l'état du bouton pour savoir s'il est en position "Je n'aime pas" ou "J'aime"
            like_button.state = tk.BooleanVar(value=False)

        # Ajouter un bouton "Suivant" pour passer à la prochaine page
        next_button = ttk.Button(
            self.recommendation_frame, text="Suivant", command=self.show_next_page)
        next_button.grid(row=1, columnspan=len(
            self.pages[page_index]), pady=10)

    def like_post(self, idx: int):
        """ Modification de l'état du bouton suite à un click sur le bouton "J'aime"/"Je n'aime pas"
        et mise à jour de la variable self.likes qui stocke toutes les informations sur les actions de 
        l'utilisateur au fur et à mesure.

        Args:
            idx (int): index de l'image pour laquelle l'utilisateur indique son ressenti.
        """

        # Obtenir l'état actuel du bouton (True si "J'aime", False si "Je n'aime pas")
        button_state = self.recommendation_frame.winfo_children()[
            idx].children['!button'].state.get()

        # Changer le texte du bouton en fonction de son état actuel
        if button_state:
            self.recommendation_frame.winfo_children(
            )[idx].children['!button'].config(text="Je n'aime pas")
        else:
            self.recommendation_frame.winfo_children(
            )[idx].children['!button'].config(text="J'aime")

        # Inverser l'état du bouton
        self.recommendation_frame.winfo_children(
        )[idx].children['!button'].state.set(not button_state)

        # Stocker le nouvel état dans self.likes pour le suivi des likes
        button_state = self.recommendation_frame.winfo_children()[
            idx].children['!button'].state.get()
        self.likes[self.pages[self.current_page_index][idx]] = button_state

    def show_recommandation_page(self):
        """ Afficher la recommandation faite via l'algorithme Thompson Sampling. """

        # Détruire le cadre de la page précédente s'il existe
        if hasattr(self, 'recommendation_frame'):
            self.recommendation_frame.destroy()
        # Créer un nouveau cadre pour la recommandation
        self.recommendation_frame = ttk.Frame(self)
        self.recommendation_frame.pack(padx=20, pady=20)

        # Calculer le pourcentage de "J'aime" de chaque thème
        pourcentage_likes = self.calculer_pourcentage_likes()
        print(f"Pourcentage de likes de chaque thème : {pourcentage_likes} \n")
        label_percentage = ttk.Label(
            self.recommendation_frame, text="Voici l'image recommandée suite à vos réponses:")
        label_percentage.pack()

        # Appliquer l'algorithme Thompson Sampling
        theme_a_recommander = self.get_recommandation(pourcentage_likes)
        print(
            f"Thème recommandé via Thompson Sampling : {theme_a_recommander} \n")

        # Récupérer et afficher l'image à recommander
        image_path = self.recommendation_dict[theme_a_recommander]
        image = Image.open(image_path)
        image = image.resize((400, 400))
        photo = ImageTk.PhotoImage(image)
        label_image = tk.Label(self.recommendation_frame, image=photo)
        label_image.image = photo
        label_image.pack()

    def calculer_pourcentage_likes(self) -> dict:
        """ Calculer le pourcentage de 'J'aime' de chaque thème. 

        Returns:
            dict: pourcentages de 'J'aime' de chaque thème.
        """

        # Initialiser un dictionnaire pour stocker le nombre de "J'aime"/True par thème
        theme_counts = {}

        # Parcourir le dictionnaire
        for path, value in self.likes.items():
            # Extraire le nom du dossier (thème)
            theme = path.split('/')[0]
            # Incrémenter le compteur pour ce thème
            theme_counts[theme] = theme_counts.get(theme, 0) + value

        # Initialiser un dictionnaire pour stocker les pourcentages calculés de "J'aime" dans chaque thème
        pourcentage_total = {}

        # Parcourir chaque thème
        for theme, count in theme_counts.items():
            # Calculer le pourcentage de "J'aime" pour ce thème
            pourcentage_total[theme] = count / len(theme_counts)

        return pourcentage_total

    def get_recommandation(self, pourcentage_likes: dict) -> str:
        """ Appliquer l'algorithme Thompson Sampling.

        Args:
            pourcentage_likes (dict): pourcentage de "J'aime" de chaque thème.

        Returns:
            str: thème recommandé par l'algorithme. 
        """

        ts = ThompsonSampling(
            pourcentage_likes, self.nb_iterations, self.taux_exploration)
        theme_a_recommander = ts.appliquer()
        return theme_a_recommander
