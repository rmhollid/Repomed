#!/usr/bin/env bash
set -euo pipefail

: "${GOOGLE_CLOUD_PROJECT:?Set GOOGLE_CLOUD_PROJECT first.}"
: "${GEMINI_API_KEY:?Set GEMINI_API_KEY first.}"

REGION="${REGION:-us-central1}"
SERVICE="${SERVICE:-repomedic}"

gcloud config set project "$GOOGLE_CLOUD_PROJECT"

gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com

gcloud run deploy "$SERVICE" \
  --source . \
  --region "$REGION" \
  --allow-unauthenticated \
  --set-env-vars "GEMINI_API_KEY=$GEMINI_API_KEY,GEMINI_MODEL=gemini-3.5-flash"

echo
echo "Deployment complete."
gcloud run services describe "$SERVICE" \
  --region "$REGION" \
  --format='value(status.url)'
