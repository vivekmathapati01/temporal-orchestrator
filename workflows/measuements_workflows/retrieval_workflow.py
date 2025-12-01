"""Retrieval workflow."""

from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
from typing import Dict, Any

with workflow.unsafe.imports_passed_through():
    from activities.measurements_activities import retrieval_activity


@workflow.defn(name="RetrievalWorkflow")
class RetrievalWorkflow:
    """Sub-workflow for retrieving measurements."""

    @workflow.run
    async def run(self, measurement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute retrieval workflow."""
        workflow.logger.info("Starting RetrievalWorkflow")

        result = await workflow.execute_activity(
            retrieval_activity,
            measurement_data,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                initial_interval=timedelta(seconds=1),
            ),
        )

        return result

