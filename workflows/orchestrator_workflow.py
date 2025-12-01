"""Marketing Orchestrator - Main parent workflow."""

from temporalio import workflow
from datetime import timedelta
from typing import Dict, Any
import logging

with workflow.unsafe.imports_passed_through():
    from workflows.researcher_workflows.researcher_workflow import ResearcherWorkflow
    from workflows.creatives_workflows.creative_workflow import CreativeWorkflow
    from workflows.golive_workflows.golive_workflow import GoLiveWorkflow
    from workflows.measuements_workflows.measurements_workflow import MeasurementsWorkflow

logger = logging.getLogger(__name__)


@workflow.defn(name="MarketingOrchestratorWorkflow")
class MarketingOrchestratorWorkflow:
    """
    Parent workflow that orchestrates the entire marketing campaign lifecycle.

    This workflow coordinates four main child workflows:
    1. ResearcherWorkflow - Campaign research and concept development
    2. CreativeWorkflow - Creative asset generation (SMS, images, videos, emails)
    3. GoLiveWorkflow - Media buying and campaign deployment
    4. MeasurementsWorkflow - Campaign measurement and analysis

    Each child workflow includes human-in-the-loop approval steps.
    """

    @workflow.run
    async def run(self, campaign_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the complete marketing orchestration workflow.

        Args:
            campaign_input: Input data for the campaign including:
                - campaign_id: Unique campaign identifier
                - campaign_name: Name of the campaign
                - target_audience: Target audience details
                - budget: Campaign budget
                - objectives: Campaign objectives
                - Any other relevant campaign data

        Returns:
            Dict containing results from all workflow stages
        """
        workflow.logger.info(f"Starting MarketingOrchestratorWorkflow for campaign: {campaign_input.get('campaign_name', 'Unknown')}")

        workflow_id = workflow.info().workflow_id
        task_queue = workflow.info().task_queue

        # Stage 1: Research Phase
        workflow.logger.info("=" * 60)
        workflow.logger.info("STAGE 1: RESEARCH PHASE")
        workflow.logger.info("=" * 60)

        research_result = await workflow.execute_child_workflow(
            ResearcherWorkflow.run,
            campaign_input,
            id=f"{workflow_id}-researcher",
            task_queue=task_queue,
        )

        workflow.logger.info("Research phase completed successfully!")

        # Stage 2: Creative Phase
        workflow.logger.info("=" * 60)
        workflow.logger.info("STAGE 2: CREATIVE PHASE")
        workflow.logger.info("=" * 60)

        creative_result = await workflow.execute_child_workflow(
            CreativeWorkflow.run,
            research_result,
            id=f"{workflow_id}-creative",
            task_queue=task_queue,
        )

        workflow.logger.info("Creative phase completed successfully!")

        # Stage 3: GoLive Phase
        workflow.logger.info("=" * 60)
        workflow.logger.info("STAGE 3: GOLIVE PHASE")
        workflow.logger.info("=" * 60)

        golive_result = await workflow.execute_child_workflow(
            GoLiveWorkflow.run,
            creative_result,
            id=f"{workflow_id}-golive",
            task_queue=task_queue,
        )

        workflow.logger.info("GoLive phase completed successfully!")

        # Stage 4: Measurements Phase
        workflow.logger.info("=" * 60)
        workflow.logger.info("STAGE 4: MEASUREMENTS PHASE")
        workflow.logger.info("=" * 60)

        measurements_result = await workflow.execute_child_workflow(
            MeasurementsWorkflow.run,
            golive_result,
            id=f"{workflow_id}-measurements",
            task_queue=task_queue,
        )

        workflow.logger.info("Measurements phase completed successfully!")

        # Final Result
        workflow.logger.info("=" * 60)
        workflow.logger.info("MARKETING CAMPAIGN ORCHESTRATION COMPLETED!")
        workflow.logger.info("=" * 60)

        return {
            "campaign_id": campaign_input.get("campaign_id"),
            "campaign_name": campaign_input.get("campaign_name"),
            "status": "completed",
            "research": research_result,
            "creative": creative_result,
            "golive": golive_result,
            "measurements": measurements_result,
        }

    @workflow.query
    def get_campaign_status(self) -> str:
        """Query to get the current campaign status."""
        return "running"

