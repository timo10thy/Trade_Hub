from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Professional(SQLModel, table=True):
    __tablename__ = "professionals"

    id: str = Field(default_factory=generate_uuid, primary_key=True, max_length=36)
    user_id: str = Field(foreign_key="users.id", unique=True, index=True, max_length=36)

    trade_category: str = Field(max_length=100)
    bio: Optional[str] = Field(default=None)
    service_area: Optional[str] = Field(default=None, max_length=255)
    years_experience: Optional[int] = Field(default=0)

    # pending | verified | rejected
    verification_status: str = Field(default="pending", max_length=20)

    # free | pro | premium
    subscription_plan: str = Field(default="free", max_length=20)

    # Denormalised — updated via service layer on new review
    avg_rating: float = Field(default=0.0)
    total_jobs: int = Field(default=0)

    # Cloudinary URLs for verification docs
    id_document_url: Optional[str] = Field(default=None, max_length=500)
    licence_url: Optional[str] = Field(default=None, max_length=500)

    hourly_rate: Optional[float] = Field(default=None)

    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
