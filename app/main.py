from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.exceptions import install_exception_handlers, success_response
from app.core.logging import configure_logging
from app.middleware.request_logging import RequestLoggingMiddleware

configure_logging()
settings = get_settings()
app = FastAPI(title=settings.app_name)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
install_exception_handlers(app)
app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/health")
def health():
    return success_response({"status": "ok"}, "Backend healthy")
