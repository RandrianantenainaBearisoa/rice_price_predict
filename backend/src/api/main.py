from fastapi import FastAPI
from src.core.inference.schemas import InferenceInput
from src.core.inference.RicePricePredictor import RicePricePredictor

app = FastAPI()
predictor = RicePricePredictor()

@app.get("/features")
async def root():
    return InferenceInput.model_json_schema()

@app.post('/predict')
async def predict(entry: InferenceInput):
    predictor = RicePricePredictor()
    prediction = predictor.predict(entry=entry)
    return prediction