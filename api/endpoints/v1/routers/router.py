"""V1 API routes."""

from fastapi import APIRouter
from . import workflow_router

router = APIRouter(prefix="/api/v1")
router.include_router(workflow_router.router)

