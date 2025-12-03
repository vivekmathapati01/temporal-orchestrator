"""Service layer for workflow operations."""

import logging
from typing import Dict, Any, Optional
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

    async def start_workflow(
        self,
        workflow_type: str,
        workflow_id: str,
        workflow_input: Dict[str, Any],
        task_queue: Optional[str] = None,
    ) -> Dict[str, str]:
        """Start a new workflow."""
        client = await self.get_client()
        queue = task_queue or settings.temporal_task_queue

        logger.info(f"Starting workflow: {workflow_type} with ID: {workflow_id}")

        handle = await client.start_workflow(
            workflow_type,
            workflow_input,
            id=workflow_id,
            task_queue=queue,
        )

        logger.info(f"Workflow started: {workflow_id}, run_id: {handle.result_run_id}")

        return {
            "workflow_id": handle.id,
            "run_id": handle.result_run_id,
        }


# Global service instance
workflow_service = WorkflowService()

