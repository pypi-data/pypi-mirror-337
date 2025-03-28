import os
from google.auth import default
from google.cloud import logging
from google.cloud.logging.handlers import CloudLoggingHandler
from google.oauth2 import service_account
from typing import Optional

class GoogleCloudLoggingClient:
    def __init__(self):
        """Initialize the Cloud Logging client."""
        self.project_id = os.getenv("GCP_PROJECT_ID")
        if not self.project_id:
            raise ValueError("Project ID must be provided or set in GCP_PROJECT_ID environment variable")

        # Setup credentials with fallback chain
        credentials = None
        try:
            if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
                credentials = service_account.Credentials.from_service_account_file(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
            else:
                credentials, project = default()
        except Exception as e:
            raise ValueError(f"Failed to initialize credentials: {str(e)}")

        self.client = logging.Client(credentials=credentials)

    def create_handler(self, name:str):
        return CloudLoggingHandler(self.client, name)

class GoogleCloudLoggingClientManager:
    _cloud_logging_client:Optional[GoogleCloudLoggingClient] = None

    @classmethod
    def initialize(cls) -> GoogleCloudLoggingClient:
        """Initialize the cloud logging client if not already initialized."""
        if cls._cloud_logging_client is None:
            cls._cloud_logging_client = GoogleCloudLoggingClient()
            cls._cloud_logging_client.client.setup_logging()
        return cls._cloud_logging_client

    @classmethod
    def get(cls) -> GoogleCloudLoggingClient:
        """Retrieve the cloud logging client, initializing it if necessary."""
        return cls.initialize()

    @classmethod
    def dispose(cls) -> None:
        """Dispose of the cloud logging client and release any resources."""
        if cls._cloud_logging_client is not None:
            cls._cloud_logging_client.client.close()
            cls._cloud_logging_client = None