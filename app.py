import streamlit as st
import pandas as pd
import base64
import pickle
import os

st.set_page_config(page_title="🍽️ Restaurant Finder", layout="wide")

gif_path = "rocket-3972_128.gif"
with open(gif_path, "rb") as f:
    gif_base64 = base64.b64encode(f.read()).decode()

st.markdown(f"""
<style>
.stApp {{
    background: url("data:image/gif;base64,{gif_base64}") no-repeat center center fixed;
    background-size: cover;
}}

.overlay {{
    background-color: rgba(0,0,0,0.6);
    padding: 2rem;
    border-radius: 15px;
    max-width: 1200px;
    margin: auto;
    color: white;
    backdrop-filter: blur(5px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.5);
}}

.restaurant-card {{
    background-color: rgba(255, 255, 255, 0.1);
    padding: 1rem 1.5rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    backdrop-filter: blur(3px);
    color: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}}
</style>
""", unsafe_allow_html=True)

try:
    with open("models/processed.pkl", "rb") as f:
        countries_df = pickle.load(f)
        countries_list = countries_df["Country"].dropna().unique()
except Exception as e:
    st.error(f"Failed to load country list from processed.pkl: {e}")
    st.stop()

st.markdown("""
<h1 style='text-align: center; font-size: 3rem; margin-bottom: 2rem;'>
    🍽️ Restaurant Finder
</h1>
""", unsafe_allow_html=True)

selected_country = st.selectbox("🌍 Select Country", sorted(countries_list))

country_file = None
available_files = os.listdir("models")
for file in available_files:
    if file.lower() == f"{selected_country.lower()}.pkl":
        country_file = os.path.join("models", file)
        break

if not country_file:
    st.error(f"No data file found for '{selected_country}'. Please ensure a .pkl exists.")
    st.stop()

try:
    df = pd.read_pickle(country_file)
except Exception as e:
    st.error(f"Failed to load data for {selected_country}: {e}")
    st.stop()

states = df["State"].dropna().unique()
selected_state = st.selectbox("🗺️ Select State", sorted(states))

cities = df[df["State"] == selected_state]["City"].dropna().unique()
selected_city = st.selectbox("🏙️ Select City", sorted(cities))

cuisines = df[
    (df["State"] == selected_state) &
    (df["City"] == selected_city)
]["Primary Cuisine"].dropna().unique()
selected_cuisine = st.selectbox("🍜 Select Primary Cuisine", sorted(cuisines))

filtered_df = df[
    (df["State"] == selected_state) &
    (df["City"] == selected_city) &
    (df["Primary Cuisine"] == selected_cuisine)
]

st.subheader(f"🔍 Showing {len(filtered_df)} restaurant(s) in {selected_city} for {selected_cuisine} cuisine")

for _, row in filtered_df.iterrows():
    st.markdown(f"""
    <div class="restaurant-card">
        <h4>🍽️ {row['Restaurant Name']}</h4>
        <p><b>📍 Location:</b> {row['Address']}, {row['City']}, {row['State']}, {row['Country']}</p>
        <p><b>🍜 Primary Cuisine:</b> {row['Primary Cuisine']} | <b>🍱 Other Cuisines:</b> {row['Cuisines']}</p>
        <p><b>💵 Price Range:</b> {row['Price range']} | <b>Avg Cost for Two:</b> ₹{row['Average Cost for two']}</p>
        <p><b>🚚 Online Delivery:</b> {'Yes' if row['Has Online delivery'] else 'No'} |
           <b>📦 Delivering Now:</b> {'Yes' if row['Is delivering now'] else 'No'} |
           <b>🍽️ Table Booking:</b> {'Yes' if row['Has Table booking'] else 'No'}</p>
        <p><b>⭐ Rating:</b> {row['Aggregate rating']} | <b>🗳️ Votes:</b> {row['Votes']}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
