from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, validator
from app.schemas.reminder import ReminderResponse

class EventBase(BaseModel):
    """Base event schema."""
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    is_all_day: bool = False

    @validator('end_time')
    def end_time_must_be_after_start_time(cls, v, values, **kwargs):
        if 'start_time' in values and v < values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v

class EventCreate(EventBase):
    """Schema for creating an event."""
    pass

class EventUpdate(BaseModel):
    """Schema for updating an event."""
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    is_all_day: Optional[bool] = None
    status: Optional[str] = None

class EventInDBBase(EventBase):
    """Base schema for event in database."""
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    status: str

    class Config:
        orm_mode = True

class EventResponse(EventInDBBase):
    """Event response schema."""
    reminders: List[ReminderResponse] = []
    
    class Config(EventInDBBase.Config):
        # This ensures proper serialization of nested objects with enum values
        @classmethod
        def schema_extra(cls, schema: dict, model: type):
            props = schema.get('properties', {})
            # Process reminders property if it exists
            if 'reminders' in props and 'items' in props['reminders']:
                reminder_schema = props['reminders']['items']
                # Handle nested reminder properties
                for prop, value in reminder_schema.get('properties', {}).items():
                    if prop in ['reminder_type', 'status']:
                        value['type'] = 'string'
