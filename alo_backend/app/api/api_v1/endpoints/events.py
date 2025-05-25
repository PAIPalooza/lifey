from datetime import datetime
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.EventResponse])
def read_events(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> Any:
    """Retrieve events for the current user."""
    query = db.query(models.Event).filter(models.Event.owner_id == current_user.id)
    
    if start_date:
        query = query.filter(models.Event.start_time >= start_date)
    if end_date:
        query = query.filter(models.Event.end_time <= end_date)
    
    events = query.offset(skip).limit(limit).all()
    
    # Process the events to manually convert enum values to strings
    # This ensures proper serialization according to SSCS and ALO Project Development Rules
    result = []
    for event in events:
        # Create a dictionary representation of the event
        event_dict = {
            "title": event.title,
            "description": event.description,
            "start_time": event.start_time,
            "end_time": event.end_time,
            "location": event.location,
            "is_all_day": event.is_all_day,
            "id": event.id,
            "owner_id": event.owner_id,
            "created_at": event.created_at,
            "updated_at": event.updated_at,
            "status": event.status,
            "reminders": []
        }
        
        # Process reminders if any
        for reminder in event.reminders:
            reminder_dict = {
                "id": reminder.id,
                "message": reminder.message,
                "reminder_time": reminder.reminder_time,
                "reminder_type": reminder.reminder_type.value if hasattr(reminder.reminder_type, "value") else str(reminder.reminder_type),
                "status": reminder.status.value if hasattr(reminder.status, "value") else str(reminder.status),
                "sent_at": reminder.sent_at,
                "event_id": reminder.event_id,
                "owner_id": reminder.owner_id,
                "created_at": reminder.created_at,
                "updated_at": reminder.updated_at
            }
            event_dict["reminders"].append(reminder_dict)
        
        result.append(event_dict)
    
    return result

@router.post("/", response_model=schemas.EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    event_in: schemas.EventCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Create a new event."""
    # Check if end time is after start time
    if event_in.end_time <= event_in.start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time",
        )
    
    # Create event
    event = models.Event(**event_in.dict(), owner_id=current_user.id)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.get("/{event_id}", response_model=schemas.EventResponse)
def read_event(
    event_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get a specific event by id."""
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    
    # Check if the current user is the owner of the event
    if event.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this event",
        )
    
    return event

@router.put("/{event_id}", response_model=schemas.EventResponse)
def update_event(
    event_id: int,
    event_in: schemas.EventUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """Update an event."""
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    
    # Check if the current user is the owner of the event
    if event.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this event",
        )
    
    # Update event data
    update_data = event_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)
    
    event.updated_at = datetime.utcnow()
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.delete("/{event_id}", response_model=schemas.EventResponse)
def delete_event(
    event_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """Delete an event."""
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    
    # Check if the current user is the owner of the event
    if event.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this event",
        )
    
    db.delete(event)
    db.commit()
    return event
