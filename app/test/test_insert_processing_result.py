import uuid
from datetime import datetime

from app.db.session import SessionLocal
from app.db.models import EventProcessingResult, SeverityLevel

# event_id column in table is UUID type and doesnt expect strings rather uuid objects. so we convert the event id string generated during event insertion to uuid object here.
EVENT_ID = uuid.UUID("21a9b780-1015-46c4-8992-cf80d3ea44a0")


def insert_processing_result():
    db = SessionLocal()

    try:
        result = EventProcessingResult(
            event_id=EVENT_ID,
            severity=SeverityLevel.critical,
            classification_reason="Payment amount exceeded critical threshold",
            recommendation="Escalate to finance team immediately",
            should_escalate=True,
            processed_at=datetime.utcnow()
        )

        db.add(result)
        db.commit()

        print("Processing result inserted for event:", EVENT_ID)

    except Exception as e:
        db.rollback()
        print("Error inserting processing result:", e)

    finally:
        db.close()


if __name__ == "__main__":
    insert_processing_result()