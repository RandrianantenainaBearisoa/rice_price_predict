import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch, MagicMock
from src.core.pipeline.cleaning import process_fuel_prices, process_rice_prices, run_data_preparing

# --- TESTS FOR FUEL PRICES ---

@patch("pandas.read_excel")
def test_process_fuel_prices(mock_read_excel):
    # 1. Fake excel data simulating the structure of the fuel price sheets
    date_cols = [datetime(2024, 1, 1), datetime(2024, 2, 1)]
    fake_data = pd.DataFrame({
        "Country": ["Madagascar"],
        "Diesel (LCU/liter)": ["Madagascar"],
        "Kerosene (LCU/liter)": ["Madagascar"],
        date_cols[0]: [5000],
        date_cols[1]: [5200]
    })

    # Simulate the read_excel function to return the same fake data for all sheets
    mock_read_excel.return_value = fake_data

    # 2. Call the function
    result = process_fuel_prices()

    # 3. Assertions
    assert isinstance(result, pd.DataFrame)
    assert "gasoline_price" in result.columns
    assert len(result) == 2
    assert not result.isnull().values.any()

# --- TESTS FOR RICE PRICES ---

@patch("pandas.read_csv")
def test_process_rice_prices(mock_read_csv):
    # 1. Fake CSV data simulating the structure of the rice price data
    fake_rice = pd.DataFrame({
        "commodity": ["Rice (local)", "Maize", "Rice (imported)"],
        "date": ["2024-01-01", "2024-01-01", "2024-02-01"],
        "price": [2500, 1200, 2800]
    })
    mock_read_csv.return_value = fake_rice

    # 2. Call the function with test dates
    result = process_rice_prices(start_date="2024-01-01", end_date="2024-02-01")

    # 3. Assertions
    assert len(result) == 2 # The Maize should be filtered out
    assert all(result["commodity"].str.contains("Rice"))

# --- TEST FOR run_data_preparing ---

def test_run_data_preparing(tmp_path):
    # 1. Create a temporary output directory
    output_dir = tmp_path / "data_warehouse"
    output_dir.mkdir()

    # 2. Mock the internal functions to avoid actual file I/O and data processing
    with patch("src.core.pipeline.cleaning.process_fuel_prices") as mock_fuel, \
         patch("src.core.pipeline.cleaning.process_rice_prices") as mock_rice, \
         patch("src.core.pipeline.cleaning.get_cleaning_destination", return_value=str(output_dir)):
        
        # Fake return data
        mock_fuel.return_value = pd.DataFrame({"date": ["2024-01-01"], "gasoline_price": [5000]})
        mock_rice.return_value = pd.DataFrame({"date": ["2024-01-01"], "price": [2500]})

        # Execute the function
        run_data_preparing()

        # 3. Assertions to check if the output files are created
        assert (output_dir / "mdg_fuel_data.csv").exists()
        assert (output_dir / "mdg_rice_price.csv").exists()