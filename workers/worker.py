"""Temporal worker implementation."""

import asyncio
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from temporalio.worker import Worker

from client.temporal_client import get_temporal_client
from config.settings import settings
from workflows import (
    MarketingOrchestratorWorkflow,
    ResearcherWorkflow,
    ResearchBriefWorkflow,
    ResearchConceptNoteWorkflow,
    CreativeWorkflow,
    SMSGenerationWorkflow,
    ImageGenerationWorkflow,
    VideoGenerationWorkflow,
    EmailTemplateWorkflow,
    GoLiveWorkflow,
    MediaBuyingWorkflow,
    DeploymentWorkflow,
    MeasurementsWorkflow,
    PollMeasurementsWorkflow,
    RetrievalWorkflow,
)
from activities import (
    # Researcher activities
    compile_research_input_activity,
    summarise_research_findings_activity,
    research_brief_activity,
    research_concept_note_activity,
    # Creative activities
    prepare_creative_inputs_activity,
    consolidate_creatives_activity,
    sms_generation_activity,
    image_generation_activity,
    video_generation_activity,
    email_template_generation_activity,
    # GoLive activities
    prepare_media_plan_activity,
    summarise_media_buy_report_activity,
    media_buying_activity,
    deployment_activity,
    # Measurements activities
    fetch_previous_metrics_activity,
    aggregate_measurements_activity,
    poll_measurements_activity,
    retrieval_activity,
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    """Run the Temporal worker."""
    logger.info("Starting Temporal worker...")
    logger.info(f"Connecting to Temporal server at {settings.temporal_host}")

    # Get Temporal client (reusable singleton)
    client = await get_temporal_client()

    logger.info(f"Task queue: {settings.temporal_task_queue}")

    # Create worker with all workflows and activities
    worker = Worker(
        client,
        task_queue=settings.temporal_task_queue,
        workflows=[
            # Main orchestrator
            MarketingOrchestratorWorkflow,
            # Researcher workflows
            ResearcherWorkflow,
            ResearchBriefWorkflow,
            ResearchConceptNoteWorkflow,
            # Creative workflows
            CreativeWorkflow,
            SMSGenerationWorkflow,
            ImageGenerationWorkflow,
            VideoGenerationWorkflow,
            EmailTemplateWorkflow,
            # GoLive workflows
            GoLiveWorkflow,
            MediaBuyingWorkflow,
            DeploymentWorkflow,
            # Measurements workflows
            MeasurementsWorkflow,
            PollMeasurementsWorkflow,
            RetrievalWorkflow,
        ],
        activities=[
            # Researcher activities
            compile_research_input_activity,
            summarise_research_findings_activity,
            research_brief_activity,
            research_concept_note_activity,
            # Creative activities
            prepare_creative_inputs_activity,
            consolidate_creatives_activity,
            sms_generation_activity,
            image_generation_activity,
            video_generation_activity,
            email_template_generation_activity,
            # GoLive activities
            prepare_media_plan_activity,
            summarise_media_buy_report_activity,
            media_buying_activity,
            deployment_activity,
            # Measurements activities
            fetch_previous_metrics_activity,
            aggregate_measurements_activity,
            poll_measurements_activity,
            retrieval_activity,
        ],
    )

    logger.info("=" * 60)
    logger.info("Worker started and listening for tasks!")
    logger.info("Registered 14 workflows and 18 activities")
    logger.info("=" * 60)

    # Run the worker
    await worker.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Worker stopped by user")
    except Exception as e:
        logger.error(f"Worker failed with error: {e}", exc_info=True)
        raise

