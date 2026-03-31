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


class Dispute(SQLModel, table=True):
    __tablename__ = "disputes"

    id: str = Field(
        default_factory=generate_uuid,
        sa_column=Column(PG_UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    )
    booking_id: str = Field(
        sa_column=Column(PG_UUID(as_uuid=False), ForeignKey("bookings.id"), unique=True, index=True, nullable=False)
    )
    raised_by: str = Field(
        sa_column=Column(PG_UUID(as_uuid=False), ForeignKey("users.id"), index=True, nullable=False)
    )

    reason: str = Field()

    # open | under_review | resolved
    status: str = Field(default="open", max_length=20)

    resolution: Optional[str] = Field(default=None)
    resolved_by: Optional[str] = Field(
        sa_column=Column(PG_UUID(as_uuid=False), ForeignKey("users.id"), nullable=True)
    )
    resolved_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=utcnow)
