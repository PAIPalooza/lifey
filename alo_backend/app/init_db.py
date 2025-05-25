"""
Database initialization script.
This script initializes the database with test data for development purposes.
"""
import logging
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import get_password_hash
from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.event import Event
from app.models.reminder import Reminder, ReminderType, ReminderStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    """Initialize the database with test data."""
    
    # Create tables if they don't exist
    logger.info("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    # Check if there are any users already
    user = db.query(User).first()
    if user:
        logger.info("Database already initialized, skipping...")
        return
    
    logger.info("Creating test users...")
    
    # Create a test user
    test_user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        is_active=True,
        is_superuser=False,
    )
    db.add(test_user)
    
    # Create an admin user
    settings = get_settings()
    admin_user = User(
        email=settings.FIRST_SUPERUSER_EMAIL,
        hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
        full_name="Admin User",
        is_active=True,
        is_superuser=True,
    )
    db.add(admin_user)
    
    # Commit the users so they get their IDs
    db.commit()
    db.refresh(test_user)
    db.refresh(admin_user)
    
    logger.info("Creating test events and reminders...")
    
    # Create a sample event for the test user
    now = datetime.utcnow()
    event = Event(
        title="Team Meeting",
        description="Weekly sync with the team",
        start_time=now + timedelta(days=1, hours=10),
        end_time=now + timedelta(days=1, hours=11),
        location="Conference Room A",
        is_all_day=False,
        status="scheduled",
        owner_id=test_user.id,
    )
    db.add(event)
    
    # Commit the event so it gets its ID
    db.commit()
    db.refresh(event)
    
    # Create a sample reminder for the event
    reminder = Reminder(
        message="Don't forget your weekly team meeting!",
        reminder_time=now + timedelta(days=1, hours=9, minutes=45),
        reminder_type=ReminderType.EMAIL,
        status=ReminderStatus.PENDING,
        event_id=event.id,
        owner_id=test_user.id,
    )
    db.add(reminder)
    
    # Create another event for the admin user
    admin_event = Event(
        title="Project Deadline",
        description="Final submission for the ALO project",
        start_time=now + timedelta(days=7),
        end_time=now + timedelta(days=7, hours=1),
        location="Virtual",
        is_all_day=True,
        status="scheduled",
        owner_id=admin_user.id,
    )
    db.add(admin_event)
    
    # Commit all remaining changes
    db.commit()
    
    logger.info("Database initialized successfully!")


def main() -> None:
    """Main function to initialize the database."""
    logger.info("Starting database initialization...")
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
    logger.info("Database initialization completed!")


if __name__ == "__main__":
    main()
