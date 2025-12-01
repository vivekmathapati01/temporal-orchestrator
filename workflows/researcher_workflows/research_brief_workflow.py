"""Research brief workflow."""

from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
from typing import Dict, Any

with workflow.unsafe.imports_passed_through():
    from activities.researcher_activities import research_brief_activity


@workflow.defn(name="ResearchBriefWorkflow")
class ResearchBriefWorkflow:
    """Sub-workflow for generating research brief."""

    @workflow.run
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute research brief workflow."""
        workflow.logger.info("Starting ResearchBriefWorkflow")

        result = await workflow.execute_activity(
            research_brief_activity,
            input_data,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                initial_interval=timedelta(seconds=1),
            ),
        )
        return result

