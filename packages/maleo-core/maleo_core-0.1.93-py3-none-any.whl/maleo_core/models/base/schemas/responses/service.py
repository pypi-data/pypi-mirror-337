from __future__ import annotations
from pydantic import Field, model_validator
from typing import Literal, Optional, Self, Any
from maleo_core.models.base.transfers.payloads import BasePayloads
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas

class BaseServiceResponsesSchemas:
    class MultipleData(BaseGeneralResponsesSchemas.Base):
        page:int = Field(..., ge=1, description="Page number, must be >= 1.", exclude=True)
        limit:int = Field(..., ge=1, le=100, description="Page size, must be 1 <= limit <= 100.", exclude=True)
        total_data:int = Field(..., description="Total data count", exclude=True)
        success:Literal[True] = Field(True, description="Success status")
        data:list[Any] = Field(..., description="Paginated data")
        pagination:Optional[BasePayloads.Pagination] = Field(None, description="Pagination metadata")
        other:Optional[Any] = Field(None, description="Response's other information")

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