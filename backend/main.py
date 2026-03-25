import requests
from src.core.pipeline.ingestion import run_data_ingestion
from src.core.pipeline.cleaning import run_data_preparing

run_data_ingestion(replace=False)
run_data_preparing()