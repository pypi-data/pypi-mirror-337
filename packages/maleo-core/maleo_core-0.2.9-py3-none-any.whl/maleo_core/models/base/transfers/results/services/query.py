from __future__ import annotations
from datetime import datetime, date
from pydantic import field_validator, field_serializer
from pydantic_core.core_schema import FieldSerializationInfo
from uuid import UUID
from maleo_core.models.base.general import BaseGeneralModels

class BaseServiceQueryResults:
    class Get(
        BaseGeneralModels.Status,
        BaseGeneralModels.Timestamp,
        BaseGeneralModels.Identifiers
    ):
        @field_validator('*', mode="before")
        def set_none(cls, values):
            if isinstance(values, str) and (values == "" or len(values) == 0):
                return None
            return values
        
        @field_serializer('*')
        def serialize_fields(self, value, info:FieldSerializationInfo) -> str:
            """Serializes all unique-typed fields."""
            if isinstance(value, UUID):
                return str(value)
            if isinstance(value, datetime) or isinstance(value, date):
                return value.isoformat()
            return value

        class Config:
            from_attributes=True