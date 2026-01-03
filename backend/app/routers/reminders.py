from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import calendar

from ..database import get_db
from ..schemas import ReminderCreate, ReminderUpdate, ReminderResponse
from ..auth import get_approved_user
from ..models import User, Reminder, ScheduleType

router = APIRouter(prefix="/reminders", tags=["reminders"])


def calculate_next_run(
    schedule_type: ScheduleType,
    schedule_time,
    schedule_days: list[int] | None = None,
    schedule_day_of_month: str | None = None,
    schedule_date = None
) -> datetime:
    now = datetime.utcnow()
    today = now.date()

    # For one-time reminders with a specific date
    if schedule_type.value == "once" and schedule_date:
        return datetime.combine(schedule_date, schedule_time)

    # Combine today's date with the schedule time
    next_run = datetime.combine(today, schedule_time)

    # If the time has already passed today, start from tomorrow
    if next_run <= now:
        next_run += timedelta(days=1)

    if schedule_type.value == "once":
        return next_run

    elif schedule_type.value == "daily":
        return next_run

    elif schedule_type.value == "weekly":
        if not schedule_days:
            schedule_days = [0]  # Default to Monday

        # Find the next valid day
        for _ in range(7):
            if next_run.weekday() in schedule_days:
                return next_run
            next_run += timedelta(days=1)

    elif schedule_type.value == "monthly":
        day = schedule_day_of_month or "1"

        for _ in range(12):  # Try up to 12 months
            year = next_run.year
            month = next_run.month
            last_day = calendar.monthrange(year, month)[1]

            if day == "last":
                target_day = last_day
            else:
                target_day = min(int(day), last_day)

            candidate = datetime(year, month, target_day, schedule_time.hour, schedule_time.minute)

            if candidate > now:
                return candidate

            # Move to next month
            if month == 12:
                next_run = datetime(year + 1, 1, 1, schedule_time.hour, schedule_time.minute)
            else:
                next_run = datetime(year, month + 1, 1, schedule_time.hour, schedule_time.minute)

    return next_run


@router.get("", response_model=list[ReminderResponse])
def list_reminders(
    current_user: User = Depends(get_approved_user),
    db: Session = Depends(get_db)
):
    reminders = db.query(Reminder).filter(Reminder.user_id == current_user.id).all()
    return reminders


@router.post("", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
def create_reminder(
    reminder: ReminderCreate,
    current_user: User = Depends(get_approved_user),
    db: Session = Depends(get_db)
):
    next_run = calculate_next_run(
        reminder.schedule_type,
        reminder.schedule_time,
        reminder.schedule_days,
        reminder.schedule_day_of_month,
        reminder.schedule_date
    )

    db_reminder = Reminder(
        user_id=current_user.id,
        message=reminder.message,
        schedule_type=reminder.schedule_type,
        schedule_time=reminder.schedule_time,
        schedule_days=reminder.schedule_days,
        schedule_day_of_month=reminder.schedule_day_of_month,
        next_run=next_run
    )
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)

    return db_reminder


@router.get("/{reminder_id}", response_model=ReminderResponse)
def get_reminder(
    reminder_id: str,
    current_user: User = Depends(get_approved_user),
    db: Session = Depends(get_db)
):
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()

    if not reminder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found")

    return reminder


@router.put("/{reminder_id}", response_model=ReminderResponse)
def update_reminder(
    reminder_id: str,
    update: ReminderUpdate,
    current_user: User = Depends(get_approved_user),
    db: Session = Depends(get_db)
):
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()

    if not reminder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found")

    update_data = update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(reminder, field, value)

    # Recalculate next_run if schedule changed
    if any(f in update_data for f in ["schedule_type", "schedule_time", "schedule_days", "schedule_day_of_month"]):
        reminder.next_run = calculate_next_run(
            reminder.schedule_type,
            reminder.schedule_time,
            reminder.schedule_days,
            reminder.schedule_day_of_month
        )

    db.commit()
    db.refresh(reminder)

    return reminder


@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reminder(
    reminder_id: str,
    current_user: User = Depends(get_approved_user),
    db: Session = Depends(get_db)
):
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()

    if not reminder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found")

    db.delete(reminder)
    db.commit()
