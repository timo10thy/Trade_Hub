from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.db.session import get_session
from app.core.security import hash_password
from app.models.user import User
from app.models.enum import UserRole
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("/register/client", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_client(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    # Check email exists
    result = await session.exec(select(User).where(User.email == user_data.email))
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check phone exists
    result = await session.exec(select(User).where(User.phone == user_data.phone))
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )

    # Create client user
    user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=hash_password(user_data.password),
        role=UserRole.client,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.post("/register/professional", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_professional(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    # Check email exists
    result = await session.exec(select(User).where(User.email == user_data.email))
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check phone exists
    result = await session.exec(select(User).where(User.phone == user_data.phone))
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )

    # Create professional user
    user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=hash_password(user_data.password),
        role=UserRole.professional,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
