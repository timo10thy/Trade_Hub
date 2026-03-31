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


class Booking(SQLModel, table=True):
    __tablename__ = "bookings"

    id: str = Field(
        default_factory=generate_uuid,
        sa_column=Column(PG_UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    )
    client_id: str = Field(
        sa_column=Column(PG_UUID(as_uuid=False), ForeignKey("users.id"), index=True, nullable=False)
    )
    professional_id: str = Field(
        sa_column=Column(PG_UUID(as_uuid=False), ForeignKey("professionals.id"), index=True, nullable=False)
    )

    job_type: str = Field(max_length=255)
    job_description: Optional[str] = Field(default=None)
    location: str = Field(max_length=500)
    scheduled_at: Optional[datetime] = Field(default=None)

    # pending | confirmed | in_progress | completed | cancelled | disputed
    status: str = Field(default="pending", max_length=20)

    budget: float = Field(default=0.0)
    platform_fee: float = Field(default=0.0)
    counter_offer: Optional[float] = Field(default=None)
    counter_offer_note: Optional[str] = Field(default=None)

    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
