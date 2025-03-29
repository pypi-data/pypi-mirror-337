from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, List, Literal, Optional, Union

class GeneralParameters:
    class AllowedMethods(str, Enum):
        OPTIONS = "OPTIONS"
        GET = "GET"
        POST = "POST"
        PATCH = "PATCH"
        PUT = "PUT"
        DELETE = "DELETE"
        ALL = "*"

    AllowedRoles = Union[List[int], Literal["*"]]
    RoutesPermissions = Dict[str, Dict[AllowedMethods, AllowedRoles]]

    class Expand(BaseModel):
        expand:list[str] = Field([], description="Expanded field(s)")

    class StatusUpdateAction(str, Enum):
        ACTIVATE = "activate"
        DEACTIVATE = "deactivate"
        RESTORE = "restore"
        DELETE = "delete"

    class StatusUpdate(BaseModel):
        action:GeneralParameters.StatusUpdateAction = Field(..., description="Status update's action to be executed")

    class Check(BaseModel):
        is_deleted:Optional[bool] = Field(None, description="Filter results based on deletion status.")
        is_active:Optional[bool] = Field(None, description="Filter results based on active status.")

    class Pagination(BaseModel):
        page:int = Field(1, ge=1, description="Page number, must be >= 1.")
        limit:int = Field(10, ge=1, le=100, description="Page size, must be 1 <= limit <= 100.")

    class Search(BaseModel):
        search:Optional[str] = Field(None, description="Search parameter string.")

    class Sorts(BaseModel):
        sort:list[str] = Field(["id.asc"], description="Sorting columns in 'column_name.asc' or 'column_name.desc' format.")

    class Filters(BaseModel):
        filter:list[str] = Field([], description="Filters for date range, e.g. 'created_at|from::<ISO_DATETIME>|to::<ISO_DATETIME>'.")

    class SortOrder(str, Enum):
        ASC = "asc"
        DESC = "desc"

    class SortColumn(BaseModel):
        name:str = Field(..., description="Column name.")
        order:GeneralParameters.SortOrder = Field(..., description="Sort order.")

    class DateFilter(BaseModel):
        name:str = Field(..., description="Column name.")
        from_date:Optional[datetime] = Field(None, description="From date.")
        to_date:Optional[datetime] = Field(None, description="To date.")