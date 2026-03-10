from src.core.utils.helpers import get_data_sources, download_file, check_file_exist, get_ingestion_destination
from pathlib import Path

def run_data_ingestion(replace: bool = True):
    """
    Runs the data ingestion process by downloading the data sources specified in the config file.
    Args:
        replace (bool = True): whether to replace the file if it already exists in the data lake.
    Returns:
        None
    """
    destination = get_ingestion_destination()
    data_sources = get_data_sources()
    for source in data_sources:
        do_we_download = False
        if replace:
            do_we_download = True
        else:
            if not check_file_exist(source["name"], destination):
                do_we_download = True

        if do_we_download:
            download_file(source["url"], source["name"], Path(destination))