from sqlmodel import SQLModel
from pydantic import EmailStr, ConfigDict
from typing import Annotated,Optional
from datetime import datetime
from app.models.enum import UserRole, UserStatus, PaymentStatus, BookingStatus, DisputeStatus, VerificationStatus



class UserAdminListResponse(SQLModel):
    model_config = ConfigDict(from_attributes=True)   
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


class DisputeAdminResponse(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    booking_id: str
    raised_by: str
    reason: str
    status: DisputeStatus
    resolution: Optional[str] = None
    resolved_by: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime

class DisputeResolve(SQLModel):
    resolution: str
    action: str 


class ProfessionalAdminResponse(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    trade_category: str
    bio: Optional[str] = None
    service_area: Optional[str] = None
    years_experience: Optional[int] = None
    nin: Optional[str] = None
    verification_status: VerificationStatus
    id_document_url: Optional[str] = None
    licence_url: Optional[str] = None
    certification_url: Optional[str] = None
    created_at: datetime

class ProfessionalVerificationUpdate(SQLModel):
    verification_status: VerificationStatus
    reason: Optional[str] = None