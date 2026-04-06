from sqlmodel import SQLModel
from pydantic import EmailStr, ConfigDict
from typing import Annotated,Optional
from datetime import datetime
from app.models.enum import UserRole,UserStatus


class UserAdminListResponse(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    full_name: str
    email: EmailStr
    phone: str
    role: UserRole
    status: UserStatus
    profile_image_url: Optional[str] = None
    created_at:datetime
    updated_at:datetime

