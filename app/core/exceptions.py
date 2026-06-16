from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(self, message: str, error_code: str = "APP_ERROR", status_code: int = status.HTTP_400_BAD_REQUEST, details: dict | None = None):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


def success_response(data, message: str = "Success", meta: dict | None = None):
    return {"success": True, "message": message, "data": data, "meta": meta or {}}


def error_response(message: str, error_code: str = "ERROR", details: dict | None = None):
    return {"success": False, "message": message, "error_code": error_code, "details": details or {}}


def install_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(_: Request, exc: AppError):
        return JSONResponse(status_code=exc.status_code, content=error_response(exc.message, exc.error_code, exc.details))

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(_: Request, exc: RequestValidationError):
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=error_response("Validation failed", "VALIDATION_ERROR", {"errors": exc.errors()}))
