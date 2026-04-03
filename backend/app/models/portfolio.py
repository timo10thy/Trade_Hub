from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey, func, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.models.enum import MediaType, ModerationStatus
from typing import Optional
from datetime import datetime
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


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
    media_type: MediaType = Field(default=MediaType.photo)
    trade_tag: Optional[str] = Field(default=None, max_length=100)
    moderation_status: ModerationStatus = Field(default=ModerationStatus.pending, index=True)

    uploaded_at: Optional[datetime] = Field(
    default=None,
    sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
)