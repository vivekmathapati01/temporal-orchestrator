"""Creative workflow activities."""

from temporalio import activity
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


@activity.defn(name="prepare_creative_inputs_activity")
async def prepare_creative_inputs_activity(research_output: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare creative inputs from research output."""
    logger.info(f"Hello from prepare_creative_inputs_activity with research_output: {research_output}")
    return {
        "status": "success",
        "message": "Creative inputs prepared successfully",
        "data": research_output
    }


@activity.defn(name="consolidate_creatives_activity")
async def consolidate_creatives_activity(creative_outputs: Dict[str, Any]) -> Dict[str, Any]:
    """Consolidate all creative outputs."""
    logger.info(f"Hello from consolidate_creatives_activity with creative_outputs: {creative_outputs}")
    return {
        "status": "success",
        "message": "Creatives consolidated successfully",
        "consolidated": "All creatives consolidated"
    }


@activity.defn(name="sms_generation_activity")
async def sms_generation_activity(creative_input: Dict[str, Any]) -> Dict[str, Any]:
    """Generate SMS content."""
    logger.info(f"Hello from sms_generation_activity with creative_input: {creative_input}")
    return {
        "status": "success",
        "message": "SMS content generated successfully",
        "sms_content": "Generated SMS content"
    }


@activity.defn(name="image_generation_activity")
async def image_generation_activity(creative_input: Dict[str, Any]) -> Dict[str, Any]:
    """Generate image content."""
    logger.info(f"Hello from image_generation_activity with creative_input: {creative_input}")
    return {
        "status": "success",
        "message": "Image content generated successfully",
        "image_url": "https://example.com/generated-image.jpg"
    }


@activity.defn(name="video_generation_activity")
async def video_generation_activity(creative_input: Dict[str, Any]) -> Dict[str, Any]:
    """Generate video content."""
    logger.info(f"Hello from video_generation_activity with creative_input: {creative_input}")
    return {
        "status": "success",
        "message": "Video content generated successfully",
        "video_url": "https://example.com/generated-video.mp4"
    }


@activity.defn(name="email_template_generation_activity")
async def email_template_generation_activity(creative_input: Dict[str, Any]) -> Dict[str, Any]:
    """Generate email template."""
    logger.info(f"Hello from email_template_generation_activity with creative_input: {creative_input}")
    return {
        "status": "success",
        "message": "Email template generated successfully",
        "email_template": "Generated email template HTML"
    }

