# P2_Python-pour-lanalyse-de-marcher

Projet N°2 du parcours OpenClassrooms


## installer le projet

commencer par cloner le projet avec git clone

une fois le projet en local, créer votre environement virtuel :

```py
py -m venv .env
```

mettez à jour Pip :

```py
py -m pip install --upgrade pip
```

installer les dépendance :

```py
pip install -r requirements.txt
```

## Utilisation

lancer une invite de commande.

placer vous dans le dossier du projet ou ce situe le fichier scraper.py

lancez le script python avec la commande :

```py
py scraper.py
```

## hiérarchie

le script scraper.py ce situe a la racine du projet.

lancer le script créera un dossier "ScrappedData" à la racine du projet.

à l'intérieur vous retrouverez un dossier par catégorie de livre, dans les quelles ce trouve un fichier CSV avec les détails de tout les livres de la catégorie et un dossier IMG avec les images de ces livre.
