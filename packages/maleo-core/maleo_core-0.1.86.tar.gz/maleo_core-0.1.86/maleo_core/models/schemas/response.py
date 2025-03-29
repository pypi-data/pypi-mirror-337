from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional, Self, Any
from maleo_core.models.transfers.results.general import GeneralResults

class BaseResponses:
    #* ----- ----- ----- Base ----- ----- ----- *#
    class Base(BaseModel):
        success:bool = Field(..., description="Response's success status")
        code:str = Field(..., description="Response's code")
        message:str = Field(..., description="Response's message")
        description:str = Field(..., description="Response's description")

    #* ----- ----- ----- Derived ----- ----- ----- *#
    class Fail(Base):
        success:Literal[False] = Field(False, description="Success status")
        other:Optional[Any] = Field(None, description="Response's other information")

    class ServerError(Fail):
        code:str = "MAL-EXC-001"
        message:str = "Unexpected Server Error"
        description:str = "An unexpected error occurred. Please try again later or contact administrator."

    class ValidationError(Fail):
        code:str = "MAL-EXC-002"
        message:str = "Validation Error"
        description:str = "Request validation failed due to missing or invalid fields. Check other for more info."

    class NotFoundError(Fail):
        code:str = "MAL-EXC-003"
        message:str = "Not Found Error"
        description:str = "The resource you requested can not be found. Ensure your request is correct."

    class RateLimitExceeded(Fail):
        code:str = "MAL-RTL-001"
        message:str = "Rate Limit Exceeded"
        description:str = "This resource is requested too many times. Please try again later."

    class Unauthorized(Fail):
        code:str = "MAL-ATH-001"
        message:str = "Unauthorized Request"

    class Forbidden(Fail):
        code:str = "MAL-ATH-002"
        message:str = "Forbidden Request"

    class SingleData(Base):
        success:Literal[True] = Field(True, description="Success status")
        data:Any
        other:Optional[Any] = Field(None, description="Response's other information")

    class MultipleData(Base):
        page:int = Field(1, ge=1, description="Page number, must be >= 1.", exclude=True)
        limit:int = Field(10, ge=1, le=100, description="Page size, must be 1 <= limit <= 100.", exclude=True)
        total_data:int = Field(..., description="Total data count", exclude=True)
        success:Literal[True] = Field(True, description="Success status")
        data:list[Any]
        pagination:Optional[GeneralResults.Pagination] = Field(None, description="Pagination metadata")
        other:Optional[Any] = Field(None, description="Response's other information")

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