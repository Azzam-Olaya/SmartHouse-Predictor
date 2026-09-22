from pathlib import Path

# Racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Données
RAW_DATA_PATH = BASE_DIR / "House_Prices.csv"
DATA_DESCRIPTION_PATH = BASE_DIR / "data_description.txt"

# Données préparées
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

# Target
TARGET = "SalePrice"

# Colonnes qui ne doivent pas être utilisées comme variables prédictives
DROP_COLUMNS = ["Id"]

# Random state pour obtenir les mêmes résultats
RANDOM_STATE = 42

# Taille du jeu de test
TEST_SIZE = 0.20