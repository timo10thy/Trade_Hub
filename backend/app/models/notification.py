from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Notification(SQLModel, table=True):
    __tablename__ = "notifications"

    id: str = Field(default_factory=generate_uuid, primary_key=True, max_length=36)
    user_id: str = Field(foreign_key="users.id", index=True, max_length=36)

    # e.g. booking_confirmed | payment_released | booking_cancelled
    type: str = Field(max_length=50)

    message: str = Field()
    is_read: bool = Field(default=False)

    # Optional link to related entity
    related_id: Optional[str] = Field(default=None, max_length=36)

    created_at: datetime = Field(default_factory=utcnow)
