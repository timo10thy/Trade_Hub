from sqlmodel import SQLModel
from pydantic import EmailStr, ConfigDict
from typing import Annotated,Optional
from datetime import datetime
from app.models.enum import UserRole,UserStatus


class UserAdminListResponse(SQLModel):
    model_config = ConfigDict(from_attributes=True)   # config first
    id: str
    full_name: str
    email: EmailStr
    phone: str
    role: UserRole
    status: UserStatus
    profile_image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class UserStatusUpdate(SQLModel):
    status: UserStatus
    reason: Optional[str] = None

from app.models.enum import UserRole, UserStatus, PaymentStatus, BookingStatus

class PaymentAdminResponse(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    booking_id: str
    amount: float
    status: PaymentStatus
    provider: Optional[str] = None
    provider_ref: Optional[str] = None
    paid_at: Optional[datetime] = None
    released_at: Optional[datetime] = None
    created_at: datetime