import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from src.core.inference.postprocessing import post_process_result


class MockBoxCoxTransformer:
    """Mock Box-Cox transformer for testing."""
    def inverse_transform(self, val):
        # Simple mock: multiply by 2 for testing purposes
        return val * 2


def test_post_process_result_returns_float():
    """Test that post_process_result returns a numeric value."""
    mock_transformer = MockBoxCoxTransformer()
    
    with patch('src.core.inference.postprocessing.joblib.load', return_value=mock_transformer):
        result = post_process_result(5.0)
        assert isinstance(result, (float, np.floating, int))


def test_post_process_result_transforms_value():
    """Test that post_process_result correctly applies inverse transformation."""
    mock_transformer = MockBoxCoxTransformer()
    
    with patch('src.core.inference.postprocessing.joblib.load', return_value=mock_transformer):
        input_val = 5.0
        result = post_process_result(input_val)
        # Mock transformer multiplies by 2, so 5.0 * 2 = 10.0
        assert result == 10.0


def test_post_process_result_with_integer_input():
    """Test that post_process_result handles integer input."""
    mock_transformer = MockBoxCoxTransformer()
    
    with patch('src.core.inference.postprocessing.joblib.load', return_value=mock_transformer):
        result = post_process_result(3)
        assert isinstance(result, (float, np.floating, int))
        assert result == 6


def test_post_process_result_with_small_value():
    """Test that post_process_result handles small values."""
    mock_transformer = MockBoxCoxTransformer()
    
    with patch('src.core.inference.postprocessing.joblib.load', return_value=mock_transformer):
        result = post_process_result(0.1)
        assert result == 0.2


def test_post_process_result_loads_correct_file():
    """Test that post_process_result loads the correct joblib file."""
    mock_transformer = MockBoxCoxTransformer()
    
    with patch('src.core.inference.postprocessing.joblib.load', return_value=mock_transformer) as mock_load:
        post_process_result(1.0)
        mock_load.assert_called_once_with('./artifacts/transformation/box_cox/box_cox.joblib')


def test_post_process_result_reshapes_input():
    """Test that post_process_result reshapes input correctly."""
    mock_transformer = MagicMock()
    mock_transformer.inverse_transform.return_value = np.array([[10.0]])
    
    with patch('src.core.inference.postprocessing.joblib.load', return_value=mock_transformer):
        result = post_process_result(5.0)
        
        # Verify inverse_transform was called with reshaped array
        mock_transformer.inverse_transform.assert_called_once()
        call_args = mock_transformer.inverse_transform.call_args[0][0]
        assert call_args.shape == (1, 1)
