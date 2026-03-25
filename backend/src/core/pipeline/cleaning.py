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

def process_world_market_prices() -> pd.DataFrame:
    """Get the usefull features from the world bank commodity price file."""

    file_path = 'data/data_lake/worldbank_commodity_price.xlsx'

    wrld_com_prices = pd.read_excel(file_path, "Monthly Prices", skiprows=4)
    wrld_com_prices = wrld_com_prices.iloc[1:].reset_index(drop=True)

    wrld_com_prices["date"] = pd.to_datetime([f"{date_str.replace('M', '-')}-01" for date_str in wrld_com_prices["Unnamed: 0"].values])

    col_names = ["date", 'Phosphate rock', 'DAP', 'TSP', 'Urea', 'Potassium chloride']

    wrld_fertilz_prices = wrld_com_prices[["date", 'Phosphate rock', 'DAP', 'TSP', 'Urea ', 'Potassium chloride **']].copy()
    wrld_fertilz_prices.columns = col_names
    
    for col in col_names[1:]:
        wrld_fertilz_prices[col] = pd.to_numeric(wrld_fertilz_prices[col], errors='coerce') # ... -> NaN

    wrld_fertilz_prices[col_names[1:]] = wrld_fertilz_prices[col_names[1:]].interpolate(method="linear", limit_direction="both")
    
    return wrld_fertilz_prices

def run_data_preparing():
    try:
        print("Starting data cleaning and preparation...")

        OUTPUT_FOLDER = get_cleaning_destination() + "/"

        mdg_fuel_data = process_fuel_prices()
        
        mdg_rice_data = process_rice_prices(
            start_date=mdg_fuel_data.iloc[0]["date"], 
            end_date=mdg_fuel_data.iloc[-1]["date"]
        )

        wrld_fertilz_prices = process_world_market_prices()

        rice_and_fuel_price = pd.merge_asof(
            mdg_rice_data.sort_values('date'), 
            mdg_fuel_data.sort_values('date'), 
            on='date', 
            direction='backward'
        )

        rice_data = pd.merge_asof(
            rice_and_fuel_price.sort_values('date'),
            wrld_fertilz_prices.sort_values('date'),
            on='date',
            direction='backward'
        )

        rice_data.to_csv(f"{OUTPUT_FOLDER}mdg_rice_data.csv", index=False)

        print(f"✅ Data ready for EDA and Modeling in {OUTPUT_FOLDER}.")
    except Exception as e:
        print(f"💥 An unexpected error occurred: {e}")