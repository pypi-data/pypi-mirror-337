from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Union
from uuid import UUID
from maleo_core.models.base.general import BaseGeneralModels

class BaseGeneralParameters:
    class Expand(BaseModel):
        expand:list[str] = Field([], description="Expanded field(s)")

    class StatusUpdateAction(str, Enum):
        ACTIVATE = "activate"
        DEACTIVATE = "deactivate"
        RESTORE = "restore"
        DELETE = "delete"

    class StatusUpdate(BaseModel):
        action:BaseGeneralParameters.StatusUpdateAction = Field(..., description="Status update's action to be executed")

    class Search(BaseModel):
        search:Optional[str] = Field(None, description="Search parameter string.")

    class Sorts(BaseModel):
        sort:list[str] = Field(["id.asc"], description="Sorting columns in 'column_name.asc' or 'column_name.desc' format.")

    class Filters(BaseModel):
        filter:list[str] = Field([], description="Filters for date range, e.g. 'created_at|from::<ISO_DATETIME>|to::<ISO_DATETIME>'.")

    class SortColumns(BaseModel):
        sort_columns:list[BaseGeneralModels.SortColumn] = Field([BaseGeneralModels.SortColumn(name="id", order=BaseGeneralModels.SortOrder.ASC)], description="List of columns to be sorted")

    class DateFilters(BaseModel):
        date_filters:list[BaseGeneralModels.DateFilter] = Field([], description="Date filters to be applied")

    class Identifiers(str, Enum):
        ID = "id"
        UUID = "uuid"

    class GetSingle(BaseGeneralModels.Status):
        identifier:BaseGeneralParameters.Identifiers = Field(..., description="Identifier")
        value:Union[int, UUID] = Field(..., description="Value")