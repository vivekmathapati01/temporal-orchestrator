"""Example script to start a marketing campaign workflow."""

import asyncio
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from client.temporal_client import get_temporal_client
from config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start_campaign():
    """Start a marketing campaign workflow."""
    # Get Temporal client (reusable singleton)
    client = await get_temporal_client()

    # Define campaign input
    campaign_input = {
        "campaign_id": "CAMP-2025-001",
        "campaign_name": "Spring Product Launch 2025",
        "target_audience": {
            "demographics": "Adults 25-45",
            "interests": ["technology", "innovation"],
            "location": "US, UK, CA",
        },
        "budget": 100000,
        "objectives": [
            "Increase brand awareness",
            "Drive product sales",
            "Generate leads",
        ],
        "channels": ["email", "sms", "social", "video"],
    }

    # Start the workflow
    logger.info(f"Starting campaign: {campaign_input['campaign_name']}")

    handle = await client.start_workflow(
        "MarketingOrchestratorWorkflow",
        campaign_input,
        id=f"marketing-campaign-{campaign_input['campaign_id']}",
        task_queue=settings.temporal_task_queue,
    )

    logger.info(f"Workflow started with ID: {handle.id}")
    logger.info(f"Run ID: {handle.result_run_id}")
    logger.info("")
    logger.info("=" * 60)
    logger.info("WORKFLOW STARTED - WAITING FOR APPROVALS")
    logger.info("=" * 60)
    logger.info("")
    logger.info("The workflow is now running and will wait for human approvals at each stage:")
    logger.info("")
    logger.info("1. Research approval - use signal 'approve_research' or 'reject_research'")
    logger.info("2. Creative approval - use signal 'approve_creatives' or 'reject_creatives'")
    logger.info("3. Media buy approval - use signal 'approve_media_buy' or 'reject_media_buy'")
    logger.info("4. Measurements approval - use signal 'approve_measurements' or 'reject_measurements'")
    logger.info("")
    logger.info("=" * 60)
    logger.info("")
    logger.info("You can send signals using the Temporal UI or CLI.")
    logger.info(f"Workflow ID: {handle.id}")
    logger.info("")
    logger.info("Example CLI command to approve research:")
    logger.info(f"  temporal workflow signal --workflow-id {handle.id}-researcher --name approve_research --input '\"Looks good!\"'")
    logger.info("")

    return handle


async def main():
    """Main entry point."""
    try:
        handle = await start_campaign()
        logger.info("Campaign workflow initiated successfully!")
        logger.info(f"Monitor the workflow in Temporal UI: http://localhost:8233/namespaces/{settings.temporal_namespace}/workflows/{handle.id}")
    except Exception as e:
        logger.error(f"Failed to start campaign: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())

