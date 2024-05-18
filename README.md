# LITRevu

## Description

Ce projet est une application web basée sur Django pour gérer des tickets et des critiques. Les utilisateurs peuvent créer, modifier et supprimer des tickets, ainsi qu'ajouter des critiques aux tickets. L'application inclut l'authentification des utilisateurs et utilise Bootstrap pour le style.

## Fonctionnalités

- demander des critiques de livres ou d’articles, en créant un billet ;
- lire des critiques de livres ou d’articles ;
- publier des critiques de livres ou d’articles.

## Installation

### Prérequis

- Python 3 ou supérieur
- Django 3 ou supérieur
- Virtualenv

### Étapes

1. Clonez le dépôt :

    ```bash
   git clone https://github.com/nomutilisateur/nom-depot.git
   cd nom-depot
   ```
2. Créez et activez un environnement virtuel :

    ```bash
    python -m venv env
    source env/bin/activate  # Sur Windows utilisez `env\Scripts\activate`
    ```
3. Installez les packages requis :
    ```bash
    pip install -r requirements.txt
    ```
4. Appliquez les migrations :
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5. Créez un superutilisateur :
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6. Lancez le serveur de développement :
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
7. Ouvrez votre navigateur web et allez sur http://127.0.0.1:8000.