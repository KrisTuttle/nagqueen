from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = "sqlite:///./nagqueen.db"
    jwt_secret: str = "change-this-to-a-random-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 168  # 7 days

    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""

    otp_expiration_minutes: int = 5

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
