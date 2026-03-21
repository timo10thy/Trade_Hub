from sqlmodel import SQLModel
from app.db.session import engine
from app.core.config import settings
import logging

logger = logging.getLogger("tradehub")


async def init_db() -> None:
    """
    Creates all tables if they don't exist.
    - Dev only — in production always use Alembic migrations.
    - Will NOT drop or modify existing tables.
    """
    # Import all models so SQLModel.metadata knows about them
    from app.models import (
        user,
        professional,
        portfolio,
        booking,
        payment,
        review,
        dispute,
        notification,
    )

    if settings.ENVIRONMENT == "development":
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
            logger.info("Database tables verified/created.")
    else:
        logger.info("Skipping init_db — use Alembic in production.")
