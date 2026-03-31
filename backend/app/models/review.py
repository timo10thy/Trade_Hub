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


class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    id: str = Field(
        default_factory=generate_uuid,
        sa_column=Column(PG_UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    )
    booking_id: str = Field(
        sa_column=Column(PG_UUID(as_uuid=False), ForeignKey("bookings.id"), unique=True, index=True, nullable=False)
    )
    reviewer_id: str = Field(
        sa_column=Column(PG_UUID(as_uuid=False), ForeignKey("users.id"), index=True, nullable=False)
    )
    reviewee_id: str = Field(
        sa_column=Column(PG_UUID(as_uuid=False), ForeignKey("users.id"), index=True, nullable=False)
    )

    # 1 to 5
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = Field(default=None)
    response: Optional[str] = Field(default=None)
    responded_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=utcnow)
