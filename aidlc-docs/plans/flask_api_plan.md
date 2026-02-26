# Plan: Flask API for TaskService

**Date:** 2026-02-26
**Author:** Software Engineer (Claude)
**Source:** `taskManager/task_service.py`
**Output:** `taskManager/app.py`

---

## Services to Expose

| TaskService method | HTTP verb | Route | Description |
|--------------------|-----------|-------|-------------|
| `add_task(title, description)` | `POST` | `/tasks` | Create a new task. Accepts JSON body. Returns the created task. |
| `list_tasks()` | `GET` | `/tasks` | Return all tasks in insertion order. |

**Proposed request / response shapes:**

```
POST /tasks
  Body (JSON):   { "title": "Buy milk", "description": "Full fat" }
  201 response:  { "id": "...", "title": "...", "description": "...", "completed": false, "created_at": ... }
  400 response:  { "error": "Task title is required and cannot be blank." }

GET /tasks
  200 response:  [ { "id": "...", "title": "...", ... }, ... ]
```

---

## Steps

- [x] **Step 1 — Log prompt in prompts.md**

- [x] **Step 2 — Review source files**
  Read `taskManager/task_service.py` and `taskManager/task.py`. Confirmed two public methods:
  `add_task(title, description)` and `list_tasks()`. Task already has `to_dict()` for JSON serialisation.

- [x] **Step 3 — Clarify dependency tracking** ✅ Confirmed: A — create `taskManager/requirements.txt` listing `flask`

- [x] **Step 4 — Write `taskManager/app.py` and `taskManager/requirements.txt`**

  The Flask application will:
  - Create a single module-level `TaskService` instance (shared across requests)
  - Register two routes as described in the table above
  - Return all responses as JSON
  - Map `ValueError` from `add_task` to HTTP 400 with an `{ "error": "..." }` body
  - Run on **port 5000** (Flask default) when executed directly

  > **Note:** `app.py` is placed inside `taskManager/` alongside the existing modules
  > so the existing `from task import Task` import in `task_service.py` continues to
  > work without modification. The app must be started from the `taskManager/` directory.

- [x] **Step 5 — Install Flask and verify the app starts**
  Flask 3.1.3 installed and importable.

- [x] **Step 6 — Smoke test both endpoints**
  Used Flask test client to confirm:
  - `POST /tasks` title+description → 201 with full task JSON ✓
  - `POST /tasks` title only → 201 with empty description ✓
  - `POST /tasks` blank title → 400 with `{ "error": "..." }` ✓
  - `GET /tasks` → 200 with both tasks in insertion order ✓

- [ ] **Step 7 — Commit and push to branch**
