from __future__ import annotations
from .general import BaseGeneralParameters
from .service import BaseServiceParameters
from .client import BaseClientParameters

class BaseParameters:
    General = BaseGeneralParameters
    Service = BaseServiceParameters
    Client = BaseClientParameters