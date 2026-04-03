from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey,func, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.models.enum import VerificationStatus, SubscriptionPlan
from typing import Optional
from datetime import datetime
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Professional(SQLModel, table=True):
    __tablename__ = "professionals"

    id: str = Field(
        default_factory=generate_uuid,
        sa_column=Column(PG_UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    )
    user_id: str = Field(
        sa_column=Column(PG_UUID(as_uuid=False), ForeignKey("users.id"), unique=True, index=True, nullable=False)
    )

    trade_category: str = Field(max_length=100, index=True)
    bio: Optional[str] = Field(default=None)
    service_area: Optional[str] = Field(default=None, max_length=255, index=True)
    years_experience: Optional[int] = Field(default=0)
    nin: Optional[str] = Field(unique=True, default=None, max_length=11)

    # pending | verified | rejected

    verification_status: VerificationStatus = Field(default=VerificationStatus.pending, index=True)
    subscription_plan: SubscriptionPlan = Field(default=SubscriptionPlan.free, index=True)

    avg_rating: float = Field(default=0.0)
    total_jobs: int = Field(default=0)

    id_document_url: Optional[str] = Field(default=None, max_length=500)
    licence_url: Optional[str] = Field(default=None, max_length=500)
    hourly_rate: Optional[float] = Field(default=None)


    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    )

