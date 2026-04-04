from src.core.inference.preprocessing import preprocess_input
from src.core.inference.postprocessing import post_process_result
from src.core.inference.schemas import InferenceInput
from pathlib import Path
import pickle


class RicePricePredictor():
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            path = Path('artifacts/model/model_prod/model.pkl')
            with open(path, 'rb') as f:
                cls._model = pickle.load(f)
        return cls._model
    
    def predict(self, entry: InferenceInput):
        model = self.get_model()
        X = preprocess_input(entry)
        y_pred = model.predict(X)
        predicted_price = post_process_result(y_pred)
        return predicted_price