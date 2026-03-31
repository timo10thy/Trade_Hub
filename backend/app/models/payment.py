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


class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    id: str = Field(
        default_factory=generate_uuid,
        sa_column=Column(PG_UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    )
    booking_id: str = Field(
        sa_column=Column(PG_UUID(as_uuid=False), ForeignKey("bookings.id"), unique=True, index=True, nullable=False)
    )

    amount: float = Field(default=0.0)

    # pending | held | released | refunded
    status: str = Field(default="pending", max_length=20)

    provider_ref: Optional[str] = Field(default=None, max_length=255)

    # paystack | flutterwave
    provider: Optional[str] = Field(default="paystack", max_length=20)

    paid_at: Optional[datetime] = Field(default=None)
    released_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=utcnow)
