"""Media buying workflow."""

from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
from typing import Dict, Any

with workflow.unsafe.imports_passed_through():
    from activities.golive_activities import media_buying_activity


@workflow.defn(name="MediaBuyingWorkflow")
class MediaBuyingWorkflow:
    """Sub-workflow for media buying."""

    @workflow.run
    async def run(self, media_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute media buying workflow."""
        workflow.logger.info("Starting MediaBuyingWorkflow")

        result = await workflow.execute_activity(
            media_buying_activity,
            media_plan,
            start_to_close_timeout=timedelta(minutes=10),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                initial_interval=timedelta(seconds=1),
            ),
        )

        return result

