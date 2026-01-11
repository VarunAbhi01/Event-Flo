#  This is for event-related API endpoints
# APIrouter: An APIRouter is like a folder for your website's addresses organised into seperate sections/files. If your API was a massive building, the FastAPI() app is the front door, and an APIRouter is a hallway that leads to specific rooms.    
    # We can have seperate files like api/events.py - api/users.py - api/payments.py, having their own routers defined in them, and we simply import and plug into our main application file (main.py) - this keeps code modular and organised. rather than writing all endpoints in main.py
# BackgroundTasks: is a fastapi feature that lets you run tasks in the background after sending a response to the user. This is useful for things that take time, like sending emails or processing data, so the user doesn't have to wait for these tasks to finish before getting a response.

from fastapi import APIRouter, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Event, EventStatus
from app.services.processor import process_event
from uuid import UUID

# we define this router for events-related endpoints. 
router = APIRouter()

# HTTP POST endpoint to create a new event: POST /events/.  will call create_event function when this endpoint is hit.
@router.post("/")
def create_event(
    event_type: str,
    payload: dict,
    background_tasks: BackgroundTasks
):
    # Create a DB session using SessionLocal(),and tell everyone that this object is of type Session. This will be created at endpoints only so same session created at endpoint be used for the requests via this and not in the seperate functions so the same session isnt shared across multiple requests.
        # why because session is a temporary conversation setup so if the same chat is shared across multiple requests by diff users if present in a function, it can mix up one users rqst to db with other users rqst, say if one says d.add() and other says db.delete() - this can cause data corruption - 
        # so we shall have one session per request created at endpoint level and passed to other functions as needed.
    db: Session = SessionLocal()

    try:
    # we are creating a new event object with the provided event_type and payload. The status is set to queued by default.
    # and this object is added to the database session, committed (saved to the database), that reflects as row in db.
        event = Event(
            event_type=event_type,
            status=EventStatus.queued,
            payload=payload
        )

        db.add(event)
        db.commit()
        db.refresh(event)

        # After the event is created and saved in the database, we add a background task to process the event. This means that the process_event function will be called with the event's ID and the database session, but it will run in the background after the response is sent to the user.
        background_tasks.add_task(process_event, event.event_id, db)

        # we send the response immedietly to the user with the event ID and its status - wont wait for background process to complete - Runs asynchronously
        return {
            "event_id": event.event_id,
            "status": event.status
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
    

# HTTP GET endpoint to retrieve an event by its ID: GET /events/{event_id}, will call get_event function when this endpoint is hit.
@router.get("/{event_id}")
def get_event(event_id: UUID):
    db: Session = SessionLocal()
    
    try:
        event = db.query(Event).filter(Event.event_id == event_id).first()

        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        return {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "status": event.status,
            "payload": event.payload,
            "error_message": event.error_message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        db.close()

# HTTP GET endpoint to list recent events to know the process happening in app: GET /events/, will call list_events function when this endpoint is hit.
@router.get("/")
def list_events():
    db: Session = SessionLocal()

    try:
        events = (
            db.query(Event)
            .order_by(Event.created_at.desc())
            .limit(20)
            .all()
        )

        return [
            {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "status": event.status,
                "created_at": event.created_at,
            }
            for event in events
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        db.close()