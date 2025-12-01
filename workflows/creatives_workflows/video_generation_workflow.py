"""Video generation workflow."""

from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
from typing import Dict, Any

with workflow.unsafe.imports_passed_through():
    from activities.creative_activities import video_generation_activity


@workflow.defn(name="VideoGenerationWorkflow")
class VideoGenerationWorkflow:
    """Sub-workflow for video generation."""

    @workflow.run
    async def run(self, creative_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute video generation workflow."""
        workflow.logger.info("Starting VideoGenerationWorkflow")

        result = await workflow.execute_activity(
            video_generation_activity,
            creative_input,
            start_to_close_timeout=timedelta(minutes=15),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                initial_interval=timedelta(seconds=1),
            ),
        )

        return result

