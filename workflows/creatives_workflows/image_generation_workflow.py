"""Image generation workflow."""

from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
from typing import Dict, Any

with workflow.unsafe.imports_passed_through():
    from activities.creative_activities import image_generation_activity


@workflow.defn(name="ImageGenerationWorkflow")
class ImageGenerationWorkflow:
    """Sub-workflow for image generation."""

    @workflow.run
    async def run(self, creative_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute image generation workflow."""
        workflow.logger.info("Starting ImageGenerationWorkflow")

        result = await workflow.execute_activity(
            image_generation_activity,
            creative_input,
            start_to_close_timeout=timedelta(minutes=10),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                initial_interval=timedelta(seconds=1),
            ),
        )

        return result

