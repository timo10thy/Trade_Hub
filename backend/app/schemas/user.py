from sqlmodel import SQLModel
from pydantic import EmailStr, field_validator
from typing import Annotated,Optional
from pydantic import StringConstraints, ConfigDict
from datetime import datetime
from app.models.enum import UserRole,UserStatus



FullName = Annotated[str, StringConstraints(min_length=3, max_length=100, strip_whitespace=True)]


class UserCreate(SQLModel):
    full_name: FullName
    email: EmailStr
    phone: str
    password: str
    role: UserRole = UserRole.client

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Password cannot be empty or whitespace")
        if len(v) < 8 or len(v) > 20:
            raise ValueError("Password must be between 8 and 20 characters")
        if not any(c.isalpha() for c in v):
            raise ValueError("Password must contain at least one letter")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Phone number cannot be empty")
        if not v.startswith("+"):
            raise ValueError("Phone number must start with country code e.g. +234")
        if not v[1:].isdigit():
            raise ValueError("Phone number must contain only digits after country code")
        if len(v) < 10 or len(v) > 15:
            raise ValueError("Phone number must be between 10 and 15 characters")
        return v

class UserResponse(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    full_name: str
    email: str
    phone: str
    profile_image_url: Optional[str] = None
    role: UserRole
    status: UserStatus
    email_verified: bool
    phone_verified: bool
    two_fa_enabled: bool
    created_at:datetime
    updated_at:datetime

class UserAdminResponse(UserResponse):
    id: str
    oauth_provider: Optional[str] = None

class UserLogin(SQLModel):
    email: EmailStr
    password: str

class TokenResponse(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse

class RefreshTokenRequest(SQLModel):
    refresh_token: str

class PasswordChange(SQLModel):
    old_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Password cannot be empty or whitespace")
        if len(v) < 8 or len(v) > 20:
            raise ValueError("Password must be between 8 and 20 characters")
        if not any(c.isalpha() for c in v):
            raise ValueError("Password must contain at least one letter")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        return v
    

class UserUpdate(SQLModel):
    full_name: Optional[FullName] = None
    phone: Optional[str] = None
    profile_image_url: Optional[str] = None

