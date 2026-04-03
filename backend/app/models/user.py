from sqlmodel import SQLModel, Field
from sqlalchemy import Column, func, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.models.enum import UserRole, UserStatus
from typing import Optional
from datetime import datetime
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(
        default_factory=generate_uuid,
        sa_column=Column(PG_UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    )
    full_name: str = Field(max_length=100, index=True)
    email: str = Field(unique=True, index=True, max_length=255)
    phone: str = Field(unique=True, index=True, max_length=20)
    password_hash: Optional[str] = Field(default=None, max_length=255)
    profile_image_url: Optional[str] = Field(default=None, max_length=500)

    role: UserRole = Field(default=UserRole.client)
    status: UserStatus = Field(default=UserStatus.pending)

    oauth_provider: Optional[str] = Field(default=None, max_length=20)
    oauth_id: Optional[str] = Field(default=None, max_length=255)

    email_verified: bool = Field(default=False)
    phone_verified: bool = Field(default=False)
    two_fa_enabled: bool = Field(default=False)

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    )
