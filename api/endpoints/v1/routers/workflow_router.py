"""Workflow router."""

import logging
from fastapi import APIRouter, HTTPException
from api.schemas.v1.generated import StartWorkflowRequest, StartWorkflowResponse
from services.campaign_workflow import workflow_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/workflows", tags=["Workflows"])


@router.post("/start", response_model=StartWorkflowResponse)
async def start_workflow(request: StartWorkflowRequest):
    """Start a new workflow."""
    try:
        result = await workflow_service.start_workflow(
            workflow_type=request.workflow_type,
            workflow_id=request.workflow_id,
            workflow_input=request.input,
            task_queue=request.task_queue,
        )
        return StartWorkflowResponse(**result)
    except Exception as e:
        logger.error(f"Error starting workflow: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

