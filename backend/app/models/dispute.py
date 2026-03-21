from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Dispute(SQLModel, table=True):
    __tablename__ = "disputes"

    id: str = Field(default_factory=generate_uuid, primary_key=True, max_length=36)
    booking_id: str = Field(foreign_key="bookings.id", unique=True, index=True, max_length=36)
    raised_by: str = Field(foreign_key="users.id", index=True, max_length=36)

    reason: str = Field()

    # open | under_review | resolved
    status: str = Field(default="open", max_length=20)

    resolution: Optional[str] = Field(default=None)
    resolved_by: Optional[str] = Field(foreign_key="users.id", default=None, max_length=36)
    resolved_at: Optional[datetime] = Field(default=None)

    created_at: datetime = Field(default_factory=utcnow)
