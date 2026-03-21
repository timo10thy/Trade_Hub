from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import decode_token, is_token_blacklisted
from app.db.session import get_session

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_session),
):
    """Extract and validate JWT. Returns the user object."""
    from app.models.user import User  # local import avoids circular deps

    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")

        if user_id is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Check blacklist (logout)
    if await is_token_blacklisted(token):
        raise credentials_exception

    # Fetch user from DB
    user = await session.get(User, user_id)
    if user is None:
        raise credentials_exception
    if user.status == "suspended":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been suspended",
        )

    return user


# ─── Role guards ─────────────────────────────────────────────
def require_role(*roles: str):
    """Usage: Depends(require_role('admin')) or Depends(require_role('professional', 'admin'))"""

    async def role_checker(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access restricted to: {', '.join(roles)}",
            )
        return current_user

    return role_checker


# ─── Convenience shortcuts ────────────────────────────────────
require_admin = require_role("admin")
require_professional = require_role("professional")
require_client = require_role("client")
require_pro_or_admin = require_role("professional", "admin")