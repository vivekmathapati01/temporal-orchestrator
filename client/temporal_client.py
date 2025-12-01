"""Temporal client implementation."""

import logging
from temporalio.client import Client, TLSConfig

from config.settings import settings

logger = logging.getLogger(__name__)


class TemporalClient:
    """Singleton class to manage Temporal client connection."""

    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TemporalClient, cls).__new__(cls)
        return cls._instance

    async def _init_async(self):
        """Initialize the Temporal client connection."""
        tls_config = None
        if settings.temporal_tls_enabled:
            logger.info("TLS enabled - configuring secure connection")
            if not settings.temporal_client_cert or not settings.temporal_client_key:
                raise ValueError("TLS enabled but client_cert or client_key not provided")

            # Read certificate and key files
            with open(settings.temporal_client_cert, 'rb') as f:
                client_cert = f.read()
            with open(settings.temporal_client_key, 'rb') as f:
                client_key = f.read()

            tls_config = TLSConfig(
                client_cert=client_cert,
                client_private_key=client_key,
            )

        logger.info(f"Connecting to Temporal server at {settings.temporal_host}")
        logger.info(f"Namespace: {settings.temporal_namespace}")

        self._client = await Client.connect(
            settings.temporal_host,
            namespace=settings.temporal_namespace,
            tls=tls_config,
        )

        logger.info("Successfully connected to Temporal server")
        return self._client

    async def get_client(self) -> Client:
        """Get or create the Temporal client instance.

        Returns:
            Client: The connected Temporal client instance.
        """
        if self._client is None:
            await self._init_async()

        return self._client


# Global instance
_temporal_client_instance = TemporalClient()


async def get_temporal_client() -> Client:
    """Get the global Temporal client instance.

    This is the main function to use for getting a Temporal client.
    It ensures a single client instance is reused across the application.

    Returns:
        Client: The connected Temporal client instance.

    Example:
        client = await get_temporal_client()
        handle = await client.start_workflow(...)
    """
    return await _temporal_client_instance.get_client()

