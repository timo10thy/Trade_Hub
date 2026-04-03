from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey, func, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.models.enum import PaymentStatus
from typing import Optional
from datetime import datetime
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


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
    status: PaymentStatus = Field(default=PaymentStatus.pending, index=True)
    provider_ref: Optional[str] = Field(unique=True, default=None, max_length=255)
    provider: Optional[str] = Field(default="paystack", max_length=20)
    paid_at: Optional[datetime] = Field(default=None)
    released_at: Optional[datetime] = Field(default=None)

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )