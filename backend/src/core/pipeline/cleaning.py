import pandas as pd
from datetime import datetime
import numpy as np
from src.core.utils.helpers import get_cleaning_destination

def process_fuel_prices() -> pd.DataFrame:
    """Loads and cleans fuel price data."""

    file_path = 'data/data_lake/global_fuel_price.xlsx'

    gasoline_data = pd.read_excel(file_path, sheet_name="Regular Gasoline (below RON 95)")
    gasoline_price = gasoline_data[gasoline_data["Country"] == "Madagascar"]

    diesel_data = pd.read_excel(file_path, sheet_name="Diesel")
    diesel_price = diesel_data[diesel_data["Diesel (LCU/liter)"] == "Madagascar"]

    kerosene_data = pd.read_excel(file_path, sheet_name="Kerosene")
    kerosene_price = kerosene_data[kerosene_data["Kerosene (LCU/liter)"] == "Madagascar"]

    keys_date = [date for date in gasoline_price.keys() if isinstance(date, datetime)]

    mdg_fuel_data = pd.DataFrame({
        "date": keys_date,
        "gasoline_price": gasoline_price[keys_date].values.flatten().astype(float),
        "diesel_price": diesel_price[keys_date].values.flatten().astype(float),
        "kerosene_price": kerosene_price[keys_date].values.flatten().astype(float)
    })

    return mdg_fuel_data.ffill().bfill()

def process_rice_prices(start_date, end_date) -> pd.DataFrame:
    """Filters rice price data for a given period."""

    file_path = 'data/data_lake/mdg_food_price.csv'

    mdg_rice_data = pd.read_csv(file_path)

    mdg_rice_data["date"] = pd.to_datetime(mdg_rice_data["date"])
    
    mask = (mdg_rice_data["commodity"].str.contains("Rice")) & \
           (mdg_rice_data["date"] >= start_date) & \
           (mdg_rice_data["date"] <= end_date)
    
    return mdg_rice_data[mask].ffill().bfill()

def run_data_preparing():
    try:
        print("Starting data cleaning and preparation...")

        OUTPUT_FOLDER = get_cleaning_destination() + "/"

        mdg_fuel_data = process_fuel_prices()
        
        mdg_rice_data = process_rice_prices(
            start_date=mdg_fuel_data.iloc[0]["date"], 
            end_date=mdg_fuel_data.iloc[-1]["date"]
        )

        rice_and_fuel_price = pd.merge_asof(
            mdg_rice_data.sort_values('date'), 
            mdg_fuel_data.sort_values('date'), 
            on='date', 
            direction='backward'
        )

        rice_and_fuel_price.to_csv(f"{OUTPUT_FOLDER}mdg_rice_and_fuel_price.csv", index=False)

        print(f"✅ Data ready for EDA and Modeling in {OUTPUT_FOLDER}.")
    except Exception as e:
        print(f"💥 An unexpected error occurred: {e}")