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


class Professional(SQLModel, table=True):
    __tablename__ = "professionals"

    id: str = Field(
        default_factory=generate_uuid,
        sa_column=Column(PG_UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    )
    user_id: str = Field(
        sa_column=Column(PG_UUID(as_uuid=False), ForeignKey("users.id"), unique=True, index=True, nullable=False)
    )

    trade_category: str = Field(max_length=100)
    bio: Optional[str] = Field(default=None)
    service_area: Optional[str] = Field(default=None, max_length=255)
    years_experience: Optional[int] = Field(default=0)

    # pending | verified | rejected

    verification_status: str = Field(default="pending", max_length=20)

    # free | pro | premium

    subscription_plan: str = Field(default="free", max_length=20)

    avg_rating: float = Field(default=0.0)
    total_jobs: int = Field(default=0)

    id_document_url: Optional[str] = Field(default=None, max_length=500)
    licence_url: Optional[str] = Field(default=None, max_length=500)
    hourly_rate: Optional[float] = Field(default=None)

    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
