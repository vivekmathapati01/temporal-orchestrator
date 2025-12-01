"""Main creative workflow."""

from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
from typing import Dict, Any

with workflow.unsafe.imports_passed_through():
    from activities.creative_activities import (
        prepare_creative_inputs_activity,
        consolidate_creatives_activity,
    )
    from workflows.creatives_workflows.sms_generation_workflow import SMSGenerationWorkflow
    from workflows.creatives_workflows.image_generation_workflow import ImageGenerationWorkflow
    from workflows.creatives_workflows.video_generation_workflow import VideoGenerationWorkflow
    from workflows.creatives_workflows.email_template_workflow import EmailTemplateWorkflow


@workflow.defn(name="CreativeWorkflow")
class CreativeWorkflow:
    """Main creative workflow with human-in-the-loop approval."""

    def __init__(self) -> None:
        self.approval_status: str = "pending"
        self.approval_feedback: str = ""

    @workflow.run
    async def run(self, research_output: Dict[str, Any]) -> Dict[str, Any]:
        """Execute creative workflow."""
        workflow.logger.info(f"Starting CreativeWorkflow with research_output: {research_output}")

        # Step 1: Prepare creative inputs
        creative_inputs = await workflow.execute_activity(
            prepare_creative_inputs_activity,
            research_output,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                initial_interval=timedelta(seconds=1),
            ),
        )

        # Step 2: Execute all creative generation workflows in parallel
        workflow.logger.info("Executing creative generation workflows in parallel")

        sms_task = workflow.execute_child_workflow(
            SMSGenerationWorkflow.run,
            creative_inputs,
            id=f"{workflow.info().workflow_id}-sms",
            task_queue=workflow.info().task_queue,
        )

        image_task = workflow.execute_child_workflow(
            ImageGenerationWorkflow.run,
            creative_inputs,
            id=f"{workflow.info().workflow_id}-image",
            task_queue=workflow.info().task_queue,
        )

        video_task = workflow.execute_child_workflow(
            VideoGenerationWorkflow.run,
            creative_inputs,
            id=f"{workflow.info().workflow_id}-video",
            task_queue=workflow.info().task_queue,
        )

        email_task = workflow.execute_child_workflow(
            EmailTemplateWorkflow.run,
            creative_inputs,
            id=f"{workflow.info().workflow_id}-email",
            task_queue=workflow.info().task_queue,
        )

        # Wait for all creative workflows to complete
        sms_result = await sms_task
        image_result = await image_task
        video_result = await video_task
        email_result = await email_task

        # Step 3: Consolidate all creatives
        creative_outputs = {
            "sms": sms_result,
            "image": image_result,
            "video": video_result,
            "email": email_result,
        }

        consolidated = await workflow.execute_activity(
            consolidate_creatives_activity,
            creative_outputs,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                initial_interval=timedelta(seconds=1),
            ),
        )

        # Step 4: Human-in-the-middle - Wait for approval signal
        workflow.logger.info("Waiting for creative approval signal...")
        await workflow.wait_condition(lambda: self.approval_status != "pending")

        #step 5: Handle approval or rejection
        if self.approval_status == "feedback":
            workflow.logger.info(f"Feedback received: {self.approval_feedback}. Rerunning creative workflow.")
            # Rerun the creative workflow with feedback
            return await self.run(research_output) #pass user feedback to creative generation activities if needed

        if self.approval_status == "approved":
            workflow.logger.info("Creatives approved!")
            return {
                "status": "approved",
                "approval_feedback": self.approval_feedback,
                "creative_outputs": creative_outputs,
            }

        if self.approval_status == "rejected":
            workflow.logger.warning(f"Creatives rejected: {self.approval_feedback}")
            raise Exception(f"Creatives rejected: {self.approval_feedback}")


    @workflow.signal(name="provide_feedback")
    async def provide_feedback(self, feedback: str = "") -> None:
        """Signal to provide feedback for creatives."""
        workflow.logger.info("Feedback provided via signal")
        self.approval_status = "feedback"
        self.approval_feedback = feedback

    @workflow.signal(name="approve_creatives")
    async def approve_creatives(self, feedback: str = "") -> None:
        """Signal to approve creatives."""
        workflow.logger.info("Creatives approved via signal")
        self.approval_status = "approved"
        self.approval_feedback = feedback

    @workflow.signal(name="reject_creatives")
    async def reject_creatives(self, feedback: str = "") -> None:
        """Signal to reject creatives."""
        workflow.logger.info("Creatives rejected via signal")
        self.approval_status = "rejected"
        self.approval_feedback = feedback

    @workflow.query(name="get_approval_status")
    def get_approval_status(self) -> str:
        """Query to get current approval status."""
        return self.approval_status

