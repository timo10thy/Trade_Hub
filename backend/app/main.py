import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.middleware import register_middleware, limiter
from app.db.init_db import init_db

logging.basicConfig(
    level=logging.INFO if settings.ENVIRONMENT == "development" else logging.WARNING,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("tradehub")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting TradeHub API — environment: {settings.ENVIRONMENT}")
    await init_db()
    yield
    logger.info("Shutting down TradeHub API...")


app = FastAPI(
    title="TradeHub API",
    description="Two-sided marketplace for trade professionals in Nigeria",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

register_middleware(app)


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "environment": settings.ENVIRONMENT}


# Routers
from app.api.v1 import auth
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])


