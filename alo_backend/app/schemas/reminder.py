from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator

class ReminderType(str, Enum):
    EMAIL = "email"
    PUSH = "push"
    SMS = "sms"
    IN_APP = "in_app"

class ReminderStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"

class ReminderBase(BaseModel):
    """Base reminder schema."""
    message: str
    reminder_time: datetime
    reminder_type: ReminderType = ReminderType.IN_APP
    status: ReminderStatus = ReminderStatus.PENDING
    event_id: Optional[int] = None

class ReminderCreate(ReminderBase):
    """Schema for creating a reminder."""
    pass

class ReminderUpdate(BaseModel):
    """Schema for updating a reminder."""
    message: Optional[str] = None
    reminder_time: Optional[datetime] = None
    reminder_type: Optional[ReminderType] = None
    status: Optional[ReminderStatus] = None

class ReminderInDBBase(ReminderBase):
    """Base schema for reminder in database."""
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    sent_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        
        # This ensures proper serialization of enum values from SQLAlchemy models
        @classmethod
        def schema_extra(cls, schema: dict, model: type):
            for prop, value in schema.get('properties', {}).items():
                if prop == 'reminder_type' or prop == 'status':
                    value['type'] = 'string'

class ReminderResponse(ReminderInDBBase):
    """Reminder response schema."""
    pass
