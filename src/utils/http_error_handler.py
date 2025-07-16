from typing import Any
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware


class HTTPErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Any) -> Response | JSONResponse:
        try:
            return await call_next(request)
        except Exception as ex:
            content: str = f"exc: {str(ex)}"
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
            return JSONResponse(content, status_code=status_code)
