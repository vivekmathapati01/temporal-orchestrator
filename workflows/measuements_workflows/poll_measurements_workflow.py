"""Poll measurements workflow."""

from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
from typing import Dict, Any

with workflow.unsafe.imports_passed_through():
    from activities.measurements_activities import poll_measurements_activity


@workflow.defn(name="PollMeasurementsWorkflow")
class PollMeasurementsWorkflow:
    """Sub-workflow for polling measurements."""

    @workflow.run
    async def run(self, deployment_id: str) -> Dict[str, Any]:
        """Execute poll measurements workflow."""
        workflow.logger.info("Starting PollMeasurementsWorkflow")

        result = await workflow.execute_activity(
            poll_measurements_activity,
            deployment_id,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                initial_interval=timedelta(seconds=1),
            ),
        )

        return result

