from .controller import BaseHTTPClientControllerResults
from .service import BaseHTTPClientServiceResults

class BaseHTTPClientResults:
    Controller = BaseHTTPClientControllerResults
    Service = BaseHTTPClientServiceResults