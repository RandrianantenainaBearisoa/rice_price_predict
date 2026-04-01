from src.core.pipeline.training import mean_scores, run_training, store_model_in_project, get_best_model
from unittest.mock import patch, MagicMock
import pandas as pd

def test_mean_scores():
    scores_lists = {
        'test_neg_mean_squared_error': [-1, -16, -49],
        'train_neg_mean_squared_error': [-1, -16, -49],
        'test_neg_mean_absolute_error': [-1, -4, -16],
        'train_neg_mean_absolute_error': [-1, -4, -16],
    }
    expected_output = {
        'test_neg_mean_squared_error': -22.0,
        'train_neg_mean_squared_error': -22.0,
        'test_neg_mean_absolute_error': -7.0,
        'train_neg_mean_absolute_error': -7.0,
        'mse': 22.0,
        'train_mse': 22.0,
        'mae': 7.0,
        'train_mae': 7.0,
        'rmse': 4.0,
        'train_rmse': 4.0
        }

    result = mean_scores(scores_lists)

    assert isinstance(result, dict)
    assert mean_scores(scores_lists) == expected_output

def test_store_model_in_project():
    with patch('src.core.pipeline.training.download_artifacts') as mock_download,\
        patch('src.core.pipeline.training.get_model_storage_location') as mock_get_location:
        location = "model/"
        mock_get_location.return_value = location
        store_model_in_project("test_run_id", "test_artifact_path")
        mock_download.assert_called_once_with(run_id="test_run_id", artifact_path="test_artifact_path", dst_path=location)

def test_get_best_model():
    scores = {
        'fit_time': [0.2, 5, 4],
        'score_time': [0.2, 5, 4],
        'test_r2': [-1, 5, 6],
        'train_r2':[-1, 5, 6],
        'test_neg_mean_squared_error': [-1, -16, -49],
        'train_neg_mean_squared_error': [-1, -16, -49],
        'test_neg_mean_absolute_error': [-1, -4, -16],
        'train_neg_mean_absolute_error': [-1, -4, -16],
        'estimator': ["model_0", "model_1", "model_2"]
    }

    best_model_scores, best_model, best_model_idx = get_best_model(scores)

    assert isinstance(best_model_scores, dict)
    assert all(isinstance(value, list) for value in best_model_scores.values())
    assert scores['estimator'][best_model_idx] == best_model

def test_run_training():
    with patch('src.core.pipeline.training.get_random_state') as mock_rand, \
        patch('src.core.pipeline.training.pd.read_csv') as mock_readcsv, \
        patch('src.core.pipeline.training.cross_validate') as mock_cv, \
        patch('src.core.pipeline.training.mean_scores') as mock_mean_score, \
        patch('src.core.pipeline.training.clone') as mock_clone, \
        patch('src.core.pipeline.training.mlflow') as mock_mlflow:
        
        mock_rand.return_value = 42
        
        mock_readcsv.return_value = pd.DataFrame({
            'champ1': [4, 2],
            'champ2': [4, 2],
            'price_transformed': [2, 5]
        })

        mock_cv.return_value = {
            'fit_time': [0.2, 5, 4],
            'score_time': [0.2, 5, 4],
            'test_r2': [-1, 5, 6],
            'train_r2':[-1, 5, 6],
            'test_neg_mean_squared_error': [-1, -16, -49],
            'train_neg_mean_squared_error': [-1, -16, -49],
            'test_neg_mean_absolute_error': [-1, -4, -16],
            'train_neg_mean_absolute_error': [-1, -4, -16],
            'estimator': [MagicMock(), MagicMock(), MagicMock()]
        }

        mock_mean_score.return_value = {
            'fit_time': 0.2,
            'score_time': 0.2,
            'test_r2': 6,
            'train_r2': 6,
            'test_neg_mean_squared_error': -22.0,
            'train_neg_mean_squared_error': -22.0,
            'test_neg_mean_absolute_error': -7.0,
            'train_neg_mean_absolute_error': -7.0,
            'mse': 22.0,
            'train_mse': 22.0,
            'mae': 7.0,
            'train_mae': 7.0,
            'rmse': 4.0,
            'train_rmse': 4.0,
        }

        mock_clone.return_value = MagicMock()

        mock_run = MagicMock()
        mock_mlflow.start_run.return_value.__enter__.return_value = mock_run

        run_training()

        mock_readcsv.assert_called_once_with('data/feature_store/selected_features.csv')
        assert mock_mlflow.start_run.called
        assert mock_mlflow.log_metrics.called
        assert mock_mlflow.log_params.called
        assert mock_mlflow.sklearn.log_model.called