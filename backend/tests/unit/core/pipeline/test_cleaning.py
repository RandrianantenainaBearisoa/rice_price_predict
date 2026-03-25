import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch, MagicMock
from src.core.pipeline.cleaning import process_fuel_prices, process_rice_prices, process_world_market_prices, run_data_preparing

# --- TESTS FOR FUEL PRICES ---

@patch("pandas.read_excel") # This decorator replaces the read_excel function with a fake object for the duration of the test
def test_process_fuel_prices(mock_read_excel): # the @patch deco effect is applied to the function by this argument
    # 1. Fake excel data simulating the structure of the fuel price sheets
    date_cols = [datetime(2024, 1, 1), datetime(2024, 2, 1)]
    fake_data = pd.DataFrame({
        "Country": ["Madagascar"],
        "Diesel (LCU/liter)": ["Madagascar"],
        "Kerosene (LCU/liter)": ["Madagascar"],
        date_cols[0]: [5000],
        date_cols[1]: [5200]
    })

    # Here , we specify that whenever read_excel is called, it should return the fake exvel data created above.
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

# --- TESTS FOR WORLD BANK COMMODITY PRICE : process_world_market_prices
def test_process_world_market_prices():

    result = process_world_market_prices()

    # assertions
    assert isinstance(result, pd.DataFrame)
    assert [str(dtyp) for dtyp in result.dtypes.to_list()] == ['datetime64[us]', 'float64', 'float64', 'float64', 'float64', 'float64']
    assert int(result.isnull().sum().sum()) == 0

# --- TEST FOR run_data_preparing ---
    
def test_run_data_preparing(tmp_path):
    # 1. Create a temporary output directory
    output_dir = tmp_path / "data_warehouse"
    output_dir.mkdir()

    # 2. Mock the internal functions to avoid actual file I/O and data processing
    # Note : We patch the functions in the cleaning module, not preparing, since they are defined there
    with patch("src.core.pipeline.cleaning.process_fuel_prices") as mock_fuel, \
         patch("src.core.pipeline.cleaning.process_rice_prices") as mock_rice, \
         patch("src.core.pipeline.cleaning.process_world_market_prices") as mock_fert, \
         patch("src.core.pipeline.cleaning.get_cleaning_destination", return_value=str(output_dir)):
        
        # Fake return data
        mock_fuel.return_value = pd.DataFrame({
            "date": pd.to_datetime(["2024-01-01"]), 
            "gasoline_price": [5200],
            "diesel_price": [5200],
            "kerosene_price": [5200]
        })
        
        mock_rice.return_value = pd.DataFrame({
            'date': pd.to_datetime(["2024-01-01"]),
            'admin1': ["Admin1"],
            'admin2': ["admin2"],
            'market': ["market"],
            'market_id': [75],
            'latitude': [-12],
            'longitude': [20],
            'category': ["Cereal"],
            'commodity': ["Rice"],
            'commodity_id': [12],
            'unit': ["KG"],
            'priceflag': ["priceflag"],
            'pricetype': ["pricetype"],
            'currency': ["MGA"],
            'price': [2300],
            'usdprice': [0.2]
       })
        
        mock_fert.return_value = pd.DataFrame({
            "date": pd.to_datetime(["2024-01-01"]),
            'Phosphate rock': [55], 
            'DAP': [55], 
            'TSP': [55], 
            'Urea': [55], 
            'Potassium chloride': [55]
        })

        # Execute the function
        run_data_preparing()

        # 3. Assertions to check if the output file is created
        expected_file = output_dir / "mdg_rice_data.csv"
        assert expected_file.exists()

        result = pd.read_csv(expected_file)

        print(result.columns)
        
        # 4. Check if all the needed columns are there
        expectected_cols = ['date', 'admin1', 'admin2', 'market', 'market_id', 'latitude',
            'longitude', 'category', 'commodity', 'commodity_id', 'unit',
            'priceflag', 'pricetype', 'currency', 'price', 'usdprice',
            'gasoline_price', 'diesel_price', 'kerosene_price', 'Phosphate rock', 'DAP', 'TSP', 'Urea', 'Potassium chloride']
        assert result.columns.to_list() == expectected_cols