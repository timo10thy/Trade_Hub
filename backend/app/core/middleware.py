from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import time
import logging

from app.core.config import settings

logger = logging.getLogger("tradehub")

# ─── Rate limiter instance (import this in routes) ───────────
limiter = Limiter(key_func=get_remote_address)


def register_middleware(app: FastAPI) -> None:
    """Call this once in main.py to attach all middleware."""

    # 1. CORS
    origins = (
        ["*"]
        if settings.ENVIRONMENT == "development"
        else [
            "https://tradehub.com",
            "https://www.tradehub.com",
        ]
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. Request logging + response time
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration = (time.perf_counter() - start) * 1000  # ms
        logger.info(
            f"{request.method} {request.url.path} "
            f"→ {response.status_code} ({duration:.1f}ms)"
        )
        response.headers["X-Response-Time"] = f"{duration:.1f}ms"
        return response

    # 3. Rate limit exceeded handler
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Too many requests. Please slow down."},
        )