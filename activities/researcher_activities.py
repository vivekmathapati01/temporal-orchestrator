"""Researcher workflow activities."""

from temporalio import activity
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


@activity.defn(name="compile_research_input_activity")
async def compile_research_input_activity(campaign_data: Dict[str, Any]) -> Dict[str, Any]:
    """Compile research inputs from campaign data."""
    logger.info(f"Hello from compile_research_input_activity with campaign_data: {campaign_data}")
    return {
        "status": "success",
        "message": "Research inputs compiled successfully",
        "data": campaign_data
    }


@activity.defn(name="summarise_research_findings_activity")
async def summarise_research_findings_activity(research_data: Dict[str, Any]) -> Dict[str, Any]:
    """Summarise research findings."""
    logger.info(f"Hello from summarise_research_findings_activity with research_data: {research_data}")
    return {
        "status": "success",
        "message": "Research findings summarised successfully",
        "summary": "Research summary generated"
    }


@activity.defn(name="research_brief_activity")
async def research_brief_activity(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate research brief."""
    logger.info(f"Hello from research_brief_activity with input_data: {input_data}")
    return {
        "status": "success",
        "message": "Research brief generated successfully",
        "brief": "Research brief content"
    }


@activity.defn(name="research_concept_note_activity")
async def research_concept_note_activity(brief_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate research concept note."""
    logger.info(f"Hello from research_concept_note_activity with brief_data: {brief_data}")
    return {
        "status": "success",
        "message": "Research concept note generated successfully",
        "concept_note": "Concept note content"
    }

