"""Main researcher workflow."""

from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
from typing import Dict, Any
from dataclasses import dataclass
with workflow.unsafe.imports_passed_through():
    from activities.researcher_activities import (
        compile_research_input_activity,
        summarise_research_findings_activity,
    )
    from workflows.researcher_workflows.research_brief_workflow import ResearchBriefWorkflow
    from workflows.researcher_workflows.research_concept_note_workflow import ResearchConceptNoteWorkflow


@workflow.defn(name="ResearcherWorkflow")
class ResearcherWorkflow:
    """Main researcher workflow with human-in-the-loop approval."""

    def __init__(self) -> None:
        self.approval_status: str = "pending"
        self.approval_feedback: str = ""

    @workflow.run
    async def run(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute researcher workflow."""
        workflow.logger.info(f"Starting ResearcherWorkflow with campaign_data: {campaign_data}")

        # Step 1: Compile research inputs
        compiled_inputs = await workflow.execute_activity(
            compile_research_input_activity,
            campaign_data,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                initial_interval=timedelta(seconds=1),
            ),
        )

        # Step 2: Execute ResearchBriefWorkflow
        brief_result = await workflow.execute_child_workflow(
            ResearchBriefWorkflow.run,
            compiled_inputs,
            id=f"{workflow.info().workflow_id}-research-brief",
            task_queue=workflow.info().task_queue,
        )

        # Step 3: Execute ResearchConceptNoteWorkflow
        concept_note_result = await workflow.execute_child_workflow(
            ResearchConceptNoteWorkflow.run,
            brief_result,
            id=f"{workflow.info().workflow_id}-concept-note",
            task_queue=workflow.info().task_queue,
        )

        # Step 4: Summarise research findings
        research_findings = await workflow.execute_activity(
            summarise_research_findings_activity,
            concept_note_result,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                initial_interval=timedelta(seconds=1),
            ),
        )

        researcher_output = {
            "research_brief": brief_result,
            "concept_note": concept_note_result,
            "research_findings": research_findings,
        }

        # Step 5: Human-in-the-middle - Wait for approval signal
        workflow.logger.info("Waiting for research approval signal...")
        await workflow.wait_condition(
            lambda: self.approval_status != "pending",
            timeout=timedelta(hours=24)
        )

        # Rerun workflow with feedback
        if self.approval_status == "feedback":
            workflow.logger.info(f"Research feedback received: {self.approval_feedback}")
            return await self.run(campaign_data)

        if self.approval_status == "approved":
            workflow.logger.info("Research approved!")
            return {
                "status": "approved",
                "approval_feedback": self.approval_feedback,
                "research_outputs": researcher_output,
            }

        if self.approval_status == "rejected":
            workflow.logger.warning(f"Research rejected: {self.approval_feedback}")
            raise Exception(f"Research rejected: {self.approval_feedback}")

    @workflow.signal(name="provide_feedback")
    async def provide_feedback(self, feedback: str = "") -> None:
        """Signal to provide feedback on research."""
        workflow.logger.info("Feedback provided via signal")
        self.approval_status = "feedback"
        self.approval_feedback = feedback

    @workflow.signal(name="approve_research")
    async def approve_research(self, feedback: str = "") -> None:
        """Signal to approve research."""
        workflow.logger.info("Researcher approved via signal")
        self.approval_status = "approved"
        self.approval_feedback = feedback

    @workflow.signal(name="reject_research")
    async def reject_research(self, feedback: str = "") -> None:
        """Signal to reject research."""
        workflow.logger.info("Researcher rejected via signal")
        self.approval_status = "rejected"
        self.approval_feedback = feedback

    @workflow.query(name="get_approval_status")
    def get_approval_status(self) -> str:
        """Query to get current approval status."""
        return self.approval_status

