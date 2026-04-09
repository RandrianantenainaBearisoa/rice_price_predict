import requests
from src.core.pipeline.ingestion import run_data_ingestion
from src.core.pipeline.cleaning import run_data_preparing
from src.core.pipeline.feat_eng import run_feature_engineering
from src.core.pipeline.training import run_training

run_data_ingestion(replace=False)
run_data_preparing()
run_feature_engineering()
run_training()