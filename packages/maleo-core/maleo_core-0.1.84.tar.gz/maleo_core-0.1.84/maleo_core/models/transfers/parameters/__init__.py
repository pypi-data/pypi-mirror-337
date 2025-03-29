from .general import GeneralParameters
from .service import ServiceParameters
from .client import ClientParameters

class BaseParameters:
    General = GeneralParameters
    Service = ServiceParameters
    Client = ClientParameters