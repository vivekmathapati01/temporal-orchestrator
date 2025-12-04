"""Pydantic models for API requests and responses."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any


class StartWorkflowRequest(BaseModel):
    """Request to start a new workflow."""

    campaign_name: str = Field(..., description="Name of the marketing campaign")
    budget: float = Field(..., description="Campaign budget", examples=[100000])
    objectives: List[str] = Field(..., description="Campaign objectives", examples=[["Increase awareness"]])
    channels: List[str] = Field(..., description="Marketing channels", examples=[["email", "sms"]])


class StartWorkflowResponse(BaseModel):
    """Response after starting a workflow."""

    workflow_id: str
    run_id: str
    message: str = "Workflow started successfully"


class SignalWorkflowRequest(BaseModel):
    """Request to send a signal to a running workflow."""

    workflow_id: str = Field(..., description="Workflow ID to send signal to")
    signal_name: str = Field(..., description="Name of the signal", examples=["approve_research", "reject_research", "provide_feedback"])
    signal_input: Optional[Any] = Field(None, description="Optional input data for the signal")


class SignalWorkflowResponse(BaseModel):
    """Response after sending a signal to a workflow."""

    workflow_id: str
    signal_name: str
    message: str = "Signal sent successfully"


class WorkflowInfo(BaseModel):
    """Information about a workflow execution."""

    workflow_id: str
    run_id: str
    workflow_type: str
    status: str
    start_time: Optional[str] = None


class GetWorkflowsResponse(BaseModel):
    """Response containing list of workflows."""

    workflows: List[WorkflowInfo]
    count: int
    message: str = "Workflows retrieved successfully"


class WorkflowStatusResponse(BaseModel):
    """Response containing workflow status details."""

    workflow_id: str
    description: Any
    message: str = "Workflow status retrieved successfully"

    model_config = {"arbitrary_types_allowed": True}


