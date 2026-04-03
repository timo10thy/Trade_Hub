from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey, func, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from typing import Optional
from datetime import datetime
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


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

    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = Field(default=None)
    response: Optional[str] = Field(default=None)
    responded_at: Optional[datetime] = Field(default=None)

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )