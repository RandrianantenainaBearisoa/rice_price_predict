import pandas as pd
import yfinance as yf
import numpy as np
from sklearn.preprocessing import PowerTransformer
from src.core.utils.helpers import get_feature_store_destination

def get_currency_data():
    usd_mga_exchange = yf.download("USDMGA=X", start="2015-01-01", end="2026-03-24")

    currency_data = usd_mga_exchange.resample("MS").mean()["Close"]
    currency_data = currency_data.reset_index()
    currency_data.columns = [col.lower() for col in currency_data.columns]
    currency_data["date"] = pd.to_datetime(currency_data["date"])
    currency_data["usdmga"] = currency_data["usdmga=x"]

    return currency_data[["date", "usdmga"]]

def apply_boxcox_transformation(df: pd.DataFrame, column: str):
    """Apply Box-Cox transformation to a specified column in the DataFrame."""
    contains_negative = (df[column] < 0).any()
    if contains_negative:
        raise ValueError(f"Box-Cox transformation cannot be applied to column '{column}' because it contains negative values.")
    else:
        pt = PowerTransformer(method="box-cox", standardize=True)
        target_reshaped = df[column].to_numpy().reshape(-1, 1)

    return pt.fit_transform(target_reshaped)

def get_month_column(df: pd.DataFrame, date_column: str):
    """Returns the column containing the month : month_i"""

    return "month_" + (df[date_column].dt.month.astype(str))

def get_rice_data():
    rice_data = pd.read_csv('data/data_warehouse/mdg_rice_data.csv')

    rice_data["date"] = pd.to_datetime(rice_data["date"])
    rice_data["price_transformed"] = apply_boxcox_transformation(df=rice_data, column="price")
    rice_data["month"] = get_month_column(df=rice_data, date_column="date")
    
    return rice_data

def get_applicant_features():
    """Make the features for the model from the cleaned data."""
    mdg_rice_data = get_rice_data()
    currency_data = get_currency_data()

    rice_data = pd.merge_asof(
            mdg_rice_data.sort_values('date'), 
            currency_data.sort_values('date')[['date','usdmga']],
            on='date', 
            direction='backward'
        )
    
    return rice_data[["latitude", "DAP","market_id", "gasoline_price", "diesel_price", "usdmga", "admin1", "pricetype", "commodity", "price_transformed", "month"]]

def get_applicant_dummies():
    """Return the selected features with one hot encoded categorical features"""
    rice_data_applicants = get_applicant_features()

    data_encoded = pd.get_dummies(rice_data_applicants, prefix="", prefix_sep="", dtype=int)
    data_numeric = data_encoded.select_dtypes(include=[np.number])
    
    return data_numeric

def get_selected_features():
    """Select the features used for the final model training"""
    features = ['gasoline_price', 'diesel_price', 'usdmga', 'Alaotra Mangoro', 'Amoron I Mania', 'Analamanga', 'Analanjirofo', 'Androy', 'Anosy', 'Atsimo Andrefana', 'Atsimo Atsinanana', 'Atsinanana', 'Betsiboka', 'Boeny', 'Bongolava', 'Diana', 'Haute Matsiatra', 'Ihorombe', 'Itasy', 'Menabe', 'Sava', 'Sofia', 'Vakinankaratra', 'Vatovavy Fitovinany', 'Rice (imported)', 'Rice (local)', 'month_1', 'month_10', 'month_11', 'month_12', 'month_2', 'month_3', 'month_4', 'month_5', 'month_6', 'month_7', 'month_8', 'month_9']
    target = ["price_transformed"]
    
    applicant_dummies = get_applicant_dummies()
    
    return applicant_dummies[features + target]

def run_feature_engineering():
    """Run the feature engineering step of the pipeline."""
    try:
        print("Starting feature engineering...")

        selected_features = get_selected_features()
        destination = get_feature_store_destination()
        selected_features.to_csv(f"{destination}/selected_features.csv", index=False)

        print("✅ Feature engineering completed successfully.")
    except Exception as e:
        print(f"💥 Error occurred during feature engineering: {e}")