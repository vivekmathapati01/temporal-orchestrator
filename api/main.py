"""FastAPI application."""

import logging
from fastapi import FastAPI
from api.endpoints.v1.routers import router as v1_router
from config.settings import settings

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title="Temporal Workflow API",
    version=settings.app_version,
    docs_url="/docs",
)

app.include_router(v1_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"service": settings.app_name, "version": settings.app_version}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)

