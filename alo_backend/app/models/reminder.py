from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from .base import Base

class ReminderType(PyEnum):
    EMAIL = "email"
    PUSH = "push"
    SMS = "sms"
    IN_APP = "in_app"

class ReminderStatus(PyEnum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"

class Reminder(Base):
    """Reminder model for event notifications."""
    
    __tablename__ = "reminders"
    
    message = Column(String(500), nullable=False)
    reminder_time = Column(DateTime, nullable=False)
    reminder_type = Column(Enum(ReminderType), nullable=False, default=ReminderType.IN_APP)
    status = Column(Enum(ReminderStatus), default=ReminderStatus.PENDING)
    sent_at = Column(DateTime, nullable=True)
    
    # Foreign keys
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True)  # Optional for standalone reminders
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="reminders")
    event = relationship("Event", back_populates="reminders")
    
    def __repr__(self) -> str:
        return f"<Reminder {self.id} for {self.reminder_time}>"
    
    @property
    def is_due(self) -> bool:
        """Check if the reminder is due to be sent."""
        return datetime.utcnow() >= self.reminder_time and self.status == ReminderStatus.PENDING
