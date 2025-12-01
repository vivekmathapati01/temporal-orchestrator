"""Main GoLive workflow."""

import logging
from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
from typing import Dict, Any

with workflow.unsafe.imports_passed_through():
    from activities.golive_activities import (
        prepare_media_plan_activity,
        summarise_media_buy_report_activity,
    )
    from workflows.golive_workflows.media_buying_workflow import MediaBuyingWorkflow
    from workflows.golive_workflows.deployment_workflow import DeploymentWorkflow

logger = logging.getLogger(__name__)


@workflow.defn(name="GoLiveWorkflow")
class GoLiveWorkflow:
    """Main GoLive workflow with human-in-the-loop approval."""

    def __init__(self) -> None:
        self.approval_status: str = "pending"
        self.approval_feedback: str = ""

    @workflow.run
    async def run(self, creative_output: Dict[str, Any]) -> Dict[str, Any]:
        """Execute GoLive workflow."""
        workflow.logger.info(f"Starting GoLiveWorkflow with creative_output: {creative_output}")

        # Step 1: Prepare media plan
        media_plan = await workflow.execute_activity(
            prepare_media_plan_activity,
            creative_output,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                initial_interval=timedelta(seconds=1),
            ),
        )

        # Step 2: Execute MediaBuyingWorkflow
        media_buy_result = await workflow.execute_child_workflow(
            MediaBuyingWorkflow.run,
            media_plan,
            id=f"{workflow.info().workflow_id}-media-buying",
            task_queue=workflow.info().task_queue,
        )

        # Step 3: Summarise media buy report
        media_buy_summary = await workflow.execute_activity(
            summarise_media_buy_report_activity,
            media_buy_result,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                initial_interval=timedelta(seconds=1),
            ),
        )

        media_buy_output = {
            "media_buy_result": media_buy_result,
            "media_buy_summary": media_buy_summary,
        }

        # Step 4: Human-in-the-middle - Wait for approval signal
        workflow.logger.info("Waiting for media buy approval signal...")
        await workflow.wait_condition(lambda: self.approval_status != "pending")

        # rerun media buy if feedback is provided
        if self.approval_status == "feedback":
            workflow.logger.info(f"Feedback received: {self.approval_feedback}")
            # Reset approval status to pending for next iteration
            self.approval_status = "pending"
            return await self.run(creative_output) # Restart the workflow with the same creative output & feedback

        if self.approval_status == "rejected":
            workflow.logger.warning(f"Media buy rejected: {self.approval_feedback}")
            raise Exception(f"Media buy rejected: {self.approval_feedback}")

        workflow.logger.info("Media buy approved! Proceeding to deployment...")

        # Step 5: Execute DeploymentWorkflow
        if self.approval_status == "approved":
            logger.info("Media buy approved, starting deployment workflow.")


        deployment_result = await workflow.execute_child_workflow(
            DeploymentWorkflow.run,
            media_buy_output,
            id=f"{workflow.info().workflow_id}-deployment",
            task_queue=workflow.info().task_queue,
        )

        return {
            "status": "deployed",
            "deployment": deployment_result,
            "media_buy_summary": media_buy_summary,
            "approval_feedback": self.approval_feedback,
        }



    @workflow.signal(name="provide_feedback")
    async def provide_feedback(self, feedback: str) -> None:
        """Signal to provide feedback on media buy."""
        workflow.logger.info("Feedback received via signal")
        self.approval_status = "feedback"
        self.approval_feedback = feedback

    @workflow.signal(name="approve_media_buy")
    async def approve_media_buy(self, feedback: str = "") -> None:
        """Signal to approve media buy."""
        workflow.logger.info("Media buy approved via signal")
        self.approval_status = "approved"
        self.approval_feedback = feedback

    @workflow.signal(name="reject_media_buy")
    async def reject_media_buy(self, feedback: str = "") -> None:
        """Signal to reject media buy."""
        workflow.logger.info("Media buy rejected via signal")
        self.approval_status = "rejected"
        self.approval_feedback = feedback

    @workflow.query(name="get_approval_status")
    def get_approval_status(self) -> str:
        """Query to get current approval status."""
        return self.approval_status

