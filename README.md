# Temporal Marketing Orchestrator

A production-grade Temporal workflow system for orchestrating marketing campaigns with human-in-the-loop approvals at each stage.

## 🏗️ Architecture

This project implements a hierarchical workflow structure with the following components:

### Main Orchestrator Workflow
- **MarketingOrchestratorWorkflow** - Parent workflow coordinating all campaign stages

### Child Workflows

#### 1. ResearcherWorkflow
Handles campaign research and concept development with the following sub-workflows:
- ResearchBriefWorkflow
- ResearchConceptNoteWorkflow
- **Human approval**: `approve_research` / `reject_research`

#### 2. CreativeWorkflow
Manages creative asset generation with parallel sub-workflows:
- SMSGenerationWorkflow
- ImageGenerationWorkflow
- VideoGenerationWorkflow
- EmailTemplateWorkflow
- **Human approval**: `approve_creatives` / `reject_creatives`

#### 3. GoLiveWorkflow
Orchestrates media buying and deployment:
- MediaBuyingWorkflow
- DeploymentWorkflow
- **Human approval**: `approve_media_buy` / `reject_media_buy`

#### 4. MeasurementsWorkflow
Handles campaign measurement and analysis:
- PollMeasurementsWorkflow
- RetrievalWorkflow
- **Human approval**: `approve_measurements` / `reject_measurements`

## 📋 Prerequisites

- Python 3.10 or higher
- **Poetry** (dependency management)
- Temporal server (local or remote)

## 🚀 Quick Start

### 1. Install Poetry (if not already installed)

```bash
# macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -

# Or using Homebrew (macOS)
brew install poetry

# Or using pipx
pipx install poetry
```

### 2. Install Temporal Server

```bash
# Using Homebrew (macOS)
brew install temporal

# Start local Temporal server
temporal server start-dev
```

The Temporal Web UI will be available at: http://localhost:8233

### 3. Install Project Dependencies

```bash
# Navigate to project directory
cd /Users/vivek/PycharmProjects/aiplatform/temporal-orchestrator

# Install all dependencies using Poetry
poetry install
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env if needed (default values work for local development)
```

### 5. Start the Worker

Using the provided script (recommended):
```bash
chmod +x scripts/start_worker.sh
./scripts/start_worker.sh
```

Or directly with Poetry:
```bash
poetry run python -m workers.worker
```

### 6. Start a Campaign

In a new terminal window:

```bash
# Start a campaign using Poetry
poetry run python scripts/start_campaign.py
```

### 7. Approve Workflow Stages

The workflow will wait for approval at each stage. 

#### Option A: Using Temporal UI (Recommended for Production)

1. Open Temporal UI: http://localhost:8233
2. Navigate to Workflows → Find your workflow (e.g., `marketing-campaign-CAMP-2025-001-researcher`)
3. Click the "Signal" button
4. Enter signal name: `approve_research` (or `approve_creatives`, `approve_media_buy`, `approve_measurements`)
5. Enter feedback (optional): `"Looks good!"`
6. Click "Send Signal"

#### Option B: Using CLI Script (Development/Testing Only)

```bash
# Approve research stage
poetry run python dev_tools/approve_workflow.py CAMP-2025-001 research "Looks good!"

# Approve creative stage
poetry run python dev_tools/approve_workflow.py CAMP-2025-001 creative "Great work!"

# Approve media buy stage
poetry run python dev_tools/approve_workflow.py CAMP-2025-001 media_buy "Approved!"

# Approve measurements stage
poetry run python dev_tools/approve_workflow.py CAMP-2025-001 measurements "Perfect!"

# Or approve all stages at once (for testing)
poetry run python dev_tools/approve_workflow.py CAMP-2025-001 all
```

⚠️ **Note**: The CLI scripts in `dev_tools/` are for local development only. In production, use the Temporal UI or build a custom web application for user interactions.

#### Option C: Using Temporal CLI

```bash
# Approve research
temporal workflow signal \
  --workflow-id marketing-campaign-CAMP-2025-001-researcher \
  --name approve_research \
  --input '"Approved!"'

# Approve creative
temporal workflow signal \
  --workflow-id marketing-campaign-CAMP-2025-001-creative \
  --name approve_creatives \
  --input '"Approved!"'

# Approve media buy
temporal workflow signal \
  --workflow-id marketing-campaign-CAMP-2025-001-golive \
  --name approve_media_buy \
  --input '"Approved!"'

# Approve measurements
temporal workflow signal \
  --workflow-id marketing-campaign-CAMP-2025-001-measurements \
  --name approve_measurements \
  --input '"Approved!"'
```

## 📁 Project Structure

