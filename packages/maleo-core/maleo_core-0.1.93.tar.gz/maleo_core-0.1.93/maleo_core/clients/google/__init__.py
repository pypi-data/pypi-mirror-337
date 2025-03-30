from .google_cloud_logging import GoogleCloudLogging
from .google_cloud_storage import GoogleCloudStorage

class GoogleCloudClients:
    Logging = GoogleCloudLogging
    Storage = GoogleCloudStorage