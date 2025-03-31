from __future__ import annotations
from datetime import datetime, date, timedelta, timezone
from enum import Enum
from pydantic import BaseModel, Field, field_serializer, model_validator
from pydantic_core.core_schema import FieldSerializationInfo
from typing import Dict, List, Literal, Optional, Union
from uuid import UUID
from maleo_core.utils.constants import REFRESH_TOKEN_DURATION_DAYS, ACCESS_TOKEN_DURATION_MINUTES

class BaseGeneralModels:
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

    class Identifiers(BaseModel):
        id:int = Field(..., description="Data's ID, must be >= 1.")
        uuid:UUID = Field(..., description="Data's UUID.")

        @field_serializer('uuid')
        def serialize_uuid(self, value:UUID, info:FieldSerializationInfo) -> str:
            """Serializes UUID to a hex string."""
            return str(value)

    class Timestamp(BaseModel):
        created_at:datetime = Field(..., description="Data's created_at timestamp")
        updated_at:datetime = Field(..., description="Data's updated_at timestamp")

        @field_serializer('created_at', 'updated_at')
        def serialize_timestamps(self, value:Union[datetime, date], info:FieldSerializationInfo) -> str:
            """Serializes datetime/date fields to ISO format."""
            return value.isoformat()

    class Status(BaseModel):
        is_deleted:Optional[bool] = Field(None, description="Data's deletion status.")
        is_active:Optional[bool] = Field(None, description="Data's active status.")

    class SimplePagination(BaseModel):
        page:int = Field(1, ge=1, description="Page number, must be >= 1.")
        limit:int = Field(10, ge=1, le=100, description="Page size, must be 1 <= limit <= 100.")

    class ExtendedPagination(SimplePagination):
        data_count:int = Field(..., description="Fetched data count")
        total_data:int = Field(..., description="Total data count")
        total_pages:int = Field(..., description="Total pages count")

    class SortOrder(str, Enum):
        ASC = "asc"
        DESC = "desc"

    class SortColumn(BaseModel):
        name:str = Field(..., description="Column name.")
        order:BaseGeneralModels.SortOrder = Field(..., description="Sort order.")

    class DateFilter(BaseModel):
        name:str = Field(..., description="Column name.")
        from_date:Optional[datetime] = Field(None, description="From date.")
        to_date:Optional[datetime] = Field(None, description="To date.")

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