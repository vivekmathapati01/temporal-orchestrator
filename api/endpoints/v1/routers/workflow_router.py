"""Workflow router."""

import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Path
from api.schemas.v1.generated import (
    StartWorkflowRequest,
    StartWorkflowResponse,
    SignalWorkflowRequest,
    SignalWorkflowResponse,
    GetWorkflowsResponse,
    WorkflowStatusResponse
)
from services.campaign_workflow import workflow_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/workflows", tags=["Workflows"])


@router.post("/start", response_model=StartWorkflowResponse)
async def start_workflow(request: StartWorkflowRequest):
    """Start a new workflow."""
    try:
        result = await workflow_service.start_workflow(request)
        return StartWorkflowResponse(**result)
    except Exception as e:
        logger.error(f"Error starting workflow: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/signal", response_model=SignalWorkflowResponse)
async def signal_workflow(request: SignalWorkflowRequest):
    """Send a signal to a running workflow."""
    try:
        result = await workflow_service.send_signal(
            workflow_id=request.workflow_id,
            signal_name=request.signal_name,
            signal_input=request.signal_input
        )
        return SignalWorkflowResponse(**result)
    except Exception as e:
        logger.error(f"Error sending signal: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=GetWorkflowsResponse)
async def get_workflows(
    limit: int = Query(default=10, ge=1, le=100, description="Maximum number of workflows to return"),
    workflow_type: Optional[str] = Query(default=None, description="Filter by workflow type (e.g., 'MarketingOrchestratorWorkflow')"),
    status: Optional[str] = Query(default=None, description="Filter by workflow status (e.g., 'Running', 'Completed')")
):
    """Get list of workflows with optional filters."""
    try:
        result = await workflow_service.list_workflows(
            limit=limit,
            workflow_type=workflow_type,
            status=status
        )
        return GetWorkflowsResponse(**result)
    except Exception as e:
        logger.error(f"Error listing workflows: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{workflow_id}", response_model=WorkflowStatusResponse)
async def get_workflow_status(
    workflow_id: str = Path(..., description="ID of the workflow to get status for")
):
    """Get status of a specific workflow."""
    try:
        result = await workflow_service.get_workflow_status(workflow_id)
        return WorkflowStatusResponse(**result)
    except Exception as e:
        logger.error(f"Error getting workflow status: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))



