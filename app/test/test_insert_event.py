from app.db.session import SessionLocal
from app.db.models import Event, EventStatus

def insert_event():
    db = SessionLocal()

    try:
        # creating a Event class object which represents a row in events table
        event = Event(
            event_type="payment_failed",
            source="test_script",
            status=EventStatus.queued,
            payload={
                "amount": 1500,
                "currency": "INR"
            }
        )

        # only plan to insert row happened and when we commit the session the data will be actually inserted into the table.
        # refresh is to get the latest state of the object from the db after commit like to get the auto generated fields values.
        db.add(event)
        db.commit()
        db.refresh(event)

        print("Event inserted with ID:", event.event_id)

    except Exception as e:
        # in case of error rollback the session to previous stable state, keeping db clean.
        db.rollback()
        print("Error inserting event:", e)

    finally:
        # Always close the session to prevent leaks.
        db.close()


if __name__ == "__main__":
    insert_event()