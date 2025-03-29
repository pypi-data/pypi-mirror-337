from enum import Enum
from fastapi import responses

class RESTResponseClass(str, Enum):
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
            RESTResponseClass.NONE: responses.Response,
            RESTResponseClass.HTML: responses.HTMLResponse,
            RESTResponseClass.TEXT: responses.PlainTextResponse,
            RESTResponseClass.JSON: responses.JSONResponse,
            RESTResponseClass.REDIRECT: responses.RedirectResponse,
            RESTResponseClass.STREAMING: responses.StreamingResponse,
            RESTResponseClass.FILE: responses.FileResponse,
        }.get(self, responses.Response)