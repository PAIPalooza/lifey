import sys
import asyncio
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.database import SessionLocal, init_db
from app.core.security import get_password_hash
from app.models import User, Event, Reminder, ReminderType, ReminderStatus

def init() -> None:
    """Initialize the database with test data."""
    print("Initializing database...")
    
    # Initialize the database (create tables)
    init_db()
    
    db = SessionLocal()
    try:
        # Create test user
        user = db.query(User).filter(User.email == "test@example.com").first()
        if not user:
            user = User(
                email="test@example.com",
                hashed_password=get_password_hash("testpassword"),
                full_name="Test User",
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"Created test user: {user.email}")
        
        # Create admin user
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin:
            admin = User(
                email="admin@example.com",
                hashed_password=get_password_hash("adminpassword"),
                full_name="Admin User",
                is_active=True,
                is_superuser=True
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print(f"Created admin user: {admin.email}")
        
        # Create test event
        event = db.query(Event).filter(Event.title == "Team Meeting").first()
        if not event:
            start_time = datetime.utcnow() + timedelta(days=1)
            event = Event(
                title="Team Meeting",
                description="Weekly team sync",
                start_time=start_time,
                end_time=start_time + timedelta(hours=1),
                location="Zoom",
                owner_id=user.id
            )
            db.add(event)
            db.commit()
            db.refresh(event)
            print(f"Created test event: {event.title}")
            
            # Create reminder for the event
            reminder = Reminder(
                message="Team meeting in 15 minutes",
                reminder_time=start_time - timedelta(minutes=15),
                reminder_type=ReminderType.IN_APP,
                status=ReminderStatus.PENDING,
                event_id=event.id,
                owner_id=user.id
            )
            db.add(reminder)
            db.commit()
            print(f"Created reminder for event: {reminder.message}")
            
            # Create a standalone reminder
            standalone_reminder = Reminder(
                message="Standalone reminder",
                reminder_time=datetime.utcnow() + timedelta(days=2),
                reminder_type=ReminderType.EMAIL,
                status=ReminderStatus.PENDING,
                owner_id=user.id
            )
            db.add(standalone_reminder)
            db.commit()
            print(f"Created standalone reminder: {standalone_reminder.message}")
        
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    # Add the project root to the Python path
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    
    init()
