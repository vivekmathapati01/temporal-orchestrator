"""Deployment workflow."""

from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
from typing import Dict, Any

with workflow.unsafe.imports_passed_through():
    from activities.golive_activities import deployment_activity


@workflow.defn(name="DeploymentWorkflow")
class DeploymentWorkflow:
    """Sub-workflow for campaign deployment."""

    @workflow.run
    async def run(self, deployment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute deployment workflow."""
        workflow.logger.info("Starting DeploymentWorkflow")

        result = await workflow.execute_activity(
            deployment_activity,
            deployment_data,
            start_to_close_timeout=timedelta(minutes=10),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                initial_interval=timedelta(seconds=1),
            ),
        )

        return result

