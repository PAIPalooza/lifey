from datetime import datetime
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.ReminderResponse])
def read_reminders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
    event_id: Optional[int] = None,
    status: Optional[schemas.ReminderStatus] = None,
) -> Any:
    """Retrieve reminders for the current user."""
    query = db.query(models.Reminder).filter(models.Reminder.owner_id == current_user.id)
    
    if event_id is not None:
        query = query.filter(models.Reminder.event_id == event_id)
    if status is not None:
        query = query.filter(models.Reminder.status == status)
    
    reminders = query.offset(skip).limit(limit).all()
    
    # Process the reminders to manually convert enum values to strings
    # This ensures proper serialization according to SSCS and ALO Project Development Rules
    result = []
    for reminder in reminders:
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
        result.append(reminder_dict)
    
    return result

@router.post("/", response_model=schemas.ReminderResponse, status_code=status.HTTP_201_CREATED)
def create_reminder(
    reminder_in: schemas.ReminderCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Create a new reminder."""
    # If event_id is provided, verify the event exists and belongs to the user
    if reminder_in.event_id is not None:
        event = db.query(models.Event).filter(models.Event.id == reminder_in.event_id).first()
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found",
            )
        if event.owner_id != current_user.id and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to add reminder to this event",
            )
    
    # Create reminder
    reminder = models.Reminder(
        **reminder_in.dict(),
        owner_id=current_user.id,
        status=schemas.ReminderStatus.PENDING
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder

@router.get("/{reminder_id}", response_model=schemas.ReminderResponse)
def read_reminder(
    reminder_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get a specific reminder by id."""
    reminder = db.query(models.Reminder).filter(models.Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found",
        )
    
    # Check if the current user is the owner of the reminder
    if reminder.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this reminder",
        )
    
    return reminder

@router.put("/{reminder_id}", response_model=schemas.ReminderResponse)
def update_reminder(
    reminder_id: int,
    reminder_in: schemas.ReminderUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """Update a reminder."""
    reminder = db.query(models.Reminder).filter(models.Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found",
        )
    
    # Check if the current user is the owner of the reminder
    if reminder.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this reminder",
        )
    
    # If event_id is being updated, verify the new event exists and belongs to the user
    if reminder_in.event_id is not None and reminder_in.event_id != reminder.event_id:
        event = db.query(models.Event).filter(models.Event.id == reminder_in.event_id).first()
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found",
            )
        if event.owner_id != current_user.id and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to associate with this event",
            )
    
    # Update reminder data
    update_data = reminder_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(reminder, field, value)
    
    # If status is being updated to SENT, set sent_at to current time
    if reminder_in.status == schemas.ReminderStatus.SENT and reminder.status != schemas.ReminderStatus.SENT:
        reminder.sent_at = datetime.utcnow()
    
    reminder.updated_at = datetime.utcnow()
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder

@router.delete("/{reminder_id}", response_model=schemas.ReminderResponse)
def delete_reminder(
    reminder_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """Delete a reminder."""
    reminder = db.query(models.Reminder).filter(models.Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found",
        )
    
    # Check if the current user is the owner of the reminder
    if reminder.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this reminder",
        )
    
    db.delete(reminder)
    db.commit()
    return reminder
