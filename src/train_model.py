"""Entraîne le modèle une fois et enregistre le modèle et les valeurs du formulaire."""

import json

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config import BASE_DIR, RAW_DATA_PATH, TARGET, DROP_COLUMNS, RANDOM_STATE


MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "house_price_model.joblib"
DEFAULTS_PATH = MODEL_DIR / "form_defaults.json"
SELECTED_PARAMS_PATH = MODEL_DIR / "selected_rf_params.json"


def add_features(data):
    """Ajoute des caractéristiques calculées à partir des colonnes existantes."""
    data = data.copy()
    data["TotalSF"] = (
        data["TotalBsmtSF"].fillna(0)
        + data["1stFlrSF"].fillna(0)
        + data["2ndFlrSF"].fillna(0)
    )
    data["TotalBathrooms"] = (
        data["FullBath"].fillna(0)
        + 0.5 * data["HalfBath"].fillna(0)
        + data["BsmtFullBath"].fillna(0)
        + 0.5 * data["BsmtHalfBath"].fillna(0)
    )
    data["HouseAge"] = data["YrSold"] - data["YearBuilt"]
    data["RemodAge"] = data["YrSold"] - data["YearRemodAdd"]
    return data


def main():
    data = pd.read_csv(RAW_DATA_PATH)
    y = data[TARGET]
    X = data.drop(columns=[TARGET] + DROP_COLUMNS)
    X = add_features(X)

    numeric_columns = X.select_dtypes(include="number").columns.tolist()
    categorical_columns = X.select_dtypes(exclude="number").columns.tolist()

    numeric_steps = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    categorical_steps = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    preparation = ColumnTransformer([
        ("numeric", numeric_steps, numeric_columns),
        ("categorical", categorical_steps, categorical_columns),
    ])

    best_params = {
        "n_estimators": 200,
        "max_depth": None,
        "min_samples_leaf": 1,
    }
    if SELECTED_PARAMS_PATH.exists():
        best_params.update(json.loads(SELECTED_PARAMS_PATH.read_text(encoding="utf-8")))

    model = Pipeline([
        ("preparation", preparation),
        ("regression", RandomForestRegressor(
            random_state=RANDOM_STATE,
            n_jobs=-1,
            **best_params,
        )),
    ])
    model.fit(X, y)

    # Le formulaire ne demande que quelques caractéristiques. Les autres
    # reçoivent une valeur typique calculée sur le jeu d'entraînement.
    defaults = {}
    for column in X.columns:
        if column in numeric_columns:
            defaults[column] = float(X[column].median())
        else:
            defaults[column] = str(X[column].mode(dropna=True).iloc[0])

    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    form_data = {
        "values": defaults,
        "neighborhood_options": sorted(X["Neighborhood"].dropna().unique().tolist()),
        "sale_year_range": [int(X["YrSold"].min()), int(X["YrSold"].max())],
    }
    DEFAULTS_PATH.write_text(
        json.dumps(form_data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Paramètres du modèle : {best_params}")
    print(f"Modèle enregistré : {MODEL_PATH}")
    print(f"Valeurs du formulaire enregistrées : {DEFAULTS_PATH}")


if __name__ == "__main__":
    main()
