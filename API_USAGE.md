# FastAPI Workflow Starter - Usage Guide

## Quick Start

### 1. Start the API Server

```bash
# Using the run script
./scripts/run_api.sh

# Or directly with poetry
poetry run uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Access the API

- **API Docs (Swagger UI)**: http://localhost:8000/docs
- **Base URL**: http://localhost:8000
- **OpenAPI Spec**: http://localhost:8000/openapi.json

## API Endpoint

### POST /api/v1/workflows/start

Start a new Temporal workflow.

**Request Body:**

```json
{
  "workflow_type": "MarketingOrchestratorWorkflow",
  "workflow_id": "campaign-001",
  "input": {
    "campaign_id": "CAMP-001",
    "campaign_name": "Spring Launch",
    "budget": 100000,
    "objectives": ["Increase awareness"],
    "channels": ["email", "sms"]
  },
  "task_queue": "marketing-orchestrator-queue"
}
```

**Response:**

```json
{
  "workflow_id": "campaign-001",
  "run_id": "8303fc92-ee93-4739-8ddf-792d92b86393",
  "message": "Workflow started successfully"
}
```

## Example Usage

### Using curl

```bash
curl -X POST http://localhost:8000/api/v1/workflows/start \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_type": "MarketingOrchestratorWorkflow",
    "workflow_id": "campaign-001",
    "input": {
      "campaign_id": "CAMP-001",
      "campaign_name": "Spring Launch 2025",
      "target_audience": {
        "demographics": "Adults 25-45",
        "interests": ["technology", "innovation"],
        "location": "US, UK, CA"
      },
      "budget": 100000,
      "objectives": [
        "Increase brand awareness",
        "Drive product sales"
      ],
      "channels": ["email", "sms", "social"]
    }
  }'
```

### Using Python

```python
import requests

url = "http://localhost:8000/api/v1/workflows/start"
payload = {
    "workflow_type": "MarketingOrchestratorWorkflow",
    "workflow_id": "campaign-001",
    "input": {
        "campaign_id": "CAMP-001",
        "campaign_name": "Spring Launch 2025",
        "budget": 100000
    }
}

response = requests.post(url, json=payload)
print(response.json())
```

### Using the Test Script

```bash
poetry run python scripts/test_api.py
```

## Project Structure

```
api/
├── main.py                          # FastAPI application
├── endpoints/
│   └── v1/
│       └── routers/
│           ├── __init__.py
│           ├── router.py            # V1 route aggregator
│           └── workflow_router.py   # Workflow endpoints
└── schemas/
    └── v1/
        └── generated.py             # Pydantic models

services/
└── campaign_workflow.py             # Workflow service layer

config/
└── settings.py                      # Configuration

openapi/
└── v1/
    └── campaign_workflow_openapi_specs.yaml  # OpenAPI specification

scripts/
├── run_api.sh                       # Start API server
└── test_api.py                      # Test the API
```

## Configuration

Set environment variables or create a `.env` file:

```bash
# Temporal Configuration
TEMPORAL_HOST=localhost:7233
TEMPORAL_NAMESPACE=default
TEMPORAL_TASK_QUEUE=marketing-orchestrator-queue

# Logging
LOG_LEVEL=INFO
```

## Notes

- Ensure Temporal server is running before starting workflows
- The API connects to Temporal on startup
- Workflows are started asynchronously
- Use the Temporal UI to monitor workflows: http://localhost:8233

