from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import Reminder, ScheduleType
from .sms import send_reminder
from .routers.reminders import calculate_next_run


def process_due_reminders():
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()

        # Find all due reminders
        due_reminders = db.query(Reminder).filter(
            Reminder.next_run <= now,
            Reminder.is_active == True
        ).all()

        for reminder in due_reminders:
            # Send the SMS
            success = send_reminder(reminder.user.phone_number, reminder.message)

            if success:
                if reminder.schedule_type == ScheduleType.once:
                    # One-time reminders get deactivated
                    reminder.is_active = False
                else:
                    # Recurring reminders get rescheduled
                    reminder.next_run = calculate_next_run(
                        reminder.schedule_type,
                        reminder.schedule_time,
                        reminder.schedule_days,
                        reminder.schedule_day_of_month
                    )

        db.commit()

    except Exception as e:
        print(f"Error processing reminders: {e}")
        db.rollback()
    finally:
        db.close()


scheduler = BackgroundScheduler()


def start_scheduler():
    scheduler.add_job(process_due_reminders, "interval", minutes=1, id="process_reminders")
    scheduler.start()


def stop_scheduler():
    scheduler.shutdown()
