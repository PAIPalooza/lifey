# 📦 Automated Life Organizer – Supabase Data Model

> This schema supports core features like event scheduling, reminders, calendar syncing, and AI assistant history, designed for use with [Supabase](https://supabase.com/).

---

## 🧑‍💼 `users`

Stores core user data.

| Column       | Type                       | Description                |
| ------------ | -------------------------- | -------------------------- |
| `id`         | `uuid` (PK)                | User ID (Supabase Auth)    |
| `email`      | `text` (UNIQUE, NOT NULL)  | User email                 |
| `full_name`  | `text`                     | Full name                  |
| `timezone`   | `text` (default `'UTC'`)   | Preferred time zone        |
| `created_at` | `timestamp with time zone` | Account creation timestamp |

---

## 📅 `calendars`

Linked third-party calendars.

| Column                 | Type                       | Description                        |
| ---------------------- | -------------------------- | ---------------------------------- |
| `id`                   | `uuid` (PK)                | Internal calendar ID               |
| `user_id`              | `uuid` (FK)                | Reference to `users` table         |
| `provider`             | `text`                     | `'google'`, `'outlook'`, `'apple'` |
| `external_calendar_id` | `text`                     | ID from external calendar service  |
| `access_token`         | `text`                     | OAuth token                        |
| `refresh_token`        | `text`                     | OAuth refresh token                |
| `token_expiry`         | `timestamp with time zone` | Expiration timestamp               |
| `synced_at`            | `timestamp with time zone` | Last sync timestamp                |

---

## 📆 `events`

Scheduled user events, tasks, or appointments.

| Column            | Type                                    | Description              |
| ----------------- | --------------------------------------- | ------------------------ |
| `id`              | `uuid` (PK)                             | Event ID                 |
| `user_id`         | `uuid` (FK)                             | Owner                    |
| `title`           | `text` (NOT NULL)                       | Event title              |
| `description`     | `text`                                  | Optional details         |
| `start_time`      | `timestamp with time zone`              | Start time               |
| `end_time`        | `timestamp with time zone`              | End time                 |
| `location`        | `text`                                  | Location name or address |
| `priority`        | `text` (`low`, `medium`, `high`)        | Task priority            |
| `status`          | `text` (`pending`, `done`, `cancelled`) | Current status           |
| `calendar_id`     | `uuid` (FK)                             | Linked external calendar |
| `recurrence_rule` | `jsonb`                                 | iCal RRULE JSON          |
| `created_at`      | `timestamp with time zone`              | Created timestamp        |

---

## ⏰ `reminders`

Alert rules tied to events.

| Column      | Type                            | Description           |
| ----------- | ------------------------------- | --------------------- |
| `id`        | `uuid` (PK)                     | Reminder ID           |
| `event_id`  | `uuid` (FK)                     | Linked event          |
| `remind_at` | `timestamp with time zone`      | Time to send reminder |
| `method`    | `text` (`push`, `email`, `sms`) | Notification channel  |
| `delivered` | `boolean`                       | Status of reminder    |

---

## 🗒️ `notes`

Rich notes attached to events (text, files, voice).

| Column       | Type                                     | Description                |
| ------------ | ---------------------------------------- | -------------------------- |
| `id`         | `uuid` (PK)                              | Note ID                    |
| `event_id`   | `uuid` (FK)                              | Associated event           |
| `user_id`    | `uuid` (FK)                              | Owner                      |
| `content`    | `text`                                   | Freeform note              |
| `note_type`  | `text` (`text`, `voice`, `link`, `file`) | Content type               |
| `file_url`   | `text`                                   | For file/voice attachments |
| `created_at` | `timestamp with time zone`               | Timestamp                  |

---

## ⚙️ `preferences`

User-level settings and app behavior.

| Column                   | Type                                  | Description             |
| ------------------------ | ------------------------------------- | ----------------------- |
| `user_id`                | `uuid` (PK, FK)                       | Owner                   |
| `default_view`           | `text` (`daily`, `weekly`, `monthly`) | UI default layout       |
| `notification_lead_time` | `integer` (in minutes)                | Default reminder buffer |
| `receive_sms`            | `boolean`                             | Enable SMS reminders    |
| `receive_email`          | `boolean`                             | Enable email reminders  |

---

## 🤖 `assistant_history`

Logs of AI assistant interactions.

| Column       | Type                       | Description                   |
| ------------ | -------------------------- | ----------------------------- |
| `id`         | `uuid` (PK)                | Entry ID                      |
| `user_id`    | `uuid` (FK)                | Owner                         |
| `message`    | `text`                     | User input                    |
| `response`   | `text`                     | AI response                   |
| `intent`     | `text`                     | Parsed intent or command type |
| `created_at` | `timestamp with time zone` | Timestamp                     |

---

## 📣 `notifications`

Track individual sent messages across channels.

| Column        | Type                                | Description        |
| ------------- | ----------------------------------- | ------------------ |
| `id`          | `uuid` (PK)                         | Notification ID    |
| `reminder_id` | `uuid` (FK)                         | Source reminder    |
| `sent_at`     | `timestamp with time zone`          | Delivery timestamp |
| `status`      | `text` (`queued`, `sent`, `failed`) | Message state      |
| `channel`     | `text` (`push`, `email`, `sms`)     | Delivery method    |
| `recipient`   | `text`                              | Destination        |
| `content`     | `text`                              | Message content    |

---

## 📍 `location_triggers` (Optional)

For geofenced reminder support.

| Column          | Type                       | Description        |
| --------------- | -------------------------- | ------------------ |
| `id`            | `uuid` (PK)                | Trigger ID         |
| `user_id`       | `uuid` (FK)                | Owner              |
| `event_id`      | `uuid` (FK)                | Related event      |
| `location_name` | `text`                     | Label for location |
| `lat`           | `decimal`                  | Latitude           |
| `lng`           | `decimal`                  | Longitude          |
| `radius_meters` | `integer` (default: `100`) | Trigger radius     |
| `triggered`     | `boolean`                  | If triggered       |

---

## 📥 Suggested Enhancements

* `event_tags` table for custom tagging/categorization
* `ai_embeddings` table using pgvector or Chroma for LLM-enhanced search
* `shared_calendars` for team or family use
* `voice_transcripts` if voice notes become popular

---


