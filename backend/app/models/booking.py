from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Booking(SQLModel, table=True):
    __tablename__ = "bookings"

    id: str = Field(default_factory=generate_uuid, primary_key=True, max_length=36)
    client_id: str = Field(foreign_key="users.id", index=True, max_length=36)
    professional_id: str = Field(foreign_key="professionals.id", index=True, max_length=36)

    job_type: str = Field(max_length=255)
    job_description: Optional[str] = Field(default=None)
    location: str = Field(max_length=500)
    scheduled_at: Optional[datetime] = Field(default=None)

    # pending | confirmed | in_progress | completed | cancelled | disputed
    status: str = Field(default="pending", max_length=20)

    budget: float = Field(default=0.0)

    # 5% platform commission
    platform_fee: float = Field(default=0.0)

    # Counter-offer from professional
    counter_offer: Optional[float] = Field(default=None)
    counter_offer_note: Optional[str] = Field(default=None)

    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
