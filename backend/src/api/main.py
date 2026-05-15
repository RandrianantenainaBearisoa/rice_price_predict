import os
import uuid
import logging
import json
import traceback
import math
from pydantic import ValidationError
from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.core.inference.schemas import InferenceInput
from src.core.inference.RicePricePredictor import RicePricePredictor
from src.core.inference.WrappedException import WrappedException


app = FastAPI()

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = RicePricePredictor()

# Basic configuration to see output in console
logging.basicConfig(level=logging.INFO, format='\n%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@app.get("/features")
async def get_features(request: Request):
    id = str(uuid.uuid4())
    try:
        features = InferenceInput.model_json_schema()
        log_data = {
            "request_id": request.headers.get('x-request-id', id),
            "features_returned": features
        }
        logging.info(json.dumps(log_data))
        return features
    except Exception as e:
        log_data = {
            "request_id": request.headers.get('x-request-id', id),
            "error": e.__str__()
        }
        logging.error(json.dumps(log_data))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=e.__str__()
        )

async def log_validation_error(request: Request):
    id = str(uuid.uuid4())
    raw_input = await request.json()
    try:
        yield
    except ValidationError as e:
        log_data = {
            "request_id": request.headers.get('x-request-id', id),
            "input_data": raw_input,
            "error": e.__str__()
        }
        logging.error(json.dumps(log_data))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=e.__str__()
        )

@app.post('/predict', dependencies=[Depends(log_validation_error)])
async def predict(request: Request, entry: InferenceInput):
    id = str(uuid.uuid4())
    request_id = request.headers.get('x-request-id', id),
    try:
        raw_input = await request.json()
        predictor = RicePricePredictor()
        prediction, featurized, y_pred = predictor.predict(entry=entry)

        log_data = {
            "request_id": request_id,
            "raw_input": raw_input,
            "validated_input": entry.dict(),
            "featurized_input": featurized.to_dict() if featurized is not None else None,
            "y_predicted": y_pred if y_pred is not None else None,
            "final_prediction": prediction,
        }
        logging.info(json.dumps(log_data))
        if math.isnan(prediction):
            raise ValueError("Predicted value is NaN, which indicates an issue with the model or input data.")
        return prediction
    except WrappedException as e:
        log_data = {
            "request_id": request_id,
            "raw_input": raw_input,
            "validated_input": entry.dict(),
            "error_location": e.exception_location() if e.exception_location() else None,
            "arguments": e.entry() if e.entry() else None,
            "cause": type(e.__cause__).__name__ if e.__cause__ else None,
            "context": type(e.__context__).__name__ if e.__context__ else None,
            "traceback": traceback.format_exc(),
        }
        logging.error(json.dumps(log_data))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.__str__()
        )
    except ValueError as e:
        log_data['error'] = e.__str__()
        logging.error(json.dumps(log_data))
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        log_data = {
            "request_id": request_id,
            "raw_input": raw_input,
            "validated_input": entry.dict(),
            "error": e.__str__(),
            "traceback": traceback.format_exc(),
        }
        logging.error(json.dumps(log_data))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )