# Projet RL : Système de recommandation de posts Insta                 

**Étudiants** : DAVID-QUILLOT Mathis, LE GROGNEC Lenaig et NOUZILLE Lorie

### Description du projet ###

Ce projet consiste à **créer une application de recommandations de posts Instagram** présentée sous la forme d'une interface graphique. Pour ce faire, l'utilisateur donne son ressenti "J'aime" ou "Je n'aime pas" sur une sélection d'images issues de quatre thèmes au total. À partir de ces réponses, l'algorithme du Thompson Sampling est exécuté afin de choisir la prochaine image à recommander à l'utilisateur. Celle-ci est ensuite affichée à l'utilisateur.

### Organisation de l'archive ###

L'archive est constituée de trois fichiers principaux à considérer lorsqu'on souhaite simplement utiliser l'application :
*   *requirements.txt* : Permet d'installer les dépendances nécessaires au bon fonctionnement du programme.
*   *__main__.py* : Définit les profils (et donc les thèmes) à considérer pour la recommandation et télécharge les images qui en sont issues. Il lance ensuite l'application, en particulier l'interface graphique.
*   *test.py* : Permet de lancer un nombre *n* de fois l'algorithme du Thompson Sampling afin d'observer ce qui se passe à chaque itération de l'algorithme et de mettre en avant l'aspect lié à l'exploration/l'exploitation de cette méthode. 

L'archive contient également d'autres fichiers utiles à l'implémentation globale de l'application et pour comprendre comment celle-ci a été réalisée :
*   *load_images.py* : Contient une fonction permettant de télécharger les images issues de profils Instagram.
*   *get_images.py* : Permet de sélectionner aléatoirement des images parmi plusieurs dossiers afin d'obtenir, pour chaque thème, une liste d'images avec laquelle on souhaite recueillir le ressenti de l'utilisateur et une image à recommander dans le cas où le thème associé est celui à recommander selon l'algorithme du Thompson Sampling.
*   *thompson_sampling.py* : Contient l'implémentation complète de l'algorithme du Thompson Sampling.
*   *interface.py* : Contient l'implémentation de l'interface graphique qui contrôle l'enchaînement des actions à effectuer pour arriver jusqu'à la recommandation finale.

### Installation ###
```bash
pip install -r "requirements.txt"
```

### Utilisation ###
#### Lancer le programme ####
```bash
python3 __main__.py
```

#### Lancer le test ####
```bash
python3 test.py
```