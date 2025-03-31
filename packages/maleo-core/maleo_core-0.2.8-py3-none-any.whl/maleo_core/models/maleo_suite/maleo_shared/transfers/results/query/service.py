from __future__ import annotations
from pydantic import Field
from uuid import UUID
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults

class MaleoSharedServiceQueryResults:
    class Get(BaseServiceQueryResults.Get):
        secret:UUID = Field(..., description="Service's secret")
        name:str = Field(..., description="Service's name")