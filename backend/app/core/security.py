from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import random
import string
import redis.asyncio as aioredis

from app.core.config import settings

# ─── Password hashing ───────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ─── JWT ────────────────────────────────────────────────────
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """Raises JWTError if invalid or expired."""
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])


# ─── Token blacklist (Redis) ─────────────────────────────────
async def get_redis() -> aioredis.Redis:
    return await aioredis.from_url(settings.REDIS_URL, decode_responses=True)


async def blacklist_token(token: str, expires_in_seconds: int) -> None:
    """Add a token to the Redis blacklist on logout."""
    r = await get_redis()
    await r.setex(f"blacklist:{token}", expires_in_seconds, "1")


async def is_token_blacklisted(token: str) -> bool:
    r = await get_redis()
    return await r.exists(f"blacklist:{token}") == 1


# ─── 2FA OTP ─────────────────────────────────────────────────
def generate_otp(length: int = 6) -> str:
    return "".join(random.choices(string.digits, k=length))


async def store_otp(phone: str, otp: str, expires_in: int = 300) -> None:
    """Store OTP in Redis for 5 minutes (300s)."""
    r = await get_redis()
    await r.setex(f"otp:{phone}", expires_in, otp)


async def verify_otp(phone: str, otp: str) -> bool:
    """Check OTP and delete it after first use."""
    r = await get_redis()
    stored = await r.get(f"otp:{phone}")
    if stored and stored == otp:
        await r.delete(f"otp:{phone}")
        return True
    return False