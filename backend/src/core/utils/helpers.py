import requests
from pathlib import Path
import yaml
from src.core.utils.TerminalSpinner import TerminalSpinner

def download_file(url: str, filename: str, destination: str) -> None:
    """
    Downloads a file and places it in the specified folder.
    Args:
        url (str): download url
        filename (str): name of the file in the destination
        destination (str): destination folder in the project
    Returns:
        None
    Raises:
        HTTPError: if there is an error regarding the download source.
    """
    with TerminalSpinner(f"Downloading {filename}"):
        destination.mkdir(parents=True, exist_ok=True)
        
        response = requests.get(url)
        response.raise_for_status()
        
        with open(destination / filename, "wb") as f:
            f.write(response.content)

PROJECT_ROOT = Path(__file__).resolve().parents[3]

def load_config_file(filename: str) -> dict:
    """
    Load the yaml file from the project root.
    Args:
        filename (str): Name of the yaml file to load
    Returns:
        dict: dictionary containing the informations in the yaml file
    Raises:
        FileNotFoundError: if the specified yaml file is not found in the config folder
    """
    config_path = PROJECT_ROOT / filename
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found in : {config_path}")
        
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)
    
def get_data_sources() -> list:
    """
    Returns the list of data sources
    Returns:
        list: list of data sources
    """
    return load_config_file("config/data_config.yaml")["data_sources"]

def get_ingestion_destination() -> str:
    """
    Returns the data destination for the ingestion process
    Returns:
        str: data destination for the ingestion process
    """
    return load_config_file("config/data_config.yaml")["data_destination"]["ingestion"]

def get_cleaning_destination() -> str:
    """
    Returns the data destination for the cleaning process
    Returns:
        str: data destination for the cleaning process
    """
    return load_config_file("config/data_config.yaml")["data_destination"]["cleaning"]

def get_feature_store_destination() -> str:
    """
    Returns the data destination for the feature store
    Returns:
        str: data destination for the feature store
    """
    return load_config_file("config/data_config.yaml")["data_destination"]["feature_store"]

def check_file_exist(file_name: str, folder: str) -> bool:
    """
    Check if a file exists in the specified folder
    Args:
        file_name (str): name of the file to check (exp: data.csv)
        folder (str): where you want to check for the existence of the file
    Returns:
        bool : True if the file exists
    """
    file_path = Path(folder)/file_name
    return file_path.exists()

def get_categorical_columns(df):
    """Return the list of categorical columns in the DataFrame."""
    return df.select_dtypes(include=["object", "category"]).columns.tolist()