import pytest
from unittest.mock import patch, MagicMock, mock_open, call
from src.core.inference.RicePricePredictor import RicePricePredictor
from src.core.inference.schemas import InferenceInput, Region, Commodity, Month
from pathlib import Path
import numpy as np


@pytest.fixture
def mock_model():
    """Create a mock model for testing."""
    model = MagicMock()
    model.predict.return_value = np.array([3.5])
    return model


@pytest.fixture
def inference_input():
    """Create a valid InferenceInput for testing."""
    return InferenceInput(
        gasoline_price=1.5,
        diesel_price=1.2,
        usd_to_mga=4000.0,
        region=Region.Analamanga,
        commodity=Commodity.Rice_Local,
        month=Month.month_4
    )


class TestRicePricePredictorModelLoading:
    """Tests for model loading functionality."""

    def test_get_model_loads_from_correct_path(self, mock_model):
        """Test that get_model loads from the correct pickle file path."""
        RicePricePredictor._model = None  # fix: reset cache before test

        with patch('builtins.open', mock_open()) as mock_file:
            with patch('src.core.inference.RicePricePredictor.pickle.load', return_value=mock_model):  # fix: patch at usage site
                model = RicePricePredictor.get_model()
                assert model is not None
                # fix: actually verify the correct path is used
                mock_file.assert_called_once_with(
                    Path('artifacts/model/model_prod/model.pkl'), 'rb'
                )

    def test_get_model_caches_model(self, mock_model):
        """Test that get_model caches the model after first load."""
        RicePricePredictor._model = None

        with patch('builtins.open', mock_open()):
            with patch('src.core.inference.RicePricePredictor.pickle.load', return_value=mock_model) as mock_pickle:  # fix
                model1 = RicePricePredictor.get_model()
                model2 = RicePricePredictor.get_model()

                assert mock_pickle.call_count == 1
                assert model1 is model2


class TestRicePricePredictorPrediction:
    """Tests for prediction functionality."""

    def test_predict_returns_float(self, mock_model, inference_input):
        """Test that predict method returns a float."""
        RicePricePredictor._model = None

        with patch('builtins.open', mock_open()):
            with patch('src.core.inference.RicePricePredictor.pickle.load', return_value=mock_model):  # fix
                with patch('src.core.inference.RicePricePredictor.preprocess_input'):
                    with patch('src.core.inference.RicePricePredictor.post_process_result', return_value=1500.0):
                        predictor = RicePricePredictor()
                        result = predictor.predict(inference_input)
                        assert isinstance(result, (float, np.floating))

    def test_predict_calls_preprocess_input(self, mock_model, inference_input):
        """Test that predict calls preprocess_input with correct argument."""
        RicePricePredictor._model = None

        with patch('builtins.open', mock_open()):
            with patch('src.core.inference.RicePricePredictor.pickle.load', return_value=mock_model):  # fix
                with patch('src.core.inference.RicePricePredictor.preprocess_input') as mock_preprocess:
                    with patch('src.core.inference.RicePricePredictor.post_process_result', return_value=1500.0):
                        mock_preprocess.return_value = MagicMock()
                        predictor = RicePricePredictor()
                        predictor.predict(inference_input)
                        mock_preprocess.assert_called_once_with(inference_input)

    def test_predict_calls_model_predict(self, mock_model, inference_input):
        """Test that predict calls model.predict method."""
        RicePricePredictor._model = None

        with patch('builtins.open', mock_open()):
            with patch('src.core.inference.RicePricePredictor.pickle.load', return_value=mock_model):  # fix
                with patch('src.core.inference.RicePricePredictor.preprocess_input', return_value=MagicMock()):
                    with patch('src.core.inference.RicePricePredictor.post_process_result', return_value=1500.0):
                        predictor = RicePricePredictor()
                        predictor.predict(inference_input)
                        mock_model.predict.assert_called_once()

    def test_predict_calls_post_process_result(self, mock_model, inference_input):
        """Test that predict calls post_process_result with model output."""
        RicePricePredictor._model = None

        with patch('builtins.open', mock_open()):
            with patch('src.core.inference.RicePricePredictor.pickle.load', return_value=mock_model):  # fix
                with patch('src.core.inference.RicePricePredictor.preprocess_input', return_value=MagicMock()):
                    with patch('src.core.inference.RicePricePredictor.post_process_result') as mock_postprocess:
                        mock_postprocess.return_value = 1500.0
                        predictor = RicePricePredictor()
                        result = predictor.predict(inference_input)
                        mock_postprocess.assert_called_once()
                        assert result == 1500.0

    def test_predict_integration_flow(self, mock_model, inference_input):
        """Test the complete prediction flow."""
        RicePricePredictor._model = None

        with patch('builtins.open', mock_open()):
            with patch('src.core.inference.RicePricePredictor.pickle.load', return_value=mock_model):  # fix
                with patch('src.core.inference.RicePricePredictor.preprocess_input', return_value=MagicMock()) as mock_preprocess:
                    with patch('src.core.inference.RicePricePredictor.post_process_result', return_value=1500.0) as mock_postprocess:
                        predictor = RicePricePredictor()
                        result = predictor.predict(inference_input)

                        mock_preprocess.assert_called_once_with(inference_input)
                        mock_model.predict.assert_called_once()
                        mock_postprocess.assert_called_once()
                        assert result == 1500.0


class TestRicePricePredictorEdgeCases:
    """Tests for edge cases and error handling."""

    def test_predict_with_boundary_values(self, mock_model):
        """Test predict with minimum positive float values."""
        RicePricePredictor._model = None

        inference_input = InferenceInput(
            gasoline_price=0.01,
            diesel_price=0.01,
            usd_to_mga=0.01,
            region=Region.Diana,
            commodity=Commodity.Rice_Imported,
            month=Month.month_1
        )

        with patch('builtins.open', mock_open()):
            with patch('src.core.inference.RicePricePredictor.pickle.load', return_value=mock_model):  # fix
                with patch('src.core.inference.RicePricePredictor.preprocess_input', return_value=MagicMock()):
                    with patch('src.core.inference.RicePricePredictor.post_process_result', return_value=100.0):
                        predictor = RicePricePredictor()
                        result = predictor.predict(inference_input)
                        assert result == 100.0

    def test_predict_with_large_values(self, mock_model):
        """Test predict with large values."""
        RicePricePredictor._model = None

        inference_input = InferenceInput(
            gasoline_price=1000.0,
            diesel_price=1000.0,
            usd_to_mga=5000.0,
            region=Region.Sofia,
            commodity=Commodity.Rice_Local,
            month=Month.month_12
        )

        with patch('builtins.open', mock_open()):
            with patch('src.core.inference.RicePricePredictor.pickle.load', return_value=mock_model):  # fix
                with patch('src.core.inference.RicePricePredictor.preprocess_input', return_value=MagicMock()):
                    with patch('src.core.inference.RicePricePredictor.post_process_result', return_value=50000.0):
                        predictor = RicePricePredictor()
                        result = predictor.predict(inference_input)
                        assert result == 50000.0

    def test_multiple_predictor_instances_share_model(self, mock_model):
        """Test that multiple predictor instances share the cached model."""
        RicePricePredictor._model = None

        with patch('builtins.open', mock_open()):
            with patch('src.core.inference.RicePricePredictor.pickle.load', return_value=mock_model) as mock_pickle:  # fix
                predictor1 = RicePricePredictor()
                predictor2 = RicePricePredictor()

                model1 = predictor1.get_model()
                model2 = predictor2.get_model()

                assert mock_pickle.call_count == 1
                assert model1 is model2