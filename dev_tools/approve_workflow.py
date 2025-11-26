"""Example script to send approval signals to workflows."""

import asyncio
import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from temporalio.client import Client
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def send_approval_signal(workflow_id: str, signal_name: str, feedback: str = "Approved"):
    """Send an approval signal to a workflow."""
    client = await Client.connect(
        settings.temporal_host,
        namespace=settings.temporal_namespace,
    )

    handle = client.get_workflow_handle(workflow_id)

    logger.info(f"Sending signal '{signal_name}' to workflow '{workflow_id}'")
    await handle.signal(signal_name, feedback)
    logger.info("✓ Signal sent successfully!")


async def approve_research(campaign_id: str, feedback: str = "Research approved"):
    """Approve research workflow."""
    workflow_id = f"marketing-campaign-{campaign_id}-researcher"
    await send_approval_signal(workflow_id, "approve_research", feedback)


async def approve_creative(campaign_id: str, feedback: str = "Creatives approved"):
    """Approve creative workflow."""
    workflow_id = f"marketing-campaign-{campaign_id}-creative"
    await send_approval_signal(workflow_id, "approve_creatives", feedback)


async def approve_media_buy(campaign_id: str, feedback: str = "Media buy approved"):
    """Approve media buy in GoLive workflow."""
    workflow_id = f"marketing-campaign-{campaign_id}-golive"
    await send_approval_signal(workflow_id, "approve_media_buy", feedback)


async def approve_measurements(campaign_id: str, feedback: str = "Measurements approved"):
    """Approve measurements workflow."""
    workflow_id = f"marketing-campaign-{campaign_id}-measurements"
    await send_approval_signal(workflow_id, "approve_measurements", feedback)


async def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python scripts/approve_workflow.py <campaign_id> <stage> [feedback]")
        print("")
        print("Stages:")
        print("  research    - Approve research stage")
        print("  creative    - Approve creative stage")
        print("  media_buy   - Approve media buy stage")
        print("  measurements - Approve measurements stage")
        print("  all         - Approve all stages sequentially")
        print("")
        print("Example:")
        print("  python scripts/approve_workflow.py CAMP-2025-001 research 'Looks great!'")
        print("  python scripts/approve_workflow.py CAMP-2025-001 all")
        sys.exit(1)

    campaign_id = sys.argv[1]
    stage = sys.argv[2]
    feedback = sys.argv[3] if len(sys.argv) > 3 else "Approved"

    try:
        if stage == "research":
            await approve_research(campaign_id, feedback)
        elif stage == "creative":
            await approve_creative(campaign_id, feedback)
        elif stage == "media_buy":
            await approve_media_buy(campaign_id, feedback)
        elif stage == "measurements":
            await approve_measurements(campaign_id, feedback)
        elif stage == "all":
            logger.info("Approving all stages sequentially...")
            await approve_research(campaign_id, feedback)
            await asyncio.sleep(1)
            await approve_creative(campaign_id, feedback)
            await asyncio.sleep(1)
            await approve_media_buy(campaign_id, feedback)
            await asyncio.sleep(1)
            await approve_measurements(campaign_id, feedback)
            logger.info("✓ All stages approved!")
        else:
            logger.error(f"Unknown stage: {stage}")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Failed to send approval: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())

