import os
import pickle
import pandas as pd

def test_processed_file_exists():
    assert os.path.exists("models/processed.pkl")

def test_processed_file_format():
    with open("models/processed.pkl", "rb") as f:
        df = pickle.load(f)
        assert isinstance(df, pd.DataFrame)
        assert "Country" in df.columns

def test_country_data_files():
    files = os.listdir("models")
    files = [f for f in files if f.endswith(".pkl") and f != "processed.pkl"]
    assert len(files) > 0
    for file in files:
        with open(os.path.join("models", file), "rb") as f:
            country_df = pickle.load(f)
            assert isinstance(country_df, pd.DataFrame)
            for col in ["State", "City", "Primary Cuisine", "Restaurant Name", "Address", "Price range"]:
                assert col in country_df.columns

def test_filter_logic():
    country_file = "models/india.pkl"
    if not os.path.exists(country_file):
        return
    df = pd.read_pickle(country_file)
    state = df["State"].dropna().unique()[0]
    city = df[df["State"] == state]["City"].dropna().unique()[0]
    cuisine = df[(df["State"] == state) & (df["City"] == city)]["Primary Cuisine"].dropna().unique()[0]
    filtered = df[
        (df["State"] == state) &
        (df["City"] == city) &
        (df["Primary Cuisine"] == cuisine)
    ]
    assert not filtered.empty
