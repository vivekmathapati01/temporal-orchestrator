"""Service layer for workflow operations."""

import logging
import uuid
from typing import Dict, Optional
from temporalio.client import Client
from client.temporal_client import get_temporal_client
from config.settings import settings

logger = logging.getLogger(__name__)


class WorkflowService:
    """Service for managing workflows."""

    def __init__(self):
        self._client: Optional[Client] = None

    async def get_client(self) -> Client:
        """Get Temporal client."""
        if self._client is None:
            self._client = await get_temporal_client()
        return self._client

    def _generate_workflow_id(self, campaign_name: str) -> str:
        normalized_name = campaign_name.replace(" ", "-").lower()
        short_uuid = str(uuid.uuid4())[:8]
        return f"{normalized_name}-{short_uuid}"

    async def start_workflow(self, request) -> Dict[str, str]:
        client = await self.get_client()
        workflow_id = self._generate_workflow_id(request.campaign_name)
        workflow_type = "MarketingOrchestratorWorkflow"
        task_queue = settings.temporal_task_queue

        # Build workflow input
        workflow_input = {
            "campaign_name": request.campaign_name,
            "budget": request.budget,
            "objectives": request.objectives,
            "channels": request.channels,
        }

        logger.info(f"Starting workflow: {workflow_type} with ID: {workflow_id}")
        logger.info(f"Campaign: {request.campaign_name}, Budget: {request.budget}")
        logger.info(f"Task queue: {task_queue}")

        handle = await client.start_workflow(
            workflow_type,
            workflow_input,
            id=workflow_id,
            task_queue=task_queue,
        )

        logger.info(f"Workflow started: {workflow_id}, run_id: {handle.result_run_id}")

        return {
            "workflow_id": handle.id,
            "run_id": handle.result_run_id,
        }

    async def send_signal(self, workflow_id: str, signal_name: str, signal_input=None) -> Dict[str, str]:
        client = await self.get_client()

        logger.info(f"Sending signal '{signal_name}' to workflow: {workflow_id}")
        if signal_input is not None:
            logger.info(f"Signal input: {signal_input}")

        # Get workflow handle
        handle = client.get_workflow_handle(workflow_id)

        # Send the signal
        await handle.signal(signal_name, signal_input)

        logger.info(f"Signal '{signal_name}' sent successfully to workflow: {workflow_id}")

        return {
            "workflow_id": workflow_id,
            "signal_name": signal_name,
        }

    async def list_workflows(
        self,
        limit: int = 10,
        workflow_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> dict:
        client = await self.get_client()

        # Enforce maximum limit
        limit = min(limit, 100)

        logger.info(f"Listing workflows with limit: {limit}, type: {workflow_type}, status: {status}")

        # Build query filter
        query_parts = []

        if workflow_type:
            query_parts.append(f"WorkflowType='{workflow_type}'")

        if status:
            query_parts.append(f"ExecutionStatus='{status}'")

        query = " AND ".join(query_parts) if query_parts else ""

        workflows = []

        # List workflow executions with filters
        async for workflow in client.list_workflows(query):
            if len(workflows) >= limit:
                break

            workflow_info = {
                "workflow_id": workflow.id,
                "run_id": workflow.run_id,
                "workflow_type": workflow.workflow_type,
                "status": workflow.status.name,
                "start_time": workflow.start_time.isoformat() if workflow.start_time else None,
            }
            workflows.append(workflow_info)

        logger.info(f"Retrieved {len(workflows)} workflows")

        return {
            "workflows": workflows,
            "count": len(workflows),
        }

    async def get_workflow_status(self, workflow_id: str) -> dict:
        client = await self.get_client()

        logger.info(f"Getting status for workflow: {workflow_id}")

        # Get workflow handle
        handle = client.get_workflow_handle(workflow_id)

        # Describe the workflow to get its details
        description = await handle.describe()

        logger.info(f"Workflow {workflow_id} status: {description.status.name}")

        # Convert description to a serializable dictionary
        description_dict = {
            "run_id": description.run_id,
            "workflow_type": description.workflow_type,
            "status": description.status.name,
            "start_time": description.start_time.isoformat() if description.start_time else None,
            "close_time": description.close_time.isoformat() if description.close_time else None,
            "execution_time": str(description.close_time - description.start_time) if description.close_time and description.start_time else None,
            "task_queue": description.task_queue,
            "history_length": description.history_length if hasattr(description, 'history_length') else None,
        }

        # Return the entire description as a dict
        return {
            "workflow_id": workflow_id,
            "description": description_dict,
        }


# Global service instance
workflow_service = WorkflowService()

