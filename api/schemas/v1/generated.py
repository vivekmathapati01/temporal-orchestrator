"""Pydantic models for API requests and responses."""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class StartWorkflowRequest(BaseModel):
    """Request to start a new workflow."""

    workflow_type: str = Field(..., description="Workflow class name", example="MarketingOrchestratorWorkflow")
    workflow_id: str = Field(..., description="Unique workflow identifier", example="campaign-001")
    input: Dict[str, Any] = Field(..., description="Workflow input data")
    task_queue: Optional[str] = Field(None, description="Task queue name")


class StartWorkflowResponse(BaseModel):
    """Response after starting a workflow."""

    workflow_id: str
    run_id: str
    message: str = "Workflow started successfully"

