from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default_factory=generate_uuid, primary_key=True, max_length=36)
    full_name: str = Field(max_length=100)
    email: str = Field(unique=True, index=True, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=20)
    password_hash: Optional[str] = Field(default=None, max_length=255)

    # client | professional | admin
    role: str = Field(default="client", max_length=20)

    # pending | active | suspended
    status: str = Field(default="pending", max_length=20)

    # OAuth
    oauth_provider: Optional[str] = Field(default=None, max_length=20)
    oauth_id: Optional[str] = Field(default=None, max_length=255)

    # Verification flags
    email_verified: bool = Field(default=False)
    phone_verified: bool = Field(default=False)

    # 2FA
    two_fa_enabled: bool = Field(default=False)

    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
