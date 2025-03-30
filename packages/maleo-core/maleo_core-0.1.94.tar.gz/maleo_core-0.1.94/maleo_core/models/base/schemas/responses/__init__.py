from .general import BaseGeneralResponsesSchemas
from .client import BaseClientResponsesSchemas
from .service import BaseServiceResponsesSchemas

class BaseResponsesSchemas:
    General = BaseGeneralResponsesSchemas
    Service = BaseServiceResponsesSchemas
    Client = BaseClientResponsesSchemas