import os
from datetime import timedelta
from google.auth import default
from google.cloud.storage import Bucket, Client
from google.oauth2 import service_account
from typing import Optional

class GoogleCloudStorage:
    _client:Optional[Client] = None
    _buckets:dict[str, Bucket] = {}

    @classmethod
    def initialize(cls) -> None:
        """Initialize the cloud storage if not already initialized."""
        if cls._client is None:
            #* Setup credentials with fallback chain
            credentials = None
            credentials_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            try:
                if credentials_file:
                    credentials = service_account.Credentials.from_service_account_file(credentials_file)
                else:
                    credentials, _ = default()
            except Exception as e:
                raise ValueError(f"Failed to initialize credentials: {str(e)}")

            cls._client = Client(credentials=credentials)

            #* Preload default bucket if env variable is set
            default_bucket_name = os.getenv("GCS_BUCKET_NAME")
            if default_bucket_name:
                cls.add_bucket(bucket_name=default_bucket_name)

    @classmethod
    def dispose(cls) -> None:
        """Dispose of the cloud storage and release any resources."""
        if cls._client is not None:
            cls._client.close()
            cls._client = None
            cls._buckets.clear()

    @classmethod
    def _get_client(cls) -> Client:
        """Retrieve the cloud storage client, initializing it if necessary."""
        cls.initialize()
        return cls._client

    @classmethod
    def _get_bucket(cls, bucket_name:Optional[str] = None) -> Bucket:
        """
        Retrieve a bucket instance, using a default bucket if none is provided.

        Args:
            bucket_name: Optional[str] - Name of the bucket. Defaults to GCS_BUCKET_NAME from env.

        Returns:
            Bucket: Google Cloud Storage bucket instance.

        Raises:
            ValueError: If the bucket does not exist.
        """
        cls.initialize()  #* Ensure client is initialized

        if bucket_name is None:
            bucket_name = os.getenv("GCS_BUCKET_NAME")  #* Default bucket

        if not bucket_name:
            raise ValueError("Bucket name must be provided or set in GCS_BUCKET_NAME environment variable.")

        #* Check cache first
        if bucket_name in cls._buckets:
            return cls._buckets[bucket_name]

        #* Lookup bucket and store in cache
        bucket = cls._client.lookup_bucket(bucket_name)
        if bucket is None:
            raise ValueError(f"Bucket '{bucket_name}' does not exist.")

        cls._buckets[bucket_name] = bucket
        return bucket

    @classmethod
    def add_bucket(cls, bucket_name:str) -> None:
        """
        Manually add a bucket to the cache.

        Args:
            bucket_name (str): Name of the bucket.

        Raises:
            ValueError: If the bucket does not exist.
        """
        client = cls._get_client()

        if bucket_name in cls._buckets:
            return  #* Bucket already cached

        bucket = client.lookup_bucket(bucket_name)
        if bucket is None:
            raise ValueError(f"Bucket '{bucket_name}' does not exist.")

        cls._buckets[bucket_name] = bucket

    def __init__(self, bucket_name:Optional[str] = None) -> None:
        """Initialize the cloud storage instance."""
        self._bucket = self.__class__._get_bucket(bucket_name)

    def generate_signed_url(self, location:str) -> str:
        """
        generate signed URL of a file in the bucket based on its location.

        Args:
            location: str
                Location of the file inside the bucket

        Returns:
            str: File's pre-signed download url

        Raises:
            ValueError: If the file does not exist
        """
        blob = self._bucket.blob(blob_name=location)
        if not blob.exists():
            raise ValueError(f"File '{location}' did not exists.")

        url = blob.generate_signed_url(version="v4", expiration=timedelta(minutes=15), method="GET")
        return url