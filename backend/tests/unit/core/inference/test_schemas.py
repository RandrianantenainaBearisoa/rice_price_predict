import pytest
from src.core.inference.schemas import InferenceInput
from pydantic import ValidationError

def test_inference_input_schema():
    input_ok = {
        "gasoline_price": 5200.0,
        "diesel_price": 5200.0,
        "usd_to_mga": 0.2,
        "region": "Alaotra Mangoro",
        "commodity": "Rice_Local",
        "month": "month_1"
    }
    obj_ok = InferenceInput(**input_ok)
    assert obj_ok.region == 'Alaotra Mangoro'
    assert obj_ok.commodity.value['value'] == 'Rice_Local'
    assert obj_ok.month.value['labels']['fr'] == 'Janvier'
    
    with pytest.raises(ValidationError) as invalid:
        input_ko = {
            "gasoline_price": -5200.0,
            "diesel_price": 5200.0,
            "usd_to_mga": 0.2,
            "region": "Alaotra Mangoro",
            "commodity": "Rice Local",
            "month": "month_1"
        }
        obj_ok = InferenceInput(**input_ko)

    errorlist = invalid.value.errors()
    assert errorlist[0]["type"] == "greater_than" and errorlist[0]["loc"][0] == "gasoline_price"
    assert errorlist[1]["type"] == "enum" and errorlist[1]["loc"][0] == "commodity"