import numpy as np
import pandas as pd
from src.core.pipeline.feat_eng import get_currency_data, apply_boxcox_transformation, get_month_column, get_rice_data, get_applicant_features, get_applicant_dummies, get_selected_features, run_feature_engineering
from src.core.utils.helpers import get_categorical_columns, check_file_exist
from collections import Counter
from unittest.mock import patch


def test_get_currency_data():
    currency_data = get_currency_data()

    assert "date" in currency_data.columns, "The 'date' column is missing from the currency data."
    assert "usdmga" in currency_data.columns, "The 'usdmga' column is missing from the currency data."
    assert currency_data.isnull().sum().sum() == 0, "There are missing values in the currency data."
    assert currency_data["date"].dtype == "datetime64[ns]", "The 'date' column is not in datetime format."
    assert currency_data["usdmga"].dtype == "float64", "The 'usdmga' column is not in the correct format."

def test_apply_boxcox_transformation(tmp_path):
    tmp_path = str(tmp_path)
    sample_data = pd.DataFrame({"price": [1, 2, 5, 10, 25, 50, 100, 250, 500, 1000]})
    expected_transformed = [-1.55, -1.25, -0.85, -0.55, -0.14, 0.17, 0.49, 0.91, 1.22, 1.55]
    with patch("src.core.pipeline.feat_eng.get_transformation_artifact_location") as mock_art_destination:
        mock_art_destination.return_value = tmp_path
        transformed_data = apply_boxcox_transformation(sample_data, "price")

        assert transformed_data.shape == (10, 1), "The transformed data should have the same number of rows and one column."
        assert not np.any(np.isnan(transformed_data)), "There should be no NaN values in the transformed data."
        assert np.isfinite(transformed_data).all(), "All values in the transformed data should be finite."
        assert np.allclose(transformed_data.flatten().round(2), expected_transformed), "The transformed values do not match the expected values within the tolerance level."
        assert check_file_exist("box_cox_transfo.joblib", tmp_path + "box_cox_transformation/")

def test_get_month_column():
    sample_data = pd.DataFrame({"date": pd.to_datetime(["2021-01-15", "2021-02-20", "2021-03-10"])})
    expected_months = ["month_1", "month_2", "month_3"]
    month_column = get_month_column(sample_data, "date")

    assert month_column.equals(pd.Series(expected_months)), "The month column does not match the expected values."

def test_get_rice_data():
    rice_data = get_rice_data()

    assert "date" in rice_data.columns, "The 'date' column is missing from the rice data."
    assert "price_transformed" in rice_data.columns, "The 'price_transformed' column is missing from the rice data."
    assert "month" in rice_data.columns, "The 'month' column is missing from the rice data."
    assert rice_data.isnull().sum().sum() == 0, "There are missing values in the rice data."
    assert rice_data["date"].dtype == "datetime64[ns]", "The 'date' column is not in datetime format."
    assert rice_data["price_transformed"].dtype == "float64", "The 'price_transformed' column is not in the correct format."

def test_get_applicant_features():
    applicant_features = get_applicant_features()
    expected_columns = ["latitude", "DAP", "market_id", "gasoline_price", "diesel_price", "usdmga", "admin1", "pricetype", "commodity", "price_transformed", "month"]
    assert list(applicant_features.columns) == expected_columns, "Some expected columns are missing from the applicant features."

def test_get_applicant_dummies():
    applicant_features = get_applicant_features()
    categorical_columns = get_categorical_columns(applicant_features)
    dummies_columns = []
    for col in categorical_columns:
        dummies_columns = dummies_columns + list(applicant_features[col].unique())
    
    applicant_dummies = get_applicant_dummies()

    assert Counter(applicant_features.select_dtypes(include=np.number).columns.tolist() + dummies_columns) == Counter(list(applicant_dummies.columns))

def test_get_selected_features():
    selected_features = get_selected_features()
    expected_columns = ['gasoline_price', 'diesel_price', 'usdmga', 'Alaotra Mangoro', 'Amoron I Mania', 'Analamanga', 'Analanjirofo', 'Androy', 'Anosy', 'Atsimo Andrefana', 'Atsimo Atsinanana', 'Atsinanana', 'Betsiboka', 'Boeny', 'Bongolava', 'Diana', 'Haute Matsiatra', 'Ihorombe', 'Itasy', 'Menabe', 'Sava', 'Sofia', 'Vakinankaratra', 'Vatovavy Fitovinany', 'Rice (imported)', 'Rice (local)', 'month_1', 'month_10', 'month_11', 'month_12', 'month_2', 'month_3', 'month_4', 'month_5', 'month_6', 'month_7', 'month_8', 'month_9', 'price_transformed']
    assert list(selected_features.columns) == expected_columns, "Some expected columns are missing from the selected features."
    assert selected_features.isnull().sum().sum() == 0, "There are missing values in the selected features."
    assert len(selected_features) > 0, "The selected features should contain at least one row of data."

def test_run_feature_engineering(tmp_path):
    destination = tmp_path / "feature_store"
    destination.mkdir()

    with patch("src.core.pipeline.feat_eng.get_feature_store_destination", return_value=str(destination)), \
        patch("src.core.pipeline.feat_eng.get_selected_features") as mock_selected:
        mock_selected.return_value = pd.DataFrame({
            'gasoline_price': [5200],
            'diesel_price': [5200],
            'usdmga': [0.2],
            'Alaotra Mangoro': [0],
            'Amoron I Mania': [0],
            'Analamanga': [0],
            'Analanjirofo': [0],
            'Androy': [0],
            'Anosy': [0],
            'Atsimo Andrefana': [0],
            'Atsimo Atsinanana': [0],
            'Atsinanana': [0],
            'Betsiboka': [0],
            'Boeny': [0],
            'Bongolava': [0],
            'Diana': [0],
            'Haute Matsiatra': [0],
            'Ihorombe': [0],
            'Itasy': [0],
            'Menabe': [0],
            'Sava': [0],
            'Sofia': [0],
            'Vakinankaratra': [0],
            'Vatovavy Fitovinany': [0],
            'Rice (imported)': [1],
            'Rice (local)': [0],
            'month_1': [1],
            'month_10': [0],
            'month_11': [0],
            'month_12': [0],
            'month_2': [1],
            'month_3': [1],
            'month_4': [1],
            'month_5': [1],
            'month_6': [1],
            'month_7': [1],
            'month_8': [1],
            'month_9': [1], 
            "price_transformed": [-1.25]
        })

        run_feature_engineering()

        expected_file = destination / "selected_features.csv"
        assert expected_file.exists(), "The selected features file was not created in the feature store destination."
        saved_data = pd.read_csv(expected_file)
        assert saved_data.equals(mock_selected.return_value), "The saved selected features do not match the expected data."