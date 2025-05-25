from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship

from .base import Base

class Event(Base):
    """Calendar event model."""
    
    __tablename__ = "events"
    
    title = Column(String(100), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String(255))
    is_all_day = Column(Boolean, default=False)
    status = Column(String(20), default="scheduled")  # scheduled, cancelled, completed
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="events")
    reminders = relationship("Reminder", back_populates="event", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Event {self.title} ({self.start_time} - {self.end_time})>"
    
    @property
    def is_past(self) -> bool:
        """Check if the event is in the past."""
        return datetime.utcnow() > self.end_time
    
    @property
    def is_upcoming(self) -> bool:
        """Check if the event is upcoming."""
        return datetime.utcnow() < self.start_time
    
    @property
    def is_ongoing(self) -> bool:
        """Check if the event is currently ongoing."""
        now = datetime.utcnow()
        return self.start_time <= now <= self.end_time
