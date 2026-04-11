from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List, Optional
from datetime import datetime

from app.core.dependencies import require_admin
from app.db.session import get_session
from app.models.user import User
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.dispute import Dispute
from app.models.professional import Professional
from app.models.enum import UserStatus, UserRole, PaymentStatus, BookingStatus, DisputeStatus
from app.schemas.admin import UserAdminListResponse, UserStatusUpdate, PaymentAdminResponse, DisputeAdminResponse, DisputeResolve
from app.services.sms_service import send_sms
from app.services.notification_service import create_notification

router = APIRouter()

@router.get("/users", response_model=List[UserAdminListResponse], status_code=status.HTTP_200_OK)
async def get_all_users(
    limit: int = 20,
    offset: int = 0,
    status: Optional[UserStatus] = None,
    role: Optional[UserRole] = None,
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(require_admin)
):
    
    query = select(User)
    if status:
        query = query.where(User.status == status)
    if role:
        query = query.where(User.role == role)
    result = await session.exec(query.offset(offset).limit(limit))
    users = result.all()
    return users

@router.get("/users/{user_id}", response_model=UserAdminListResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(require_admin)
):
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/users/{user_id}/status", response_model=UserAdminListResponse, status_code=status.HTTP_200_OK)
async def user_status_verify(
    user_id: str,
    status_update: UserStatusUpdate,
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(require_admin)
):
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = status_update.status
    session.add(user)
    await session.commit()
    await session.refresh(user)
    if status_update.status == UserStatus.active:
        send_sms(
            user.phone,
            "Your TradeHub account has been approved. Login at: https://tradehub.com/login"
        )
        await create_notification(
            session,
            user.id,
            "account_verified",
            "Your account has been approved. You can now access the platform."
        )
    elif status_update.status == UserStatus.suspended:
        send_sms(user.phone, f"Your TradeHub account has been suspended. Reason: {status_update.reason or 'Policy violation'}")
        await create_notification(session, user.id, "account_suspended", f"Your account has been suspended. Reason: {status_update.reason or 'Policy violation'}")
    return user


@router.get("/payments/pending-release", response_model=List[PaymentAdminResponse], status_code=status.HTTP_200_OK)
async def get_pending_release_payments(
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(require_admin)
):
    query = (
        select(Payment)
        .join(Booking, Payment.booking_id == Booking.id)
        .where(Payment.status == PaymentStatus.held)
        .where(Booking.status == BookingStatus.completed)
    )
    result = await session.exec(query)
    return result.all()


@router.patch("/payments/{payment_id}/release", response_model=PaymentAdminResponse, status_code=status.HTTP_200_OK)
async def release_payment(
    payment_id: str,
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(require_admin)
):
    payment = await session.get(Payment, payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    if payment.status != PaymentStatus.held:
        raise HTTPException(status_code=400, detail="Payment is not in held status")

    booking = await session.get(Booking, payment.booking_id)
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.status != BookingStatus.completed:
        raise HTTPException(status_code=400, detail="Booking is not completed yet")

    payment.status = PaymentStatus.released
    payment.released_at = datetime.utcnow()
    session.add(payment)
    await session.commit()
    await session.refresh(payment)

    # Notify professional
    professional = await session.get(Professional, booking.professional_id)
    if professional:
        professional_user = await session.get(User, professional.user_id)
        if professional_user:
            send_sms(
                professional_user.phone,
                f"Good news! Payment of {payment.amount} has been released to your account."
            )
            await create_notification(
                session,
                professional_user.id,
                "payment_released",
                f"Payment of {payment.amount} for your completed job has been released."
            )
    return payment


@router.patch("/payments/{payment_id}/refund", response_model=PaymentAdminResponse, status_code=status.HTTP_200_OK)
async def refund_payment(
    payment_id: str,
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(require_admin)
):
    payment = await session.get(Payment, payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    if payment.status != PaymentStatus.held:
        raise HTTPException(status_code=400, detail="Payment is not in held status")

    payment.status = PaymentStatus.refunded
    session.add(payment)
    await session.commit()
    await session.refresh(payment)

    booking = await session.get(Booking, payment.booking_id)
    if booking:
        client = await session.get(User, booking.client_id)
        if client:
            send_sms(
                client.phone,
                f"Your payment of {payment.amount} has been refunded."
            )
            await create_notification(
                session,
                client.id,
                "payment_refunded",
                f"Your payment of {payment.amount} has been refunded successfully."
            )
    return payment


# dispute
@router.get("/disputes", response_model=List[DisputeAdminResponse], status_code=status.HTTP_200_OK)
async def get_all_disputes(
    status: Optional[DisputeStatus] = None,
    limit: int = 20,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(require_admin)
):
    query = select(Dispute)
    if status:
        query = query.where(Dispute.status == status)
    result = await session.exec(query.offset(offset).limit(limit))
    return result.all()


@router.get("/disputes/{dispute_id}", response_model=DisputeAdminResponse, status_code=status.HTTP_200_OK)
async def get_dispute_by_id(
    dispute_id: str,
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(require_admin)
):
    dispute = await session.get(Dispute, dispute_id)
    if dispute is None:
        raise HTTPException(status_code=404, detail="Dispute not found")
    return dispute


@router.patch("/disputes/{dispute_id}/resolve", response_model=DisputeAdminResponse, status_code=status.HTTP_200_OK)
async def resolve_dispute(
    dispute_id: str,
    resolve_data: DisputeResolve,
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(require_admin)
):
    dispute = await session.get(Dispute, dispute_id)
    if dispute is None:
        raise HTTPException(status_code=404, detail="Dispute not found")
    if dispute.status == DisputeStatus.resolved:
        raise HTTPException(status_code=400, detail="Dispute already resolved")

    # Update dispute
    dispute.status = DisputeStatus.resolved
    dispute.resolution = resolve_data.resolution
    dispute.resolved_by = current_admin.id
    dispute.resolved_at = datetime.utcnow()
    session.add(dispute)
    await session.commit()
    await session.refresh(dispute)

    # Handle payment based on admin decision
    payment_result = await session.exec(
        select(Payment).where(Payment.booking_id == dispute.booking_id)
    )
    payment = payment_result.first()

    if payment and payment.status == PaymentStatus.held:
        if resolve_data.action == "release":
            payment.status = PaymentStatus.released
            payment.released_at = datetime.utcnow()
        elif resolve_data.action == "refund":
            payment.status = PaymentStatus.refunded
        session.add(payment)
        await session.commit()

    # Notify the person who raised the dispute
    raiser = await session.get(User, dispute.raised_by)
    if raiser:
        send_sms(
            raiser.phone,
            f"Your dispute has been resolved. Resolution: {resolve_data.resolution}"
        )
        await create_notification(
            session,
            raiser.id,
            "dispute_resolved",
            f"Your dispute has been resolved. Resolution: {resolve_data.resolution}"
        )

    return dispute