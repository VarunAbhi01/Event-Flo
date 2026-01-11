# MODELS: model is a python class that represents a table in the database. Its attributes map to the columns and objects maps to row in that table
# This file defines the structure of the tables, their relationships, and any constraints or data types associated with each column.

# enum is to define a set of restricted values to a variable.
import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Enum,
    JSON,
    Text,
    Boolean,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

# all models will be inheriting from this Base class to define themselves as tables in db
from app.db.session import Base

# defining fixed values for Event status and severity Level instead of allowing any other string values by user say now no one can simply assign any random values like "done", "finish", only the values we define are allowed to use. This helps maintain data integrity and consistency in the database.
class EventStatus(str, enum.Enum):
    queued = "queued"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class SeverityLevel(str, enum.Enum):
    low = "LOW"
    warning = "WARNING"
    high = "HIGH"
    critical = "CRITICAL"

# EVENT data model representing the events table in the database
class Event(Base):
    __tablename__ = "events"
    # uuid.uuid4() generates a random UUID and UUID(as_uuid=True) ensures that the UUID is stored in the database in its native binary format rather than as a string.
    event_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String, nullable=False)
    source = Column(String, nullable=True)
    # Enum(EventStatus) → only allowed enum values defined in EventStatus can be stored in this column. Default is 'queued' when a new event is created.
    status = Column(Enum(EventStatus), nullable=False, default=EventStatus.queued)
    payload = Column(JSON, nullable=False)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationship: which is related to ORM, when loading an Event, it provides an easy access to its related data.
    # uselist=False in the relationship above indicates that each Event can have at most one associated EventProcessingResult, establishing a one-to-one relationship between the two tables.
    # each Event can have one associated EventProcessingResult, accessible via the processing_result attribute.
    processing_result = relationship(
        "EventProcessingResult",
        back_populates="event",
        uselist=False
    )

# EVENT PROCESSING RESULT data model representing the event_processing_results table in the database
class EventProcessingResult(Base):
    __tablename__ = "event_processing_results"

    event_id = Column(
        UUID(as_uuid=True),
        ForeignKey("events.event_id"),
        primary_key=True
    )
    severity = Column(Enum(SeverityLevel), nullable=False)
    classification_reason = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=False)
    should_escalate = Column(Boolean, nullable=False)
    processed_at = Column(DateTime, default=datetime.utcnow)
    # each EventProcessingResult is linked back to its corresponding Event using the foreign key event_id.
    event = relationship("Event", back_populates="processing_result")