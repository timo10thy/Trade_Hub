from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List, Optional
from app.models.enum import UserStatus

from app.core.dependencies import require_admin
from app.models.user import User
from app.db.session import get_session
from app.schemas.admin import UserAdminListResponse, UserStatusUpdate
from app.schemas.user import UserResponse, UserCreate

router = APIRouter()

@router.get("/users", response_model=List[UserAdminListResponse], status_code=status.HTTP_200_OK)
async def get_all_users(
    limit: int = 20,
    offset: int = 0,
    status: Optional[UserStatus] = None,
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(require_admin)
):
    
    query = select(User)
    if status:
        query = query.where(User.status == status)
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
    user_id:str,status_update: UserStatusUpdate, 
    session:AsyncSession = Depends(get_session),
    current_admin:User=Depends(require_admin)
):
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = status_update.status
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user