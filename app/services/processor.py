from sqlalchemy.orm import Session
# this session prvided by sqlalchemy defines what a database session is capable of doing like querying, inserting, updating, deleting rows in the table.
# sessionLocal creates session classes after making a connection to db for operating on db, and we use this when its passed to this process event fucntion.

from app.db.models import Event, EventProcessingResult, EventStatus
from app.services.rules import classify_event

# Session is a type hint indicating that the db parameter is expected to be an instance of SQLAlchemy's Session class like sessionLocal() object created in events.py and passed here when process_event is called as background task.
def process_event(event_id, db: Session):
    """
    Processes a single event end-to-end.
    """

    try:
        # 1. Fetch event
        # query(event) means select * from event table
        event = db.query(Event).filter(Event.event_id == event_id).first()

        if not event:
            raise ValueError("Event not found")

        # 2. Mark as processing
        event.status = EventStatus.processing
        # we commit here because even if the app crashes later, you still know processing started
        db.commit()

        # 3. Apply business rules
        classification = classify_event(event.event_type, event.payload)

        # 4. Store processing result
        result = EventProcessingResult(
            event_id=event.event_id,
            severity=classification.severity,
            classification_reason=classification.classification_reason,
            recommendation=classification.recommendation,
            should_escalate=classification.should_escalate,
        )
        # add just stages the object for insertion, it doesn't push to db until commit is called
        db.add(result)

        # 5. Mark event as completed
        event.status = EventStatus.completed
        db.commit()

    except Exception as e:
        db.rollback()

        # If event exists, mark it as failed
        # locals() is a dictionary of local variables defined in this current function
        if 'event' in locals() and event:
            event.status = EventStatus.failed
            event.error_message = str(e)
            db.commit()

        raise