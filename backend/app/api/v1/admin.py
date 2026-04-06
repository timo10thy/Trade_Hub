from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List

from app.core.dependencies import require_admin
from app.models.user import User
from app.db.session import get_session
from app.schemas.admin import UserAdminListResponse

router = APIRouter()

@router.get("/users", response_model=List[UserAdminListResponse], status_code=status.HTTP_200_OK)
async def get_all_users(
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(require_admin)
):
    result = await session.exec(select(User))
    users = result.all()
    return users