import pandas as pd

from src.config import RAW_DATA_PATH, TARGET, DROP_COLUMNS


def load_data():
    """
    Charge le dataset original.
    """
    df = pd.read_csv(RAW_DATA_PATH)
    return df


def basic_information(df):
    """
    Retourne les informations principales du dataset.
    """
    return {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "duplicates": df.duplicated().sum(),
        "missing_values": df.isna().sum()
    }


def separate_features_target(df):
    """
    Sépare les variables explicatives X de la variable cible y.
    """
    X = df.drop(columns=[TARGET] + DROP_COLUMNS)
    y = df[TARGET]

    return X, y

