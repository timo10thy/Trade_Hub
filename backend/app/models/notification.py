from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey, func, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from typing import Optional
from datetime import datetime
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Notification(SQLModel, table=True):
    __tablename__ = "notifications"

    id: str = Field(
        default_factory=generate_uuid,
        sa_column=Column(PG_UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    )
    user_id: str = Field(
        sa_column=Column(PG_UUID(as_uuid=False), ForeignKey("users.id"), index=True, nullable=False)
    )

    type: str = Field(max_length=50)
    message: str = Field()
    is_read: bool = Field(default=False, index=True)
    related_id: Optional[str] = Field(default=None, max_length=36)

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )