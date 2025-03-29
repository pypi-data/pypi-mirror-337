from __future__ import annotations
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, Field, model_validator
from typing import Literal, Self, Any
from uuid import UUID
from maleo_core.utils.constants import REFRESH_TOKEN_DURATION_DAYS, ACCESS_TOKEN_DURATION_MINUTES

class BasePayloads:
    class Token(BaseModel):
        id:int
        uuid:UUID
        role_id:int
        scope:Literal["refresh", "access"]
        iat:datetime = datetime.now(timezone.utc)
        exp:datetime

        @model_validator(mode="before")
        def set_iat_and_exp(cls, values:dict):
            iat = values.get("iat", None)
            exp = values.get("iat", None)
            if not iat and not exp:
                iat = datetime.now(timezone.utc)
                values["iat"] = iat
                if values["scope"] == "refresh":
                    values["exp"] = iat + timedelta(days=REFRESH_TOKEN_DURATION_DAYS)
                elif values["scope"] == "access":
                    values["exp"] = iat + timedelta(minutes=ACCESS_TOKEN_DURATION_MINUTES)
            return values

    class Pagination(BaseModel):
        limit:int = Field(..., ge=1, le=100, description="Page size, must be 1 <= limit <= 100.", exclude=True)
        data:list[Any] = Field(..., description="Paginated data", exclude=True)
        page_number:int = Field(..., ge=1, description="Page number, must be >= 1.")
        data_count:int = Field(0, description="Fetched data count")
        total_data:int = Field(..., description="Total data count")
        total_pages:int = Field(1, description="Total pages count")

        @model_validator(mode="after")
        def calculate(self) -> Self:
            self.data_count = len(self.data)
            self.total_pages = (self.total_data // self.limit) + (1 if self.total_data % self.limit > 0 else 0)
            return self