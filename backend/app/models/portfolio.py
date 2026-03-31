from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from typing import Optional
from datetime import datetime, timezone
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Portfolio(SQLModel, table=True):
    __tablename__ = "portfolios"

    id: str = Field(
        default_factory=generate_uuid,
        sa_column=Column(PG_UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    )
    professional_id: str = Field(
        sa_column=Column(PG_UUID(as_uuid=False), ForeignKey("professionals.id"), index=True, nullable=False)
    )

    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    media_url: str = Field(max_length=500)

    # photo | video
    media_type: str = Field(default="photo", max_length=10)
    trade_tag: Optional[str] = Field(default=None, max_length=100)

    # pending | approved | rejected
    moderation_status: str = Field(default="pending", max_length=20)

    uploaded_at: datetime = Field(default_factory=utcnow)
