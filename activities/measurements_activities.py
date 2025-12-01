"""Measurements workflow activities."""

from temporalio import activity
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


@activity.defn(name="fetch_previous_metrics_activity")
async def fetch_previous_metrics_activity(campaign_id: str) -> Dict[str, Any]:
    """Fetch previous metrics for the campaign. get data for given campaign id"""
    logger.info(f"Hello from fetch_previous_metrics_activity with campaign_id: {campaign_id}")
    return {
        "status": "success",
        "message": "Previous metrics fetched successfully",
        "metrics": {"impressions": 0, "clicks": 0, "conversions": 0}
    }


@activity.defn(name="aggregate_measurements_activity")
async def aggregate_measurements_activity(measurements: Dict[str, Any]) -> Dict[str, Any]:
    """Aggregate all measurements."""
    logger.info(f"Hello from aggregate_measurements_activity with measurements: {measurements}")
    return {
        "status": "success",
        "message": "Measurements aggregated successfully",
        "aggregated": "Aggregated measurements data"
    }


@activity.defn(name="poll_measurements_activity")
async def poll_measurements_activity(deployment_id: str) -> Dict[str, Any]:
    """Poll for campaign measurements."""
    logger.info(f"Hello from poll_measurements_activity with deployment_id: {deployment_id}")
    return {
        "status": "success",
        "message": "Measurements polled successfully",
        "measurements": {"impressions": 1000, "clicks": 50, "conversions": 5}
    }


@activity.defn(name="retrieval_activity")
async def retrieval_activity(measurement_data: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieve and store final measurements."""
    logger.info(f"Hello from retrieval_activity with measurement_data: {measurement_data}")
    return {
        "status": "success",
        "message": "Measurements retrieved and stored successfully",
        "retrieval_id": "retrieval-12345"
    }

