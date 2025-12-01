"""SMS generation workflow."""

from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
from typing import Dict, Any

with workflow.unsafe.imports_passed_through():
    from activities.creative_activities import sms_generation_activity


@workflow.defn(name="SMSGenerationWorkflow")
class SMSGenerationWorkflow:
    """Sub-workflow for SMS generation."""

    @workflow.run
    async def run(self, creative_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute SMS generation workflow."""
        workflow.logger.info("Starting SMSGenerationWorkflow")

        result = await workflow.execute_activity(
            sms_generation_activity,
            creative_input,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                maximum_attempts=1,
                initial_interval=timedelta(seconds=1),
            ),
        )

        return result

