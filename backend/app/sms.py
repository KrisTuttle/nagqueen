from twilio.rest import Client
from .config import get_settings

settings = get_settings()


def get_twilio_client() -> Client | None:
    if not settings.twilio_account_sid or not settings.twilio_auth_token:
        return None
    return Client(settings.twilio_account_sid, settings.twilio_auth_token)


def send_sms(to: str, message: str) -> bool:
    client = get_twilio_client()
    if not client:
        print(f"[DEV MODE] SMS to {to}: {message}")
        return True

    try:
        client.messages.create(
            body=message,
            from_=settings.twilio_phone_number,
            to=to
        )
        return True
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return False


def send_otp(phone_number: str, code: str) -> bool:
    message = f"Your Nag Queen verification code is: {code}"
    return send_sms(phone_number, message)


def send_reminder(phone_number: str, reminder_message: str) -> bool:
    return send_sms(phone_number, reminder_message)
