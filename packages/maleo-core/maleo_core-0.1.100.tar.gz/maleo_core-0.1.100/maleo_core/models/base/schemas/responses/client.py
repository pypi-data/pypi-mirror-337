from __future__ import annotations
from pydantic import Field, model_validator
from typing import Literal, Optional, Self, Any
from maleo_core.models.base.transfers.payloads import BasePayloads
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas

class BaseClientResponsesSchemas:
    class MultipleData(BaseGeneralResponsesSchemas.Base):
        page:int = Field(1, ge=1, description="Page number, must be >= 1.")
        limit:int = Field(10, ge=1, le=100, description="Page size, must be 1 <= limit <= 100.")
        total_data:int = Field(0, description="Total data count")
        success:Literal[True] = Field(True, description="Success status")
        data:list[Any] = Field(..., description="Paginated data")
        pagination:Optional[BasePayloads.Pagination] = Field(..., description="Pagination metadata")
        other:Optional[Any] = Field(None, description="Response's other information")

        @model_validator(mode="after")
        def calculate_pagination_component(self) -> Self:
            self.page = self.pagination.page
            self.limit = self.pagination.limit
            self.total_data = self.pagination.total_data

            return self