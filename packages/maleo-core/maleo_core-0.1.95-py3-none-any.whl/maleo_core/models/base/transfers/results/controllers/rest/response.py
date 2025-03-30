from __future__ import annotations
from enum import Enum
from fastapi import responses

class BaseRESTResponseClass(str, Enum):
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
            BaseRESTResponseClass.NONE: responses.Response,
            BaseRESTResponseClass.HTML: responses.HTMLResponse,
            BaseRESTResponseClass.TEXT: responses.PlainTextResponse,
            BaseRESTResponseClass.JSON: responses.JSONResponse,
            BaseRESTResponseClass.REDIRECT: responses.RedirectResponse,
            BaseRESTResponseClass.STREAMING: responses.StreamingResponse,
            BaseRESTResponseClass.FILE: responses.FileResponse,
        }.get(self, responses.Response)