# ✅ ALO Backend MVP – Sprint 1 Backlog (1 Hour Sprint)

## 📅 Sprint Goal

Set up the backend infrastructure for the Automated Life Organizer (ALO) MVP. Deliver working APIs for `users`, `events`, and `reminders` with a connected Supabase PostgreSQL instance.

---

## 🧱 Epic 1: Project Setup & Infrastructure

> **Story 1.1 – Initialize FastAPI Backend**

- [ ] Create new FastAPI project scaffold with Poetry or pip
- [ ] Add `.env`, `.env.example`, and Git ignore rules
- [ ] Set up Docker + Docker Compose for local PostgreSQL + FastAPI

**Est. Time:** 5 mins  
**Priority:** 🔴 Critical

---

## 🧩 Epic 2: Database Schema Setup (Supabase)

> **Story 2.1 – Define core tables in Supabase**

- [ ] Create `users` table
- [ ] Create `events` table
- [ ] Create `reminders` table
- [ ] Add basic seed data for 1 test user and 2 events
- [ ] Run migration via Supabase SQL Editor or CLI

**Est. Time:** 15 mins  
**Priority:** 🔴 Critical

---

## 🧠 Epic 3: Model Layer & DB Integration

> **Story 3.1 – Build SQLAlchemy Models & Pydantic Schemas**

- [ ] Create `User`, `Event`, `Reminder` SQLAlchemy models
- [ ] Create corresponding Pydantic request/response schemas
- [ ] Create reusable `db.py` connection/session file

**Est. Time:** 15 mins  
**Priority:** 🔴 Critical

---

## 🚦 Epic 4: CRUD APIs for Events & Reminders

> **Story 4.1 – Create CRUD endpoints for `events`**

- [ ] `POST /events`: Create an event
- [ ] `GET /events`: List all events for a user
- [ ] `PATCH /events/{id}`: Update event details
- [ ] `DELETE /events/{id}`: Soft delete event (optional)

> **Story 4.2 – Create CRUD endpoints for `reminders`**

- [ ] `POST /reminders`: Create a reminder
- [ ] `GET /reminders`: List all reminders for a user

**Est. Time:** 15 mins  
**Priority:** 🔴 Critical

---

## 🧪 Epic 5: Local Testing & Debugging

> **Story 5.1 – Validate functionality via Postman or curl**

- [ ] Test creating events and reminders
- [ ] Test listing all data for a user
- [ ] Check DB entries in pgAdmin or Supabase UI
- [ ] Fix any integration or schema issues

**Est. Time:** 10 mins  
**Priority:** 🔴 Critical

---

## 📦 Epic 6: GitHub & Docs

> **Story 6.1 – Final project polish & push**

- [ ] Push code to GitHub repo
- [ ] Include updated `README.md`, `.env.example`, and `backlog.md`
- [ ] Document `/docs` API via FastAPI auto-gen

**Est. Time:** 5 mins  
**Priority:** 🟢 Optional but Recommended

---

## ⏳ Total Estimated Time: **60 minutes**

> ⚠️ Focus on `users`, `events`, `reminders`. All other tables (notes, location, assistant logs) come in Sprint 2+.

---

## 🧠 Future Sprints (Not in Scope Today)

- Authentication via Supabase Auth middleware
- Voice input (Whisper or Google Speech-to-Text)
- AI Assistant integration (OpenAI / Ollama)
- Calendar sync (Google / Outlook)
- Frontend dashboard in React or Svelte

---
