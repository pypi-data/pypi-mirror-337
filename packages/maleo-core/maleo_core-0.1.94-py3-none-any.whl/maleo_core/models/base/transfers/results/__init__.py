from __future__ import annotations
from .general import BaseGeneralResults
from .controllers import BaseControllerResults
from .service import BaseServiceResults
from .query import BaseQueryResults
from .clients import BaseClientResults

class BaseResults:
    General = BaseGeneralResults
    Controller = BaseControllerResults
    Service = BaseServiceResults
    Query = BaseQueryResults
    Client = BaseClientResults