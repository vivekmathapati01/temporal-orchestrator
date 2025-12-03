#!/bin/bash
# Script to run the FastAPI server

echo "Starting Temporal Workflow API..."
cd "$(dirname "$0")/.."
poetry run uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

