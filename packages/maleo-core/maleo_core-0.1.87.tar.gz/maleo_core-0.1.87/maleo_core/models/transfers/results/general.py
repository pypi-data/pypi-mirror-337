from __future__ import annotations
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional, Self, Any

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

    class Pagination(BaseModel):
        page_number:int = Field(..., ge=1, description="Page number, must be >= 1.")
        data_count:int = Field(0, description="Fetched data count")
        total_data:int = Field(..., description="Total data count")
        total_pages:int = Field(1, description="Total pages count")

    class MultipleData(Base):
        page:int = Field(1, ge=1, description="Page number, must be >= 1.", exclude=True)
        limit:int = Field(10, ge=1, le=100, description="Page size, must be 1 <= limit <= 100.", exclude=True)
        total_data:int = Field(..., description="Total data count", exclude=True)
        success:Literal[True] = Field(True, description="Success status")
        data:list[Any]
        pagination:Optional[GeneralResults.Pagination] = Field(None, description="Pagination metadata")
        other:Optional[Any] = Field(None, description="Optional other information")

        @model_validator(mode="after")
        def calculate_pagination(self) -> Self:
            total_data = self.total_data
            total_pages = (total_data // self.limit) + (1 if total_data % self.limit > 0 else 0)

            #* Assign the computed pagination object
            self.pagination = GeneralResults.Pagination(
                page_number=self.page,
                data_count=len(self.data),
                total_data=total_data,
                total_pages=total_pages
            )
            return self