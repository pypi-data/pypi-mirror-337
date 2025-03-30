from __future__ import annotations
from .result import BaseRESTResult
from .response import BaseRESTResponseClass

class BaseRESTControllerResults:
    Result = BaseRESTResult
    ResponseClass = BaseRESTResponseClass