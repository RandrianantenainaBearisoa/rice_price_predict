import pytest
from pathlib import Path
from unittest.mock import patch
from src.core.pipeline.ingestion import run_data_ingestion, get_data_sources

# This fixture will be executed before each test to set up a temporary environment for testing 
@pytest.fixture
def mock_env(tmp_path):
    # 1. Create a temporary directory to act as the ingestion destination
    temp_destination = tmp_path / "data_lake"
    temp_destination.mkdir()

    # 2. Prepare the list of expected file paths
    expected_files = [temp_destination / source['name'] for source in get_data_sources()]

    # 3. Use 'patch' to make 'get_ingestion_destination' return our temporary directory
    with patch("src.core.pipeline.ingestion.get_ingestion_destination", return_value=str(temp_destination)):
        yield expected_files
    
def test_run_data_ingestion(mock_env): # the patch is applied through the fixture (fixture is passed as an argument, defined above)
    expected_files = mock_env
    run_data_ingestion()
    
    # 3. Assertions to check if the expected files have been created
    assert all(f.exists() for f in expected_files)

def test_run_data_ingestion_with_replace(mock_env):
    expected_files = mock_env
    run_data_ingestion(replace=True)
    
    assert all(f.exists() for f in expected_files)

def test_run_data_ingestion_without_replace(mock_env):
    expected_files = mock_env
    run_data_ingestion(replace=False)
    
    assert all(f.exists() for f in expected_files)