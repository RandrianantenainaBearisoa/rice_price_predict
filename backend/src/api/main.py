from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.inference.schemas import InferenceInput
from src.core.inference.RicePricePredictor import RicePricePredictor

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = RicePricePredictor()

@app.get("/features")
async def root():
    return InferenceInput.model_json_schema()

@app.post('/predict')
async def predict(entry: InferenceInput):
    predictor = RicePricePredictor()
    prediction = predictor.predict(entry=entry)
    return prediction