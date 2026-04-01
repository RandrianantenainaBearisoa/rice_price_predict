import mlflow
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from datetime import datetime
from sklearn.base import clone
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_validate, KFold
from src.core.utils.helpers import get_random_state

def mean_scores(scores_lists):
    scores_lists = pd.DataFrame(scores_lists)
    scores_lists[['mse', 'train_mse', 'mae', 'train_mae']] = scores_lists[['test_neg_mean_squared_error', 'train_neg_mean_squared_error', 'test_neg_mean_absolute_error', 'train_neg_mean_absolute_error']].abs()
    scores_lists["rmse"] = np.sqrt(scores_lists["test_neg_mean_squared_error"].abs())
    scores_lists["train_rmse"] = np.sqrt(scores_lists["train_neg_mean_squared_error"].abs())
    return scores_lists.mean().to_dict()

def run_training():
    print("Starting model training...")

    try:
        load_dotenv()
        mlflow.set_tracking_uri("http://localhost:5000")
        mlflow.set_experiment("rice_price_product_experiments")

        random_state = get_random_state()
        alpha_value = 1.0
        target = "price_transformed"
        dataset = pd.read_csv("data/feature_store/selected_features.csv")
        features = dataset.columns.drop(target)
        metrics = ['r2', 'neg_mean_squared_error', 'neg_mean_absolute_error']
        params = {"alpha": alpha_value, "random_state": random_state}

        with mlflow.start_run(run_name=f"Final_Models_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}") as parent_run:
            X = dataset[list(features)]
            y = dataset[target]

            model = Ridge(alpha=alpha_value)
            KFcv = KFold(n_splits=5, shuffle=True, random_state=random_state)

            scores = cross_validate(model, X, y, scoring=metrics, cv=KFcv, return_train_score=True, return_estimator=True)
            run_list = []
            for i in range(len(scores["estimator"])):
                scores_df = pd.DataFrame(scores)
                scores_df = scores_df[['fit_time', 'score_time', 'test_r2', 'train_r2',
                    'test_neg_mean_squared_error', 'train_neg_mean_squared_error',
                    'test_neg_mean_absolute_error', 'train_neg_mean_absolute_error']].iloc[i].to_dict()
                selected_model_scores = {key: [value]for key, value in scores_df.items()}
                with mlflow.start_run(run_name=f"Final_Model_{i}", nested=True) as run:
                    mlflow.log_metrics(mean_scores(selected_model_scores))
                    mlflow.log_params(params=params)
                    mlflow.set_tag("features", ", ".join(list(X.columns)))
                    mlflow.sklearn.log_model(scores["estimator"][i], f"model_Ridge_{i}")
                    run_list.append(run.info.run_id)
            best_model_idx = scores['test_r2'].argmax()
            with mlflow.start_run(run_name=f"Final_Model_for_PROD", nested=True) as run:
                final_model = scores["estimator"][best_model_idx]
                mlflow.sklearn.log_model(final_model, "model_Ridge")
                mlflow.set_tag("features", ", ".join(list(features)))
                mlflow.set_tag("trained_on", "full_dataset")
                mlflow.set_tag("original_run_id", run_list[best_model_idx])
                mlflow.log_params(params)
        print("✅ Model training completed successfully.")
    except Exception as e:
        print(f"💥 Error occurred during model training: {e}")
