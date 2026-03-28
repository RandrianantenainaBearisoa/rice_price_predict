#!/bin/bash

if [ ! -f .env ]; then
echo "Error : .env not found."
exit 1
fi

echo "Loading env variables..."

set -a
source .env
set +a

echo "Starting MLflow server on Postgres..."

uv run mlflow server \
--backend-store-uri "$MLFLOW_DATABASE_URL" \
--default-artifact-root "$MLFLOW_ARTIFACT_ROOT" \
--host 0.0.0.0 \
--port 5000