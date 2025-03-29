from __future__ import annotations
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, model_validator
from typing import Literal
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