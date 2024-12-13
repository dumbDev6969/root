from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from utils.logger import get_logger

logger = get_logger(__name__)

class AppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

class DatabaseException(AppException):
    def __init__(self, detail: str):
        super().__init__(500, f"Database error: {detail}")

class AuthenticationException(AppException):
    def __init__(self, detail: str):
        super().__init__(401, f"Authentication error: {detail}")

class AuthorizationException(AppException):
    def __init__(self, detail: str):
        super().__init__(403, f"Authorization error: {detail}")

class ValidationException(AppException):
    def __init__(self, detail: str):
        super().__init__(422, f"Validation error: {detail}")

async def error_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, AppException):
        logger.error(f"{exc.__class__.__name__}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )
    elif isinstance(exc, HTTPException):
        logger.error(f"HTTPException: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )
    else:
        logger.error(f"Unexpected error: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"error": "An unexpected error occurred"}
        )

def setup_error_handlers(app):
    app.add_exception_handler(AppException, error_handler)
    app.add_exception_handler(Exception, error_handler)
