import requests
from src.core.utils.helpers import get_data_sources, download_file, check_file_exist, get_ingestion_destination
from pathlib import Path

def data_ingestion_logic(replace: bool = True):
    """
    The logic begind the function run_data_ingestion()
    """
    destination = get_ingestion_destination()
    data_sources = get_data_sources()
    print(f"Starting data ingestion process to {destination}...")
    for source in data_sources:
        do_we_download = False
        if replace:
            do_we_download = True
        else:
            if not check_file_exist(source["name"], destination):
                do_we_download = True
            else:
                print(f"✅ {source['name']} already exists in {destination}. Skipping download.")

        if do_we_download:
            download_file(source["url"], source["name"], Path(destination))

def run_data_ingestion(replace: bool = True):
    """
    Runs the data ingestion process by downloading the data sources specified in the config file.
    Args:
        replace (bool = True): whether to replace the file if it already exists in the data lake.
    Returns:
        None
    """
    try:
        data_ingestion_logic(replace)
        print("✅ Data ingestion process completed successfully.")
    except requests.exceptions.ConnectionError:
        print("🌐 Network error: Check your internet connection or the source URL.")
    except Exception as e:
        print(f"💥 An unexpected error occurred: {e}")