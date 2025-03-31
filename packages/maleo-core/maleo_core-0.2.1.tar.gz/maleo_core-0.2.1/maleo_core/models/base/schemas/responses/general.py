from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal, Optional, Any
from maleo_core.models.base.general import BaseGeneralModels

class BaseGeneralResponsesSchemas:
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
        data:Any = Field(..., description="Fetched data")
        other:Optional[Any] = Field(None, description="Response's other information")

    class MultipleData(Base):
        page:int = Field(..., ge=1, description="Page number, must be >= 1.", exclude=True)
        limit:int = Field(..., ge=1, le=100, description="Page size, must be 1 <= limit <= 100.", exclude=True)
        total_data:int = Field(..., description="Total data count", exclude=True)
        success:Literal[True] = Field(True, description="Success status")
        data:list[Any] = Field(..., description="Paginated data")
        pagination:BaseGeneralModels.ExtendedPagination = Field(..., description="Pagination metadata")
        other:Optional[Any] = Field(None, description="Optional other information")