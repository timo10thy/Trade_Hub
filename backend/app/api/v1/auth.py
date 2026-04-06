from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.db.session import get_session
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.core.config import settings
from app.models.user import User
from app.models.enum import UserRole, UserStatus
from app.schemas.user import UserCreate, UserResponse, UserLogin, TokenResponse

router = APIRouter()


@router.post("/register/client", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_client(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(User).where(User.email == user_data.email))
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    result = await session.exec(select(User).where(User.phone == user_data.phone))
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )

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
    result = await session.exec(select(User).where(User.email == user_data.email))
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    result = await session.exec(select(User).where(User.phone == user_data.phone))
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )

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


@router.post("/register/admin", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_admin(
    user_data: UserCreate,
    x_admin_secret: str = Header(...),
    session: AsyncSession = Depends(get_session)
):
    if x_admin_secret != settings.ADMIN_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin secret key"
        )

    result = await session.exec(select(User).where(User.email == user_data.email))
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    result = await session.exec(select(User).where(User.phone == user_data.phone))
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )

    user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=hash_password(user_data.password),
        role=UserRole.admin,
        status=UserStatus.active,
        email_verified=True,
        phone_verified=True,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(user_data: UserLogin, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(User).where(User.email == user_data.email))
    user = result.first()
    if not user:
        raise HTTPException(404, "User not found")
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(401, "Incorrect password")
    if user.status == UserStatus.suspended:
        raise HTTPException(403, "Account suspended")
    
    access_token = create_access_token({"sub": user.id, "role": user.role.value})
    refresh_token = create_refresh_token({"sub": user.id})
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user
    )