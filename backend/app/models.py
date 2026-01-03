import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, Enum, Time, JSON
from sqlalchemy.orm import relationship
import enum

from .database import Base


def generate_uuid():
    return str(uuid.uuid4())


class ScheduleType(enum.Enum):
    once = "once"
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    phone_number = Column(String(20), unique=True, nullable=False, index=True)
    is_approved = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    reminders = relationship("Reminder", back_populates="user", cascade="all, delete-orphan")


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    schedule_type = Column(Enum(ScheduleType), nullable=False)
    schedule_time = Column(Time, nullable=False)
    schedule_days = Column(JSON, nullable=True)  # For weekly: [0,1,2,3,4,5,6] = Mon-Sun
    schedule_day_of_month = Column(String(10), nullable=True)  # For monthly: "1", "15", "last"
    next_run = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reminders")


class OTPCode(Base):
    __tablename__ = "otp_codes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    phone_number = Column(String(20), nullable=False, index=True)
    code = Column(String(6), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
