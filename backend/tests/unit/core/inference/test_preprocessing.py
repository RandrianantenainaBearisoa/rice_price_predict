from src.core.inference.preprocessing import selection_to_dummies, preprocess_input
from src.core.inference.schemas import InferenceInput
import pandas as pd

def test_selection_to_dummies():
    selected = "toto"
    categories = ["tata", "toto", "tyty"]
    expected_return = [0, 1, 0]
    given_return = selection_to_dummies(selected=selected, options=categories)
    assert expected_return == given_return

def test_preprocess_input():
    mock_input = InferenceInput(
      **{ "gasoline_price": 5200.0,
        "diesel_price": 5200.0,
        "usd_to_mga": 0.2,
        "region": "Vatovavy_Fitovinany",
        "commodity": "Rice_Local",
        "month": "month_1"}
    )

    result_df = preprocess_input(mock_input)

    assert isinstance(result_df, pd.DataFrame)
    assert result_df.shape == (1, 38)

    assert result_df.iloc[0]['gasoline_price'] == 5200.0
    assert result_df.iloc[0]['diesel_price'] == 5200.0
    assert result_df.iloc[0]['usdmga'] == 0.2

    assert result_df.iloc[0]['Vatovavy Fitovinany'] == 1
    assert result_df.iloc[0]['Vakinankaratra'] == 0
    assert result_df.iloc[0]['Rice (local)'] == 1
    assert result_df.iloc[0]['Rice (imported)'] == 0

    assert result_df.iloc[0]['month_1'] == 1
    assert result_df.iloc[0]['month_2'] == 0