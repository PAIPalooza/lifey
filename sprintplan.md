# 🕐 1-Hour Sprint Plan: ALO MVP (Phase 1 Kickoff)

**Goal:**
Build the core database, backend service, and basic CRUD APIs for `users`, `events`, and `reminders`.

**Environment Assumptions:**

* Backend: **FastAPI + Supabase (PostgreSQL)**
* Auth: Supabase Auth (Email/Password for now)
* Tools: Docker, VS Code, Postman, pgAdmin (optional)
* AI Tooling: Codeium/Copilot/Windsurf/Cody (for speed)

---

## ⏰ Sprint Timeline (60 Minutes)

### ✅ Minute 0–5: Setup & Project Bootstrapping

* [ ] Clone starter FastAPI repo or create new with:

  ```bash
  fastapi startproject alo_backend
  cd alo_backend
  poetry init && poetry add fastapi[all] psycopg2-binary
  ```
* [ ] Initialize Git, `.env`, and `.env.example`
* [ ] Create Dockerfile and docker-compose.yml for FastAPI + PostgreSQL
* [ ] Configure Supabase project (GUI):

  * Enable `email` auth
  * Link project DB via `pgvector` if needed later

---

### ✅ Minute 6–20: Supabase Schema Creation (pgAdmin / SQL file)

* [ ] Create `users`, `events`, and `reminders` tables (from markdown model)
* [ ] Use Supabase SQL Editor or `psql` CLI to run schema
* [ ] Add indexes on `user_id`, `event_id`, and `start_time`
* [ ] Add seed data for one user and 2 sample events

---

### ✅ Minute 21–35: Backend Model Layer

* [ ] Define SQLAlchemy models:

  * `User`, `Event`, `Reminder`
* [ ] Add Pydantic schemas for input/output (CRUD)
* [ ] Setup DB session (`db.py`) and connection pooling

```python
class Event(Base):
    __tablename__ = "events"
    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    start_time = Column(DateTime(timezone=True))
```

---

### ✅ Minute 36–50: FastAPI Router Setup

* [ ] Create routes: `/events`, `/reminders`

  * `GET /events` (list)
  * `POST /events` (create)
  * `PATCH /events/{id}` (update)
  * `DELETE /events/{id}` (soft delete optional)
* [ ] Include routers in `main.py`
* [ ] Add exception handling for invalid data and foreign keys

---

### ✅ Minute 51–60: Testing & Verification

* [ ] Use Postman or Curl to:

  * Add new event
  * Set a reminder
  * Query all events for a user
* [ ] Review logs and DB entries
* [ ] Push to GitHub with a `README.md`

---

## 📂 Output Deliverables

* ✅ `alo_backend/` FastAPI service running via Docker
* ✅ Supabase schema live with real data
* ✅ REST API for events and reminders
* ✅ Initial user auth (via Supabase Auth)
* ✅ GitHub repo pushed with README and `.env.example`

---

## 🧠 Stretch Goals (if time allows)

* Add `notes` table and link to event
* Generate OpenAPI docs via FastAPI (`/docs`)
* Enable CORS for frontend
* Deploy backend to Render or Railway for demo

---
