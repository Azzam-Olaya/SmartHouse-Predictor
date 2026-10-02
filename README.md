# SmartHouse Predictor

Application Streamlit pour estimer le prix de vente d'une maison à partir de ses caractéristiques.

## Installation

Utilisez Python 3.13 en 64 bits sous Windows. Depuis la racine du projet, créez un environnement virtuel et installez les dépendances :

```bash
py -3.13 -m venv .venv313
.venv313\Scripts\python.exe -m pip install --upgrade pip
.venv313\Scripts\python.exe -m pip install -r requirements.txt
```

Les dépendances incluent aussi Matplotlib et Seaborn pour les notebooks d’analyse. Le jeu de données contient les prix de vente historiques d’Ames, Iowa ; les montants du modèle sont en dollars américains.

## Entraîner et sauvegarder le modèle

Cette commande entraîne le Random Forest une fois et crée les fichiers du modèle dans `models/` :

```bash
.venv313\Scripts\python.exe -m src.train_model
```

Le modèle n'est pas réentraîné lors des prédictions dans l'application.

## Lancer l'application

```bash
.venv313\Scripts\python.exe -m streamlit run app/app.py
```

Streamlit affiche une adresse locale à ouvrir dans le navigateur. Le formulaire demande quelques caractéristiques ; les autres colonnes utilisent des valeurs typiques calculées depuis le jeu de données lors de l'entraînement.

## Lancer avec Docker

Après avoir exécuté le notebook de modélisation et le script d’entraînement afin que les fichiers du modèle existent, et avec Docker Desktop installé et démarré, depuis la racine du projet :

```bash
docker compose up --build
```

Ouvrez ensuite [http://localhost:8501](http://localhost:8501). Pour arrêter l'application, utilisez `Ctrl+C`, puis :

```bash
docker compose down
```

Le conteneur charge le modèle déjà sauvegardé ; il ne le réentraîne pas au démarrage ni à chaque prédiction.

## Modélisation et interprétation

Le notebook `notebooks/exploration.ipynb` contient l'analyse exploratoire et la création de variables. Le notebook `notebooks/modeling.ipynb` compare trois modèles, réalise la validation croisée, ajuste le Random Forest et examine les erreurs. Les résultats affichés dépendent de l'exécution des cellules dans l'ordre.

Après la recherche, `models/best_rf_params.json` conserve les meilleurs paramètres selon la validation croisée. Le notebook écrit aussi `models/selected_rf_params.json` : il retient ces paramètres seulement s’ils améliorent le RMSE du jeu de test ; sinon il conserve le Random Forest initial. Relancez `.venv313\Scripts\python.exe -m src.train_model` pour entraîner le modèle final de l’application avec les paramètres retenus.
