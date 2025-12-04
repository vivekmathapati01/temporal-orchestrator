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

## API Endpoints

### GET /api/v1/workflows/{workflow_id}

Get detailed status of a specific workflow.

**Path Parameters:**
- `workflow_id` (required): ID of the workflow to get status for

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/workflows/spring-launch-1e13946d"
```

**Response:**

```json
{
  "workflow_id": "spring-launch-1e13946d",
  "run_id": "8303fc92-ee93-4739-8ddf-792d92b86393",
  "workflow_type": "MarketingOrchestratorWorkflow",
  "status": "RUNNING",
  "start_time": "2025-12-05T10:30:00Z",
  "close_time": null,
  "execution_time": null,
  "message": "Workflow status retrieved successfully"
}
```

**For Completed Workflow:**
```json
{
  "workflow_id": "summer-sale-a3f5b21c",
  "run_id": "7192eb81-de82-3628-7cce-681c81a75282",
  "workflow_type": "MarketingOrchestratorWorkflow",
  "status": "COMPLETED",
  "start_time": "2025-12-04T15:20:00Z",
  "close_time": "2025-12-04T17:35:00Z",
  "execution_time": "2:15:00",
  "message": "Workflow status retrieved successfully"
}
```

### GET /api/v1/workflows

Get list of workflows with optional filters.

**Query Parameters:**
- `limit` (optional): Maximum number of workflows to return (default: 10, max: 100)
- `workflow_type` (optional): Filter by workflow type (e.g., "MarketingOrchestratorWorkflow")
- `status` (optional): Filter by workflow status (e.g., "Running", "Completed")

**Example Request:**
```bash
# Get all workflows with default limit
curl -X GET "http://localhost:8000/api/v1/workflows"

# Get 20 workflows
curl -X GET "http://localhost:8000/api/v1/workflows?limit=20"

# Filter by workflow type
curl -X GET "http://localhost:8000/api/v1/workflows?workflow_type=MarketingOrchestratorWorkflow"

# Filter by status
curl -X GET "http://localhost:8000/api/v1/workflows?status=Running"

# Combine filters
curl -X GET "http://localhost:8000/api/v1/workflows?limit=50&workflow_type=MarketingOrchestratorWorkflow&status=Completed"
```

**Response:**

```json
{
  "workflows": [
    {
      "workflow_id": "spring-launch-1e13946d",
      "run_id": "8303fc92-ee93-4739-8ddf-792d92b86393",
      "workflow_type": "MarketingOrchestratorWorkflow",
      "status": "RUNNING",
      "start_time": "2025-12-05T10:30:00Z"
    },
    {
      "workflow_id": "summer-sale-a3f5b21c",
      "run_id": "7192eb81-de82-3628-7cce-681c81a75282",
      "workflow_type": "MarketingOrchestratorWorkflow",
      "status": "COMPLETED",
      "start_time": "2025-12-04T15:20:00Z"
    }
  ],
  "count": 2,
  "message": "Workflows retrieved successfully"
}
```

**Workflow Status Values:**
- `RUNNING` - Workflow is currently executing
- `COMPLETED` - Workflow finished successfully
- `FAILED` - Workflow failed with an error
- `CANCELED` - Workflow was canceled
- `TERMINATED` - Workflow was terminated
- `CONTINUED_AS_NEW` - Workflow continued as new execution
- `TIMED_OUT` - Workflow timed out

### POST /api/v1/workflows/start

Start a new marketing campaign workflow.

**Request Body:**

```json
{
  "campaign_name": "Spring Launch",
  "budget": 100000,
  "objectives": ["Increase awareness"],
  "channels": ["email", "sms"]
}
```

**Response:**

```json
{
  "workflow_id": "spring-launch-1e13946d",
  "run_id": "8303fc92-ee93-4739-8ddf-792d92b86393",
  "message": "Workflow started successfully"
}
```

### POST /api/v1/workflows/signal

Send a signal to a running workflow (for approvals, rejections, or feedback).

**Request Body:**

```json
{
  "workflow_id": "spring-launch-1e13946d-researcher",
  "signal_name": "approve_research",
  "signal_input": "Research looks good!"
}
```

**Available Signals:**
- `approve_research` - Approve the research phase
- `reject_research` - Reject the research phase
- `approve_creatives` - Approve the creative phase
- `reject_creatives` - Reject the creative phase
- `approve_media_buy` - Approve the media buying phase
- `reject_media_buy` - Reject the media buying phase
- `approve_measurements` - Approve the measurements phase
- `reject_measurements` - Reject the measurements phase
- `provide_feedback` - Provide feedback (can be used in any phase)

**Response:**

```json
{
  "workflow_id": "spring-launch-1e13946d-researcher",
  "signal_name": "approve_research",
  "message": "Signal sent successfully"
}
```

## Example Usage

### Listing Workflows

#### Using curl

```bash
# Get default 10 workflows
curl -X GET http://localhost:8000/api/v1/workflows

