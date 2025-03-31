from __future__ import annotations
from pydantic import field_validator
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

        class Config:
            from_attributes=True