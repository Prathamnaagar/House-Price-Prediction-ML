import streamlit as st
import pandas as pd
import numpy as np
import joblib
import pickle

# Load model
with open("house_price_model.pkl", "rb") as file:
    model = pickle.load(file)

feature_names = joblib.load("feature_names.pkl")

st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 House Price Prediction")
st.write("Enter house details and predict the estimated price.")

cities = [
    'Auburn','Beaux Arts Village','Bellevue','Black Diamond',
    'Bothell','Burien','Carnation','Clyde Hill','Covington',
    'Des Moines','Duvall','Enumclaw','Fall City','Federal Way',
    'Inglewood-Finn Hill','Issaquah','Kenmore','Kent','Kirkland',
    'Lake Forest Park','Maple Valley','Medina','Mercer Island',
    'Milton','Newcastle','Normandy Park','North Bend','Pacific',
    'Preston','Ravensdale','Redmond','Renton','Sammamish',
    'SeaTac','Seattle','Shoreline','Skykomish','Snoqualmie',
    'Snoqualmie Pass','Tukwila','Vashon','Woodinville',
    'Yarrow Point'
]

col1, col2 = st.columns(2)

with col1:
    bedrooms = st.number_input("Bedrooms", 1, 20, 3)
    bathrooms = st.number_input("Bathrooms", 1.0, 20.0, 2.0)
    sqft_living = st.number_input("Sqft Living", 100, 10000, 2000)
    sqft_lot = st.number_input("Sqft Lot", 100, 100000, 5000)
    floors = st.number_input("Floors", 1.0, 5.0, 2.0)
    waterfront = st.selectbox("Waterfront", [0,1])
    view = st.slider("View", 0, 4, 0)

with col2:
    condition = st.slider("Condition", 1, 5, 3)
    sqft_above = st.number_input("Sqft Above", 100, 10000, 1500)
    sqft_basement = st.number_input("Sqft Basement", 0, 5000, 0)
    yr_built = st.number_input("Year Built", 1900, 2025, 2000)
    yr_renovated = st.number_input("Year Renovated", 0, 2025, 0)
    zip_code = st.number_input("ZIP Code", 10000, 99999, 98001)
    city = st.selectbox("City", cities)

year = st.number_input("Sale Year", 2000, 2030, 2014)
month = st.number_input("Sale Month", 1, 12, 5)
day = st.number_input("Sale Day", 1, 31, 2)

effective_age = year - max(yr_built, yr_renovated) if yr_renovated > 0 else year - yr_built

if st.button("Predict House Price"):

    data = {col: 0 for col in feature_names}

    data['bedrooms'] = bedrooms
    data['bathrooms'] = bathrooms
    data['sqft_living'] = sqft_living
    data['sqft_lot'] = sqft_lot
    data['floors'] = floors
    data['waterfront'] = waterfront
    data['view'] = view
    data['condition'] = condition
    data['sqft_above'] = sqft_above
    data['sqft_basement'] = sqft_basement
    data['yr_built'] = yr_built
    data['yr_renovated'] = yr_renovated
    data['year'] = year
    data['month'] = month
    data['day'] = day
    data['effective_age'] = effective_age
    data['zip'] = zip_code

    city_col = f"city_{city}"

    if city_col in data:
        data[city_col] = 1

    input_df = pd.DataFrame([data])

    prediction = model.predict(input_df)

    actual_price = np.expm1(prediction[0])

    st.success(f"🏠 Estimated House Price: ${actual_price:,.0f}")