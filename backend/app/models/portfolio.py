from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Portfolio(SQLModel, table=True):
    __tablename__ = "portfolios"

    id: str = Field(default_factory=generate_uuid, primary_key=True, max_length=36)
    professional_id: str = Field(foreign_key="professionals.id", index=True, max_length=36)

    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)

    # Cloudinary URL
    media_url: str = Field(max_length=500)

    # photo | video
    media_type: str = Field(default="photo", max_length=10)

    # Trade category tag
    trade_tag: Optional[str] = Field(default=None, max_length=100)

    # pending | approved | rejected
    moderation_status: str = Field(default="pending", max_length=20)

    uploaded_at: datetime = Field(default_factory=utcnow)
