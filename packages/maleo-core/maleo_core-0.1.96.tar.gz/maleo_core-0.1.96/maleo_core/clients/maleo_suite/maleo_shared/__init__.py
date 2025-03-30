from .manager import MaleoSharedClientManager
from .services import MaleoSharedServices

class MaleoSharedClient:
    Manager = MaleoSharedClientManager
    Services = MaleoSharedServices