```
temporal-orchestrator/
├── .env.example              # Environment configuration template
├── .gitignore               # Git ignore file
├── pyproject.toml           # Poetry configuration and dependencies
├── README.md                # This file
├── config/                  # 📌 PRODUCTION
│   ├── __init__.py
│   └── settings.py          # Application settings
├── workflows/               # 📌 PRODUCTION - Core business logic
│   ├── __init__.py
│   ├── orchestrator_workflow.py    # Main parent workflow
│   ├── researcher_workflow.py      # Research workflows
│   ├── creative_workflow.py        # Creative workflows
│   ├── golive_workflow.py         # GoLive workflows
│   └── measurements_workflow.py    # Measurements workflows
├── activities/              # 📌 PRODUCTION - Task implementations
│   ├── __init__.py
│   ├── researcher_activities.py    # Research activities
│   ├── creative_activities.py      # Creative activities
│   ├── golive_activities.py       # GoLive activities
│   └── measurements_activities.py  # Measurements activities
├── workers/                 # 📌 PRODUCTION - Worker process
│   ├── __init__.py
│   └── worker.py            # Worker implementation
├── scripts/                 # 📌 PRODUCTION - Operational scripts
│   ├── __init__.py
│   └── start_worker.sh      # Start the worker process
└── dev_tools/               # 🔧 DEVELOPMENT ONLY - Not for production
    ├── README.md            # Dev tools documentation
    ├── approve_workflow.py  # CLI tool to send approval signals (dev only)
    └── start_campaign.py    # CLI tool to start test campaigns (dev only)
```

### Production vs Development Files

**Production Files** (📌):
- `config/`, `workflows/`, `activities/`, `workers/` - Core application code
- `scripts/start_worker.sh` - Worker startup script
- Deploy these to production

**Development Files** (🔧):  
- `dev_tools/` - CLI tools for local testing
- Use during development, **NOT** in production
- In production, use Temporal UI or build a proper web application
│   ├── creative_activities.py      # Creative activities
│   ├── golive_activities.py       # GoLive activities
│   └── measurements_activities.py  # Measurements activities
├── workers/
│   ├── __init__.py
│   └── worker.py            # Worker implementation
└── scripts/
    ├── __init__.py
    ├── start_worker.sh      # Shell script to start worker
    ├── start_campaign.py    # Script to start a campaign
    └── approve_workflow.py  # Script to approve workflow stages
```

## 🎯 Features

- ✅ **Production-grade code** with proper error handling and logging
- ✅ **Hierarchical workflow structure** with parent and child workflows
- ✅ **Human-in-the-loop approvals** at each major stage
- ✅ **Parallel execution** of creative generation tasks
- ✅ **Retry policies** for fault tolerance
- ✅ **Type hints** throughout the codebase
- ✅ **Configurable settings** via environment variables
- ✅ **Helper scripts** for common operations
- ✅ **Comprehensive logging** for debugging and monitoring

## 🔧 Configuration

Edit `.env` file to configure:

```bash
# Temporal Server
TEMPORAL_HOST=localhost:7233
TEMPORAL_NAMESPACE=default
TEMPORAL_TASK_QUEUE=marketing-orchestrator-queue

# Logging
LOG_LEVEL=INFO

# Application
APP_NAME=marketing-orchestrator
APP_VERSION=0.1.0
```

## 📊 Monitoring

Monitor workflows in the Temporal Web UI:
- Local: http://localhost:8233
- Navigate to your namespace (default: `default`)
- Find workflows by ID: `marketing-campaign-{campaign_id}`

## 🧪 Development

### Adding New Activities

1. Create activity function in appropriate `activities/*.py` file
2. Add `@activity.defn` decorator
3. Register in `activities/__init__.py`
4. Register in `workers/worker.py`

### Adding New Workflows

1. Create workflow class in appropriate `workflows/*.py` file
2. Add `@workflow.defn` decorator
3. Register in `workflows/__init__.py`
4. Register in `workers/worker.py`

### Code Quality

```bash
# Format code
poetry run black .

# Type checking
poetry run mypy .

# Run tests (when added)
poetry run pytest
```

## 📝 Notes

- All activities currently print "hello" messages for demonstration
- Implement actual business logic in activity functions as needed
- Adjust timeouts and retry policies based on your requirements
- Use Temporal queries to check workflow state without waiting for completion

## 🤝 Contributing

1. Follow existing code structure and patterns
2. Add type hints to all functions
3. Include docstrings for classes and functions
4. Update README for significant changes

## 📄 License

This project is provided as-is for demonstration purposes.

## 🆘 Troubleshooting

### Worker won't start
- Ensure Temporal server is running: `temporal server start-dev`
- Check `.env` configuration matches your Temporal server

### Workflow stuck at approval
- Send approval signal using CLI or Web UI
- Check workflow ID is correct
- Verify signal name matches workflow definition

### Activities failing
- Check worker logs for errors
- Verify activity is registered in worker
- Check timeout configurations

## 📚 Additional Resources

- [Temporal Documentation](https://docs.temporal.io/)
- [Temporal Python SDK](https://github.com/temporalio/sdk-python)
- [Temporal Samples](https://github.com/temporalio/samples-python)

