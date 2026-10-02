"""Formulaire Streamlit pour estimer le prix d'une maison."""

import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT_DIR / "models" / "house_price_model.joblib"
DEFAULTS_PATH = ROOT_DIR / "models" / "form_defaults.json"

st.set_page_config(page_title="Estimation immobilière", page_icon="🏠")
st.title("Estimer le prix d'un logement")
st.write("Renseignez quelques caractéristiques pour obtenir une estimation.")


@st.cache_resource
def load_model():
    """Charge une fois le modèle déjà entraîné."""
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_defaults():
    return json.loads(DEFAULTS_PATH.read_text(encoding="utf-8"))


if not MODEL_PATH.exists() or not DEFAULTS_PATH.exists():
    st.error("Le modèle n'est pas encore créé.")
    st.code("python -m src.train_model", language="bash")
    st.stop()

model = load_model()
form_data = load_defaults()
defaults = form_data["values"]

with st.expander("Quelles caractéristiques influencent le plus le modèle ?"):
    preprocessor = model.named_steps["preparation"]
    regressor = model.named_steps["regression"]
    importance = pd.DataFrame({
        "Caractéristique": preprocessor.get_feature_names_out(),
        "Importance": regressor.feature_importances_,
    }).nlargest(10, "Importance")
    st.bar_chart(importance, x="Caractéristique", y="Importance", horizontal=True)
    st.caption("Ces scores décrivent l'usage des variables par le modèle ; ils ne prouvent pas une relation de cause à effet.")

with st.form("house_form"):
    st.subheader("Caractéristiques du logement")
    col1, col2 = st.columns(2)

    with col1:
        quality = st.slider("Qualité générale (1 à 10)", 1, 10, 6)
        living_area = st.number_input(
            "Surface habitable (sq ft)", min_value=200, max_value=10000,
            value=int(defaults["GrLivArea"]), step=50,
        )
        basement_area = st.number_input(
            "Surface du sous-sol (sq ft)", min_value=0, max_value=5000,
            value=int(defaults["TotalBsmtSF"]), step=50,
        )
        lot_area = st.number_input(
            "Surface du terrain (sq ft)", min_value=500, max_value=100000,
            value=int(defaults["LotArea"]), step=100,
        )
        year_sold = st.number_input(
            "Année de vente", min_value=2006, max_value=2026,
            value=int(defaults["YrSold"]), step=1,
        )

    with col2:
        neighborhoods = form_data["neighborhood_options"]
        neighborhood_default = defaults["Neighborhood"]
        neighborhood_index = neighborhoods.index(neighborhood_default)
        neighborhood = st.selectbox(
            "Quartier", neighborhoods, index=neighborhood_index
        )
        year_built = st.number_input(
            "Année de construction", min_value=1800, max_value=int(year_sold),
            value=int(defaults["YearBuilt"]), step=1,
        )
        year_renovated = st.number_input(
            "Année de rénovation", min_value=1800, max_value=int(year_sold),
            value=int(defaults["YearRemodAdd"]), step=1,
        )
        garage_cars = st.number_input(
            "Places de garage", min_value=0, max_value=5,
            value=int(defaults["GarageCars"]), step=1,
        )

    submitted = st.form_submit_button("Estimer le prix")

if submitted:
    trained_years = form_data["sale_year_range"]
    if year_sold > trained_years[1]:
        st.warning(
            f"Le modèle a été entraîné sur des ventes de {trained_years[0]} "
            f"à {trained_years[1]}. Une année plus récente est une extrapolation "
            "et peut rendre l'estimation moins fiable."
        )
    # Les champs non affichés gardent une valeur typique issue des données.
    house = defaults.copy()
    house["OverallQual"] = quality
    house["GrLivArea"] = living_area
    house["TotalBsmtSF"] = basement_area
    house["LotArea"] = lot_area
    house["Neighborhood"] = neighborhood
    house["YearBuilt"] = year_built
    house["YearRemodAdd"] = year_renovated
    house["GarageCars"] = garage_cars
    house["YrSold"] = year_sold
    house["TotalSF"] = basement_area + living_area
    house["HouseAge"] = year_sold - year_built
    house["RemodAge"] = year_sold - year_renovated

    prediction = model.predict(pd.DataFrame([house]))[0]
    st.success(f"Prix de vente estimé : {prediction:,.0f} $")
    st.caption(
        "Estimation indicative calculée à partir des caractéristiques saisies "
        "et de valeurs typiques pour les autres informations du logement."
    )
