from __future__ import annotations
from .schemas import BaseSchemas
from .transfers import BaseTransfers

class BaseModels:
    Transfers = BaseTransfers
    Schemas = BaseSchemas