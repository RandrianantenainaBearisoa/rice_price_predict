from src.core.utils.helpers import download_file, get_cleaning_destination, load_config_file, get_data_sources, check_file_exist, get_ingestion_destination

def test_load_config_file():
    config = load_config_file("config/data_config.yaml")
    assert config["data_sources"][0]["format"] == "csv"

def test_get_data_sources():
    data_sources = get_data_sources()
    assert data_sources[0]["format"] == "csv"

def test_get_cleaning_destination():
    cleaning_destination = get_cleaning_destination()
    assert cleaning_destination == "data/data_warehouse"

def test_download_file(tmp_path):
    data_sources = get_data_sources()
    download_file(data_sources[0]["url"], data_sources[0]["name"], tmp_path)
    assert (tmp_path / data_sources[0]["name"]).exists()

def test_check_file_exist():
    assert check_file_exist("data_config.yaml", "config/")

def test_get_ingestion_destination():
    ingestion_destination = get_ingestion_destination()
    assert ingestion_destination == "data/data_lake"