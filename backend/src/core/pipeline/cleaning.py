import pandas as pd
from datetime import datetime
import numpy as np

def process_fuel_prices(file_path: str) -> pd.DataFrame:
    """Loads and cleans fuel price data."""
    gasoline = pd.read_excel(file_path, sheet_name="Regular Gasoline (below RON 95)").iloc[67]
    diesel = pd.read_excel(file_path, sheet_name="Diesel").iloc[101]
    kerosene = pd.read_excel(file_path, sheet_name="Kerosene").iloc[34]

    df = pd.DataFrame({
        "date": gasoline.index[4:].values,
        "gasoline_price": gasoline[4:].values.astype(float),
        "diesel_price": diesel[2:115].values.astype(float),
        "kerosene_price": kerosene[2:].values.astype(float)
    })

    return df.ffill().bfill()

def process_rice_prices(file_path: str, start_date, end_date) -> pd.DataFrame:
    """Filters rice price data for a given period."""
    df = pd.read_csv(file_path)
    
    mask = (df["commodity"].str.contains("Rice")) & \
           (df["date"] >= str(start_date)) & \
           (df["date"] <= str(end_date))
    return df[mask]

def run_data_preparing():
    INPUT_FUEL = 'data/data_lake/global_fuel_price.xlsx'
    INPUT_FOOD = 'data/data_lake/mdg_food_price.csv'
    OUTPUT_FOLDER = 'data/data_warehouse/'

    fuel_df = process_fuel_prices(INPUT_FUEL)
    
    rice_df = process_rice_prices(
        INPUT_FOOD, 
        start_date=fuel_df.iloc[0]["date"], 
        end_date=fuel_df.iloc[-1]["date"]
    )

    fuel_df.to_csv(f"{OUTPUT_FOLDER}prepared_fuel_price.csv", index=False)
    rice_df.to_csv(f"{OUTPUT_FOLDER}prepared_rice_price.csv", index=False)