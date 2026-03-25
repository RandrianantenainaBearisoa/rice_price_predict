#!/bin/bash

# 1. Vérification du fichier .env
if [ ! -f .env ]; then
echo "Erreur : Le fichier .env est introuvable."
exit 1
fi

echo "Chargement des variables d'environnement..."

# 2.
# On "source" le fichier .env pour que le terminal connaisse les variables.
# 'set -a' exporte automatiquement toutes les variables lues.
set -a
source .env
set +a

echo "Démarrage du serveur MLflow sur Postgres..."

# 3. Maintenant, les variables comme $MLFLOW_DATABASE_URL existent pour le Shell
uv run mlflow server \
--backend-store-uri "$MLFLOW_DATABASE_URL" \
--default-artifact-root "$MLFLOW_ARTIFACT_ROOT" \
--host 0.0.0.0 \
--port 5000