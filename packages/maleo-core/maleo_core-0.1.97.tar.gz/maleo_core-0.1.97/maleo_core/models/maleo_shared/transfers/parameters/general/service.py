from __future__ import annotations
from enum import Enum
from pydantic import Field
from typing import Union
from uuid import UUID
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters

class MaleoSharedServiceGeneralParameters:
    class GetSingleIdentifiers(str, Enum):
        ID = "id"
        UUID = "uuid"
        NAME = "name"

    class GetSingle(BaseGeneralParameters.Check):
        identifier:MaleoSharedServiceGeneralParameters.GetSingleIdentifiers = Field(..., description="Identifier")
        value:Union[int, UUID, str] = Field(..., description="Value")