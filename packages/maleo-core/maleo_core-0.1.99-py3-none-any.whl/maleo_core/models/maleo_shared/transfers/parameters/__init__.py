from .general import MaleoSharedGeneralParameters
from .service import MaleoSharedServiceParameters
from .client import MaleoSharedHTTPClientParameters

class MaleoSharedParameters:
    General = MaleoSharedGeneralParameters
    Service = MaleoSharedServiceParameters
    Client = MaleoSharedHTTPClientParameters