from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal, Optional, Any
from maleo_core.models.base.general import BaseGeneralModels

class BaseGeneralResults:
    #* ----- ----- ----- Base ----- ----- ----- *#
    class Base(BaseModel):
        success:bool = Field(..., description="Success status")
        message:Optional[str] = Field(None, description="Optional message")
        description:Optional[str] = Field(None, description="Optional description")

    #* ----- ----- ----- Derived ----- ----- ----- *#
    class Fail(Base):
        success:Literal[False] = Field(False, description="Success status")
        other:Optional[Any] = Field(None, description="Optional other information")

    class SingleData(Base):
        success:Literal[True] = Field(True, description="Success status")
        data:Any = Field(..., description="Fetched data")
        other:Optional[Any] = Field(None, description="Optional other information")

    class MultipleData(
        Base,
        BaseGeneralModels.SimplePagination
    ):
        total_data:int = Field(..., description="Total data count")
        success:Literal[True] = Field(True, description="Success status")
        data:list[Any] = Field(..., description="Paginated data")
        pagination:BaseGeneralModels.ExtendedPagination = Field(..., description="Pagination metadata")
        other:Optional[Any] = Field(None, description="Optional other information")