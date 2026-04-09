from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.notification import Notification
import logging

logger = logging.getLogger("tradehub")

async def create_notification(
    session: AsyncSession,
    user_id: str,
    type: str,
    message: str
) -> Notification:
    try:
        notification = Notification(
            user_id=user_id,
            type=type,
            message=message
        )
        session.add(notification)
        await session.commit()
        await session.refresh(notification)
        logger.info(f"Notification created for user {user_id}")
        return notification
    except Exception as e:
        logger.error(f"Failed to create notification for user {user_id}: {str(e)}")
        raise
