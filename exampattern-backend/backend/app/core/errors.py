import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

logger = logging.getLogger(__name__)

_CODES = {
    400: "bad_request", 401: "unauthorized", 403: "forbidden", 404: "not_found",
    409: "conflict", 413: "payload_too_large", 415: "unsupported_media_type",
    422: "validation_error", 429: "rate_limited",
}


def error_response(status: int, message: str, details=None, headers=None) -> JSONResponse:
    body = {"error": {"code": _CODES.get(status, "error"), "message": message}}
    if details is not None:
        body["error"]["details"] = details
    return JSONResponse(status_code=status, content=body, headers=headers)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def _http(_: Request, exc: HTTPException):
        return error_response(exc.status_code, str(exc.detail), headers=exc.headers)

    @app.exception_handler(RequestValidationError)
    async def _validation(_: Request, exc: RequestValidationError):
        details = [
            {"field": ".".join(str(p) for p in e["loc"] if p != "body"), "message": e["msg"]}
            for e in exc.errors()
        ]
        return error_response(422, "Request validation failed", details)

    @app.exception_handler(RateLimitExceeded)
    async def _rate(_: Request, exc: RateLimitExceeded):
        return error_response(429, "Too many requests. Please slow down.")

    @app.exception_handler(Exception)
    async def _unhandled(_: Request, exc: Exception):
        logger.exception("Unhandled error")
        return JSONResponse(
            status_code=500,
            content={"error": {"code": "internal_error", "message": "Something went wrong."}},
        )
