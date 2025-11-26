"""Configuration settings for the Temporal orchestrator.

This module provides type-safe, validated configuration management.

Benefits of using Pydantic Settings over raw .env:
- Type safety: Automatic type conversion and validation
- Default values: Centralized defaults instead of scattered os.getenv calls
- Validation: Ensures valid values before app starts (fail fast)
- Documentation: Clear definition of all available settings
- IDE support: Auto-completion and type hints
- Computed properties: Derive values from other settings
- Environment files: Automatic .env file loading
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    The .env file stores raw values, this class provides:
    - Type conversion (strings to proper types)
    - Validation (only valid values accepted)
    - Defaults (fallback values)
    - Computed properties (derived values)

    Example .env:
        TEMPORAL_HOST=localhost:7233
        LOG_LEVEL=DEBUG
        TEMPORAL_NAMESPACE=production
    """

    # Temporal Configuration
    temporal_host: str = "localhost:7233"
    temporal_namespace: str = "default"
    temporal_task_queue: str = "marketing-orchestrator-queue"

    # Logging Configuration
    # Using Literal ensures only valid log levels are accepted
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # Application Configuration
    app_name: str = "marketing-orchestrator"
    app_version: str = "0.1.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        # Validate on assignment - catch errors immediately
        validate_assignment=True,
    )

    # Example computed property
    @property
    def is_local_dev(self) -> bool:
        """Check if running in local development mode."""
        return "localhost" in self.temporal_host

    @property
    def temporal_ui_url(self) -> str:
        """Get the Temporal UI URL based on host."""
        if self.is_local_dev:
            return "http://localhost:8233"
        return f"http://{self.temporal_host.split(':')[0]}:8233"


# Global settings instance
# This is loaded once at import time - any validation errors fail immediately
settings = Settings()

