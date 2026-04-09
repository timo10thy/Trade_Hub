from twilio.rest import Client
from app.core.config import settings
import logging

logger = logging.getLogger("tradehub")

def send_sms(to: str, message: str) -> bool:
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to
        )
        logger.info(f"SMS sent to {to}")
        return True
    except Exception as e:
        logger.error(f"SMS failed to {to}: {str(e)}")
        return False