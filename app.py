import streamlit as st
import pandas as pd
import os

# --- Page Config ---
st.set_page_config(page_title="🍽️ Restaurant Finder", layout="wide")

# --- CSS styles + video background ---
st.markdown(
    """
    <style>
    /* Full viewport video background */
    #bg-video {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        object-fit: cover;
        z-index: -1;
        filter: brightness(0.6); /* darken video for readability */
    }

    /* Overlay to dim video if needed */
    #overlay {
        position: fixed;
        top:0; left:0; width:100vw; height:100vh;
        background: rgba(0, 0, 0, 0.4);
        z-index: 0;
    }

    /* Center everything vertically & horizontally */
    .main-container {
        position: relative;  /* to stack above video */
        z-index: 1;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        padding: 20px;
        gap: 40px;
    }

    h1 {
        font-size: 3.5rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 0 15px rgba(0, 0, 0, 0.8);
    }

    .input-container {
        background: rgba(0,0,0,0.65);
        padding: 35px 50px;
        border-radius: 25px;
        width: 450px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8.5px);
        -webkit-backdrop-filter: blur(8.5px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    /* Style select boxes with 3D-ish blue glow */
    div[role="listbox"], div[data-baseweb="select"] > div:first-child {
        border-radius: 15px !important;
        border: 2px solid #5e9cff !important;
        box-shadow: 0 4px 15px rgba(94, 156, 255, 0.6);
        background: linear-gradient(145deg, #3b6ed6, #2a4bb7);
        color: white !important;
        font-weight: 600 !important;
    }

    div[role="option"]:hover {
        background-color: #2a4bb7 !important;
        color: white !important;
    }

    .stSelectbox > div > div {
        max-width: 400px;
        margin: auto;
    }

    .info-box {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        color: white;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        text-align: left;
        transition: transform 0.2s ease;
    }

    .info-box:hover {
        transform: scale(1.03);
        background: rgba(255, 255, 255, 0.25);
    }
    </style>

    <!-- Video background -->
    <video autoplay muted loop id="bg-video" playsinline>
      <source src="https://cdn.pixabay.com/animation/2023/02/13/09/42/09-42-58-584_512.gif" type="video/mp4">
      Your browser does not support the video tag.
    </video>

    <!-- Optional overlay -->
    <div id="overlay"></div>
    """,
    unsafe_allow_html=True
)

# Main container div
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Title
st.markdown('<h1>🍴 Restaurant Recommender</h1>', unsafe_allow_html=True)

# Input container div
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# Folder containing country pkls
pkl_folder = "models/"
countries = [f.split(".pkl")[0] for f in os.listdir(pkl_folder) if f.endswith(".pkl")]

# Step 1: Select Country
country = st.selectbox("🌍 Select Country", sorted(countries))

if country:
    data_path = os.path.join(pkl_folder, f"{country}.pkl")
    try:
        df_country = pd.read_pickle(data_path)
    except Exception as e:
        st.error(f"Failed to load data for {country}: {e}")
        st.stop()

    # Step 2: Select State or fallback to City
    states = df_country['State'].dropna().unique() if 'State' in df_country.columns else df_country['City'].unique()
    state = st.selectbox(f"🏙️ Select State in {country}", sorted(states)) if len(states) > 0 else None

    # Step 3: Select City filtered by state or country
    if state:
        cities = df_country[df_country['State'] == state]['City'].unique()
    else:
        cities = df_country['City'].unique()
    city = st.selectbox(f"🌆 Select City in {state if state else country}", sorted(cities))

    # Step 4: Filter and show restaurants
    if city:
        filtered_df = df_country[df_country['City'] == city]

        if not filtered_df.empty:
            st.markdown(f"### 🏆 Top Restaurants in {city}, {state if state else country}")
            for idx, row in filtered_df.sort_values('Aggregate rating', ascending=False).head(10).iterrows():
                online_delivery = "Yes" if row['Has Online delivery'] == 1 else "No"
                delivering_now = "Yes" if row['Is delivering now'] == 1 else "No"
                table_booking = "Yes" if row['Has Table booking'] == 1 else "No"
                cuisine = row.get('Primary Cuisine', row['Cuisines'])

                st.markdown(f"""
                <div class='info-box'>
                    <h4>{row['Restaurant Name']}</h4>
                    <b>📍 Address:</b> {row['Address']}<br>
                    <b>🍲 Cuisine:</b> {cuisine}<br>
                    <b>💻 Online Delivery:</b> {online_delivery} | <b>🚚 Delivering Now:</b> {delivering_now}<br>
                    <b>🍽️ Table Booking:</b> {table_booking}<br>
                    <b>⭐ Rating:</b> {row['Aggregate rating']} | <b>💰 Price Range:</b> {row['Price range']}<br>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No restaurants found for this city.")

st.markdown('</div>', unsafe_allow_html=True)  # close input-container
st.markdown('</div>', unsafe_allow_html=True)  # close main-container
