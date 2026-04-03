from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey, func, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.models.enum import DisputeStatus
from typing import Optional
from datetime import datetime
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


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
    status: DisputeStatus = Field(default=DisputeStatus.open, index=True)
    resolution: Optional[str] = Field(default=None)
    resolved_by: Optional[str] = Field(
        sa_column=Column(PG_UUID(as_uuid=False), ForeignKey("users.id"), nullable=True)
    )
    resolved_at: Optional[datetime] = Field(default=None)

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )