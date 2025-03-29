from .general import GeneralResults
from .controllers import ControllerResults
from .service import ServiceResults
from .query import QueryResults

class BaseResults:
    General = GeneralResults
    Controller = ControllerResults
    Service = ServiceResults
    Query = QueryResults