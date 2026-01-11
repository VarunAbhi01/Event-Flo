# EventFlo — Async Event Processing Backend

EventFlo is a simple, interview-ready backend system that demonstrates how to design and build an asynchronous event-processing workflow using FastAPI and PostgreSQL.

The project intentionally focuses on clarity, correctness, and explainability rather than advanced infrastructure or cloud services.

⸻

✨ What This Project Demonstrates
	•	REST API design using FastAPI
	•	Asynchronous background processing (without queues)
	•	Clear event lifecycle management
	•	Rule-based business decision engine (no AI / LLMs)
	•	Strong data integrity using PostgreSQL constraints
	•	Clean separation of concerns:
	•	API layer
	•	Business logic
	•	Persistence layer

This project is designed to be easy to explain line-by-line in interviews.

⸻

# 🚀 Setup Instructions

1️⃣ Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

2️⃣ Install dependencies
pip install fastapi uvicorn sqlalchemy alembic pydantic psycopg2-binary

3️⃣ Run the application
uvicorn app.main:app --reload


Once running, open:

👉 http://127.0.0.1:8000/docs

This opens FastAPI’s interactive Swagger UI.

⸻

# 📁 Recommended Project Structure (Phase 1)

eventflo/
│
├── app/
│   ├── main.py               # FastAPI application entry point
│   │
│   ├── db/
│   │   ├── session.py        # Database session and engine setup
│   │   ├── models.py         # SQLAlchemy ORM models
│   │
│   ├── services/
│   │   ├── processor.py     # Event lifecycle & background processing logic
│   │   ├── rules.py         # Business rules engine
│   │
│   ├── api/
│   │   ├── events.py        # API route definitions
│
├── alembic/                  # Database migrations
├── alembic.ini
├── requirements.txt
└── README.md



The structure is intentionally minimal and readable.

⸻

# 🔄 High-Level Execution Flow
	1.	Client sends an event via POST /events
	2.	Event is stored with status queued
	3.	API responds immediately with event_id
	4.	Background task processes the event
	5.	Status transitions:
	•	queued → processing → completed / failed
	6.	Processing result is persisted
	7.	Client can query status using GET /events/{event_id}

⸻

# 🧠 Execution Order (Recommended Build Sequence)

Follow this order to avoid confusion while building or understanding the project.

⸻

Step 1 — Database & Models
	•	Define events table
	•	Define event_processing_results table
	•	Create enums for:
	•	Event status
	•	Severity level

Once this layer is correct, everything else becomes straightforward.

⸻

Step 2 — Business Rules Engine (Pure Python)
	•	No FastAPI
	•	No database writes

A simple deterministic function:
def classify_event(event_type: str, payload: dict) -> ClassificationResult:
    ...

Why this matters:
	•	Fully testable
	•	Easy to reason about
	•	Easy to explain in interviews

⸻

Step 3 — Background Processor

A single orchestration function that:
	1.	Marks event as processing
	2.	Applies business rules
	3.	Saves processing result
	4.	Marks event as completed
	5.	Handles failures by marking event as failed

No queues.
No workers.
No hidden complexity.

⸻

Step 4 — API Endpoints

Only three endpoints are implemented:
	•	POST /events — create a new event
	•	GET /events/{event_id} — fetch event status and details
	•	GET /events — list recent events

Each endpoint is intentionally boring and simple.

⸻

# 🎯 Design Philosophy

Never build something you cannot explain.

This project prioritizes:
	•	Simplicity over abstraction
	•	Correctness over cleverness
	•	Understanding over tooling

It is designed to be extended later with:
	•	Queues
	•	Workers
	•	Cloud deployment

…but remains fully resume-worthy in its current form.

⸻

# 🧪 Testing

All functionality can be tested using:
	•	FastAPI Swagger UI (/docs)
	•	PostgreSQL GUI tools (Postico / pgAdmin)

No external services are required.

⸻

## 📌 Sample API Requests

All APIs can be tested using **FastAPI Swagger UI** at:
http://127.0.0.1:8000/docs

or via `curl` from the terminal.

---

### Create an Event  
**POST `/events`**

Creates a new event and triggers background processing.

Request Body (example: payment failure)

```json
{
  "event_type": "payment_failed",
  "payload": {
    "amount": 1500
  }
}

Response
{
  "event_id": "21a9b780-1015-46c4-8992-cf80d3ea44a0",
  "status": "queued"
}

The response is returned immediately while processing continues asynchronously in the background.


### 🔹 Get Event Status
GET /events/{event_id}

Fetches the current status and details of a specific event.

Example Request
GET /events/21a9b780-1015-46c4-8992-cf80d3ea44a0

Example Response (after processing)
{
  "event_id": "21a9b780-1015-46c4-8992-cf80d3ea44a0",
  "event_type": "payment_failed",
  "status": "completed",
  "payload": {
    "amount": 1500
  },
  "error_message": null
}


### 🔹 List Recent Events

GET /events

Returns a list of recently created events with their current status.

Example Response
[
  {
    "event_id": "21a9b780-1015-46c4-8992-cf80d3ea44a0",
    "event_type": "payment_failed",
    "status": "completed",
    "created_at": "2026-01-10T08:30:00"
  },
  {
    "event_id": "3f2a7d10-acde-4c89-9c63-acde12345678",
    "event_type": "sla_breach",
    "status": "processing",
    "created_at": "2026-01-10T08:28:12"
  }
]


# 📌 Phase Scope

This repository currently implements Phase 1 only.

Future phases (optional):
	•	Phase 2: Queues, retries, idempotency (local)
	•	Phase 3: Cloud deployment (AWS)




