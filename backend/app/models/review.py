from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    id: str = Field(default_factory=generate_uuid, primary_key=True, max_length=36)
    booking_id: str = Field(foreign_key="bookings.id", unique=True, index=True, max_length=36)
    reviewer_id: str = Field(foreign_key="users.id", index=True, max_length=36)
    reviewee_id: str = Field(foreign_key="users.id", index=True, max_length=36)

    # 1 to 5
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = Field(default=None)

    # Professional public response
    response: Optional[str] = Field(default=None)
    responded_at: Optional[datetime] = Field(default=None)

    created_at: datetime = Field(default_factory=utcnow)
