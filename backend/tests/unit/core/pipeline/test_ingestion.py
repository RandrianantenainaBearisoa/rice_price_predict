from src.core.pipeline.ingestion import run_data_ingestion
from src.core.utils.helpers import get_data_sources, get_ingestion_destination
from pathlib import Path

destination = get_ingestion_destination()
sources = [Path(destination)/file_name['name'] for file_name in get_data_sources()]

def test_run_data_ingestion():
    run_data_ingestion()
    assert all([file_path.exists() for file_path in sources])

def test_run_data_ingestion_with_replace():
    run_data_ingestion(replace=True)
    assert all([file_path.exists() for file_path in sources])

def test_run_data_ingestion_without_replace():
    run_data_ingestion(replace=False)
    assert all([file_path.exists() for file_path in sources])