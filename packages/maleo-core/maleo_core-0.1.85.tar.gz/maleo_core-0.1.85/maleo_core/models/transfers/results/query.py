from __future__ import annotations
from datetime import datetime, date
from pydantic import BaseModel, field_serializer, field_validator
from uuid import UUID
from maleo_core.models.transfers.results.general import GeneralResults

class QueryResults:
    class Get(BaseModel):
        id:int
        uuid:UUID
        created_at:datetime
        updated_at:datetime
        is_deleted:bool
        is_active:bool

        @field_validator('*', mode="before")
        def set_none(cls, values):
            if isinstance(values, str) and (values == "" or len(values) == 0):
                return None
            return values

        @field_serializer('*')
        def serialize_values(self, values):
            if isinstance(values, datetime) or isinstance(values, date):
                return values.isoformat()
            if isinstance(values, UUID):
                return str(values)
            return values

        class Config:
            from_attributes=True

    Fail = GeneralResults.Fail
    SingleData = GeneralResults.SingleData
    MultipleData = GeneralResults.MultipleData