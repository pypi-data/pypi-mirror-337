from __future__ import annotations
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional, Self, Any
from ..payloads import BasePayloads

class GeneralResults:
    class Authorization(BaseModel):
        authorized:Literal[False, True]
        response:Optional[JSONResponse] = None
        token:Optional[str] = None

        class Config:
            arbitrary_types_allowed = True

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
        data:Any
        other:Optional[Any] = Field(None, description="Optional other information")

    class MultipleData(Base):
        page:int = Field(..., ge=1, description="Page number, must be >= 1.")
        limit:int = Field(..., ge=1, le=100, description="Page size, must be 1 <= limit <= 100.")
        total_data:int = Field(..., description="Total data count")
        success:Literal[True] = Field(True, description="Success status")
        data:list[Any] = Field(..., description="Paginated data")
        pagination:Optional[BasePayloads.Pagination] = Field(None, description="Pagination metadata")
        other:Optional[Any] = Field(None, description="Optional other information")

        @model_validator(mode="after")
        def calculate_pagination(self) -> Self:
            total_pages = (self.total_data // self.limit) + (1 if self.total_data % self.limit > 0 else 0)

            #* Assign the computed pagination object
            self.pagination = BasePayloads.Pagination(
                page_number=self.page,
                data_count=len(self.data),
                total_data=self.total_data,
                total_pages=total_pages
            )
            return self