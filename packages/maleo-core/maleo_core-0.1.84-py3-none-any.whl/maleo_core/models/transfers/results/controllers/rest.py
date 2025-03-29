from enum import Enum
from fastapi import responses
from fastapi import status
from pydantic import BaseModel, Field
from typing import Any

class ResponseClass(str, Enum):
    NONE = "none"
    HTML = "html"
    TEXT = "text"
    JSON = "json"
    REDIRECT = "redirect"
    STREAMING = "streaming"
    FILE = "file"

    def get_response_class(self) -> type[responses.Response]:
        """Returns the corresponding FastAPI Response class."""
        return {
            ResponseClass.NONE: responses.Response,
            ResponseClass.HTML: responses.HTMLResponse,
            ResponseClass.TEXT: responses.PlainTextResponse,
            ResponseClass.JSON: responses.JSONResponse,
            ResponseClass.REDIRECT: responses.RedirectResponse,
            ResponseClass.STREAMING: responses.StreamingResponse,
            ResponseClass.FILE: responses.FileResponse,
        }.get(self, responses.Response)

class RESTControllerResults(BaseModel):
    success:bool = Field(..., description="REST Controller's success status")
    response_class:ResponseClass = Field(ResponseClass.JSON, description="REST Controller's response class")
    content:Any = Field(..., description="REST Controller's response content")
    status_code:int = Field(status.HTTP_200_OK, description="REST Controller's response status code")

    class Config:
        arbitrary_types_allowed=True

    def to_response(self) -> responses.Response:
        """Dynamically creates a response based on response_class."""
        response_cls = self.response_class.get_response_class()
        return response_cls(content=self.content, status_code=self.status_code)