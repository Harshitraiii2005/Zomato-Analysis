-- Zomato Analysis & Restaurant Recommendation System
Welcome to the Zomato Analysis & Restaurant Recommendation System — an interactive web app built with Streamlit to help users explore and find the best restaurants based on location and cuisine preferences.
-- Project Overview
This project analyzes Zomato restaurant data to provide insights and personalized restaurant recommendations. Users can select their country, state, city, and preferred cuisine, then explore restaurants matching their criteria with detailed information including ratings, delivery options, price ranges, and more.

-- Features
* Interactive filters for Country, State, City, and Primary Cuisine.
* Displays detailed restaurant information:
* Location, address, and cuisines served.
* Price range and average cost for two.
* Availability of online delivery, table booking, and current delivery status.
* Ratings and number of votes.
* Beautiful UI with a dynamic GIF background and translucent card overlays for better readability.
* Fully responsive and scalable with modular data files per country.
* Efficient data loading and caching using pickle files.

-- Tech Stack
* Python — Data processing and backend logic.
* Streamlit — Web app framework for building the interactive UI.
* Pandas — Data manipulation and analysis.
* Pickle — For fast loading of preprocessed datasets.
* HTML & CSS — Custom styling embedded in Streamlit markdown.


-- How to Run Locally
Clone the repo
bash
git clone https://github.com/yourusername/zomato-recommendation-app.git
cd zomato-recommendation-app
Create and activate a virtual environment (optional but recommended)
bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
Install dependencies
bash
pip install -r requirements.txt
Run the Streamlit app
bash
streamlit run app.py
Open the app
Navigate to http://localhost:8501 in your browser.

-- Dataset
The dataset consists of cleaned and processed Zomato restaurant data, separated by country and stored as pickle (.pkl) files for quick loading.
The master file processed.pkl contains the list of available countries for selection.

This project is licensed under the MIT License





