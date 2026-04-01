from src.core.utils.helpers import download_file, get_cleaning_destination, load_config_file, get_data_sources, check_file_exist, get_ingestion_destination, get_categorical_columns, get_feature_store_destination, get_random_state, get_model_storage_location, delete_directory
import pandas as pd

def test_load_config_file():
    config = load_config_file("config/data_config.yaml")
    assert config["data_sources"][0]["format"] == "csv"

def test_get_data_sources():
    data_sources = get_data_sources()
    assert data_sources[0]["format"] == "csv"

def test_get_cleaning_destination():
    cleaning_destination = get_cleaning_destination()
    assert cleaning_destination == "data/data_warehouse"

def test_get_feature_store_destination():
    feature_store_destination = get_feature_store_destination()
    assert feature_store_destination == "data/feature_store"

def test_download_file(tmp_path):
    data_sources = get_data_sources()
    download_file(data_sources[0]["url"], data_sources[0]["name"], tmp_path)
    assert (tmp_path / data_sources[0]["name"]).exists()

def test_check_file_exist():
    assert check_file_exist("data_config.yaml", "config/")

def test_get_ingestion_destination():
    ingestion_destination = get_ingestion_destination()
    assert ingestion_destination == "data/data_lake"

def test_get_categorical_columns():
    df = pd.DataFrame({
        "numeric_col": [1, 2, 3],
        "categorical_col": ["A", "B", "C"],
        "mixed_col": [1, "B", 3]
    })
    categorical_columns = get_categorical_columns(df)
    assert categorical_columns == ["categorical_col", "mixed_col"]

def test_get_random_state():
    random_state = get_random_state()
    assert random_state == 42

def test_get_model_storage_location():
    model_storage_location = get_model_storage_location()
    assert model_storage_location == "model/"

def test_delete_directory(tmp_path):
    directory_to_delete = tmp_path / "test_directory"
    directory_to_delete.mkdir()
    (directory_to_delete / "subdir").mkdir()

    assert directory_to_delete.exists()

    delete_directory(tmp_path, "test_directory")

    assert not directory_to_delete.exists()