# Get 20 workflows
curl -X GET "http://localhost:8000/api/v1/workflows?limit=20"

# Get maximum 100 workflows
curl -X GET "http://localhost:8000/api/v1/workflows?limit=100"
```

#### Using Python

```python
import requests

# Get default 10 workflows
url = "http://localhost:8000/api/v1/workflows"
response = requests.get(url)
result = response.json()

print(f"Total workflows: {result['count']}")
for workflow in result['workflows']:
    print(f"ID: {workflow['workflow_id']}, Status: {workflow['status']}")

# Get 50 workflows
response = requests.get(url, params={"limit": 50})
result = response.json()
print(f"Retrieved {result['count']} workflows")
```

### Getting Workflow Status

#### Using curl

```bash
# Get status of a specific workflow
curl -X GET http://localhost:8000/api/v1/workflows/spring-launch-1e13946d
```

#### Using Python

```python
import requests

workflow_id = "spring-launch-1e13946d"
url = f"http://localhost:8000/api/v1/workflows/{workflow_id}"
response = requests.get(url)
result = response.json()

print(f"Workflow: {result['workflow_id']}")
print(f"Status: {result['status']}")
print(f"Started: {result['start_time']}")
if result['close_time']:
    print(f"Completed: {result['close_time']}")
    print(f"Execution Time: {result['execution_time']}")
```

### Starting a Campaign

#### Using curl

```bash
curl -X POST http://localhost:8000/api/v1/workflows/start \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_name": "Spring Launch",
    "budget": 100000,
    "objectives": ["Increase awareness", "Drive sales"],
    "channels": ["email", "sms", "social"]
  }'
```

#### Using Python

```python
import requests

url = "http://localhost:8000/api/v1/workflows/start"
payload = {
    "campaign_name": "Spring Launch",
    "budget": 100000,
    "objectives": ["Increase awareness"],
    "channels": ["email", "sms"]
}

response = requests.post(url, json=payload)
result = response.json()
print(f"Workflow ID: {result['workflow_id']}")
```

### Sending Signals

#### Approve Research Phase

```bash
curl -X POST http://localhost:8000/api/v1/workflows/signal \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": "spring-launch-1e13946d-researcher",
    "signal_name": "approve_research",
    "signal_input": "Research looks excellent!"
  }'
```

#### Reject Creatives with Feedback

```bash
curl -X POST http://localhost:8000/api/v1/workflows/signal \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": "spring-launch-1e13946d-creative",
    "signal_name": "reject_creatives",
    "signal_input": "Please use more vibrant colors and update the messaging"
  }'
```

#### Provide Feedback

```bash
curl -X POST http://localhost:8000/api/v1/workflows/signal \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": "spring-launch-1e13946d-golive",
    "signal_name": "provide_feedback",
    "signal_input": "Consider targeting younger demographics"
  }'
```

#### Using Python

```python
import requests

# Approve research
signal_url = "http://localhost:8000/api/v1/workflows/signal"
signal_payload = {
    "workflow_id": "spring-launch-1e13946d-researcher",
    "signal_name": "approve_research",
    "signal_input": "Approved!"
}

response = requests.post(signal_url, json=signal_payload)
print(response.json())
```

## Workflow Lifecycle

1. **Start Workflow** - Creates a new marketing campaign workflow
2. **Research Phase** - Wait for approval/rejection signal
3. **Creative Phase** - Wait for approval/rejection signal  
4. **GoLive Phase** - Wait for approval/rejection signal
5. **Measurements Phase** - Wait for approval/rejection signal
6. **Complete** - Campaign workflow finishes

At each phase, you can:
- **Approve** - Move to the next phase
- **Reject** - Retry the current phase
- **Provide Feedback** - Send feedback without approving/rejecting

## Notes

- Workflow IDs are auto-generated from campaign name + UUID
- Child workflow IDs follow pattern: `{parent-workflow-id}-{phase}` (e.g., `spring-launch-1e13946d-researcher`)
- Signals must be sent to the correct child workflow ID for each phase
- Signal input is optional but recommended for providing context

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

