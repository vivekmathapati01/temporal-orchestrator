"""Main measurements workflow."""

from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
from typing import Dict, Any

with workflow.unsafe.imports_passed_through():
    from activities.measurements_activities import (
        fetch_previous_metrics_activity,
        aggregate_measurements_activity,
    )
    from workflows.measuements_workflows.poll_measurements_workflow import PollMeasurementsWorkflow
    from workflows.measuements_workflows.retrieval_workflow import RetrievalWorkflow


@workflow.defn(name="MeasurementsWorkflow")
class MeasurementsWorkflow:
    """Main measurements workflow with human-in-the-loop approval."""

    def __init__(self) -> None:
        self.approval_status: str = "pending"
        self.approval_feedback: str = ""

    @workflow.run
    async def run(self, deployment_output: Dict[str, Any]) -> Dict[str, Any]:
        """Execute measurements workflow."""
        workflow.logger.info(f"Starting MeasurementsWorkflow with deployment_output: {deployment_output}")

        # Step 1: Fetch previous metrics
        campaign_id = deployment_output.get("deployment", {}).get("deployment_id", "unknown")

        previous_metrics = await workflow.execute_activity(
            fetch_previous_metrics_activity,
            campaign_id,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                initial_interval=timedelta(seconds=1),
            ),
        )

        # Step 2: Execute PollMeasurementsWorkflow
        poll_result = await workflow.execute_child_workflow(
            PollMeasurementsWorkflow.run,
            campaign_id,
            id=f"{workflow.info().workflow_id}-poll",
            task_queue=workflow.info().task_queue,
        )

        # Step 3: Aggregate measurements
        measurements_data = {
            "previous": previous_metrics,
            "current": poll_result,
        }

        aggregated = await workflow.execute_activity(
            aggregate_measurements_activity,
            measurements_data,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                initial_interval=timedelta(seconds=1),
            ),
        )

        # Step 4: Human-in-the-middle - Wait for approval signal
        workflow.logger.info("Waiting for measurements approval signal...")
        await workflow.wait_condition(lambda: self.approval_status != "pending")

        #step 4: Handle approval decision

        # rerun if feedback
        if self.approval_status == "feedback":
            workflow.logger.info(f"Feedback received: {self.approval_feedback}. Rerunning measurements aggregation...")
            return await self.run(deployment_output)  # Rerun the workflow with the same deployment output

        if self.approval_status == "rejected":
            workflow.logger.warning(f"Measurements rejected: {self.approval_feedback}")
            raise Exception(f"Measurements rejected: {self.approval_feedback}")

        workflow.logger.info("Measurements approved! Proceeding to retrieval...")

        # Step 5: Execute RetrievalWorkflow
        retrieval_result = await workflow.execute_child_workflow(
            RetrievalWorkflow.run,
            aggregated,
            id=f"{workflow.info().workflow_id}-retrieval",
            task_queue=workflow.info().task_queue,
        )

        return {
            "status": "completed",
            "measurements": aggregated,
            "retrieval": retrieval_result,
            "approval_feedback": self.approval_feedback,
        }

    @workflow.signal(name="provide_feedback")
    async def provide_feedback(self, feedback: str = "") -> None:
        """Signal to provide feedback on measurements."""
        workflow.logger.info("Feedback received via signal")
        self.approval_status = "feedback"
        self.approval_feedback = feedback

    @workflow.signal(name="approve_measurements")
    async def approve_measurements(self, feedback: str = "") -> None:
        """Signal to approve measurements."""
        workflow.logger.info("Measurements approved via signal")
        self.approval_status = "approved"
        self.approval_feedback = feedback

    @workflow.signal(name="reject_measurements")
    async def reject_measurements(self, feedback: str = "") -> None:
        """Signal to reject measurements."""
        workflow.logger.info("Measurements rejected via signal")
        self.approval_status = "rejected"
        self.approval_feedback = feedback

    @workflow.query(name="get_approval_status")
    def get_approval_status(self) -> str:
        """Query to get current approval status."""
        return self.approval_status

