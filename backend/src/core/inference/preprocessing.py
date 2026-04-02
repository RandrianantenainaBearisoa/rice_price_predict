from src.core.inference.schemas import InferenceInput, Region, Commodity, Month
import pandas as pd

def selection_to_dummies(selected: str, options: list):
    return [1 if selected == opt else 0 for opt in options]

def preprocess_input(inputs: InferenceInput):
    """Make the inputs ready for prediction"""
    commidities = [val.value["feature"] for val in Commodity]
    regions = [val for val in Region]
    months = [val.value["value"] for val in Month]
    values = [inputs.gasoline_price, inputs.diesel_price, inputs.usd_to_mga]+ selection_to_dummies(inputs.region, regions) + selection_to_dummies(inputs.commodity.value["feature"], commidities) + selection_to_dummies(inputs.month.value["feature"], months)
    features = ['gasoline_price','diesel_price','usdmga','Alaotra Mangoro','Amoron I Mania','Analamanga','Analanjirofo','Androy','Anosy','Atsimo Andrefana','Atsimo Atsinanana','Atsinanana','Betsiboka','Boeny','Bongolava','Diana','Haute Matsiatra','Ihorombe','Itasy','Menabe','Sava','Sofia','Vakinankaratra','Vatovavy Fitovinany','Rice (imported)','Rice (local)','month_1','month_10','month_11','month_12','month_2','month_3','month_4','month_5','month_6','month_7','month_8','month_9']
    return pd.DataFrame([{feature: value for feature, value in zip(features, values)}])