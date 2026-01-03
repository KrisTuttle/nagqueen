from pydantic import BaseModel, Field
from datetime import datetime, time, date
from typing import Optional
from enum import Enum


class ScheduleType(str, Enum):
    once = "once"
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"


# Auth schemas
class OTPRequest(BaseModel):
    phone_number: str = Field(..., pattern=r"^\+[1-9]\d{1,14}$", description="E.164 format phone number")


class OTPVerify(BaseModel):
    phone_number: str = Field(..., pattern=r"^\+[1-9]\d{1,14}$")
    code: str = Field(..., min_length=6, max_length=6)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    phone_number: str
    is_approved: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Reminder schemas
class ReminderCreate(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)
    schedule_type: ScheduleType
    schedule_time: time
    schedule_date: Optional[date] = Field(None, description="For once: specific date")
    schedule_days: Optional[list[int]] = Field(None, description="For weekly: 0=Mon, 6=Sun")
    schedule_day_of_month: Optional[str] = Field(None, description="For monthly: 1-31 or 'last'")


class ReminderUpdate(BaseModel):
    message: Optional[str] = Field(None, min_length=1, max_length=500)
    schedule_type: Optional[ScheduleType] = None
    schedule_time: Optional[time] = None
    schedule_date: Optional[date] = None
    schedule_days: Optional[list[int]] = None
    schedule_day_of_month: Optional[str] = None
    is_active: Optional[bool] = None


class ReminderResponse(BaseModel):
    id: str
    message: str
    schedule_type: ScheduleType
    schedule_time: time
    schedule_days: Optional[list[int]]
    schedule_day_of_month: Optional[str]
    next_run: datetime
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
