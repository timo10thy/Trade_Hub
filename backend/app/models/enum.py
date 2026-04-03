from enum import Enum

class UserRole(str, Enum):
    client = "client"
    professional = "professional"
    admin = "admin"



class UserStatus(str, Enum):
    pending = "pending"
    active = "active"
    suspended = "suspended"


class VerificationStatus(str, Enum):
    pending = "pending"
    verified = "verified"
    rejected = "rejected"

class SubscriptionPlan(str, Enum):
    free = "free"
    pro = "pro"
    premium = "premium"

class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"
    disputed = "disputed"

class PaymentStatus(str, Enum):
    pending = "pending"
    held = "held"
    released = "released"
    refunded = "refunded"

class MediaType(str, Enum):
    photo = "photo"
    video = "video"

class DisputeStatus(str, Enum):
    open = "open"
    under_review = "under_review"
    resolved = "resolved"

class ModerationStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"