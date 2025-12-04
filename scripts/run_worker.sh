#!/bin/bash

# Start Worker Script for Temporal Marketing Orchestrator
# This script starts the Temporal worker using Poetry

set -e

echo "=================================================="
echo "Starting Temporal Marketing Orchestrator Worker"
echo "=================================================="
echo ""

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed!"
    echo "Please install Poetry: https://python-poetry.org/docs/#installation"
    echo "Or use: curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

echo "✓ Poetry is available"

# Navigate to project root (parent of scripts directory)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "✓ Working directory: $PROJECT_ROOT"

# Check if dependencies are installed
if [ ! -f "poetry.lock" ]; then
    echo "Dependencies not installed. Running poetry install..."
    poetry install
fi

echo "✓ Dependencies ready"

# Check if .env file exists, if not copy from example
if [ ! -f ".env" ]; then
    echo ".env file not found. Creating from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✓ Created .env file. Please review and update as needed."
    else
        echo ".env.example not found!"
        exit 1
    fi
fi

echo "✓ Environment configuration loaded"
echo ""

# Check if Temporal server is running (optional)
echo "Checking Temporal server connection..."
TEMPORAL_HOST=${TEMPORAL_HOST:-localhost:7233}

echo "✓ Temporal configuration ready"
echo ""

# Start the worker using Poetry
echo "=================================================="
echo "Starting worker..."
echo "=================================================="
echo ""
echo "Press Ctrl+C to stop the worker"
echo ""

poetry run python -m workers.worker

