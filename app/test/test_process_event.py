import uuid

from app.db.session import SessionLocal
from app.db.models import Event
from app.services.processor import process_event


def run_processor_test():
    db = SessionLocal()

    try:
        # 1. Fetch one existing event (latest)
        event = db.query(Event).order_by(Event.created_at.desc()).first()

        if not event:
            print("No events found to process")
            return

        print("Processing event:", event.event_id)

        # 2. Call processor
        process_event(event.event_id, db)

        print("Processing completed")

    except Exception as e:
        print("Error during processing:", e)

    finally:
        db.close()


if __name__ == "__main__":
    run_processor_test()