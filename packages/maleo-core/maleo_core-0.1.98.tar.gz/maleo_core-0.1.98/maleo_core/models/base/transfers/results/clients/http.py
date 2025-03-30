from httpx import Response
from pydantic import BaseModel, Field
from typing import Any

class BaseHTTPClientResults(BaseModel):
    response:Response = Field(..., description="HTTP Client's response")
    status_code:int = Field(..., description="HTTP Client's response status code")
    content:Any = Field(..., description="HTTP Client's response content")
    success:bool = Field(..., description="HTTP Client's success status")

    class Config:
        arbitrary_types_allowed=True