"""Research concept note workflow."""

from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
from typing import Dict, Any

with workflow.unsafe.imports_passed_through():
    from activities.researcher_activities import research_concept_note_activity


@workflow.defn(name="ResearchConceptNoteWorkflow")
class ResearchConceptNoteWorkflow:
    """Sub-workflow for generating research concept note."""

    @workflow.run
    async def run(self, brief_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute research concept note workflow."""
        workflow.logger.info("Starting ResearchConceptNoteWorkflow")

        result = await workflow.execute_activity(
            research_concept_note_activity,
            brief_data,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                initial_interval=timedelta(seconds=1),
            ),
        )
        return result

