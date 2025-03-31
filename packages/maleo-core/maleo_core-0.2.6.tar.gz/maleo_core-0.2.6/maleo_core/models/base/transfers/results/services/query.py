from __future__ import annotations
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
        def serialize_all_uuid(self, value, info:FieldSerializationInfo) -> str:
            """Serializes all UUID to a hex string."""
            if isinstance(value, UUID):
                return str(value)
            return value

        class Config:
            from_attributes=True