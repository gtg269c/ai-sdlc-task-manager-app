# Plan: Python Task Manager Code Generation

**Date:** 2026-02-26
**Author:** Software Engineer (Claude)
**Source design:** `aidlc-docs/design-artifacts/task_component_model.md`
**Output files:**
- `taskManager/task.py` — `Task` class
- `taskManager/task_service.py` — `TaskService` class

---

## Scope Note

The task requests a **simplified Python implementation** covering only two features:
- Add a new task
- List all tasks

This is a Python backend representation of the data shape and state-layer logic defined in the component model. The UI layer (React components) is out of scope for this task.

---

## Steps

- [x] **Step 1 — Log prompt in prompts.md**

- [x] **Step 2 — Review source design artifact**
  Read `task_component_model.md`. Key inputs for the Python implementation:
  - **Task data shape:** `id` (UUID), `title` (str, required), `description` (str, optional), `completed` (bool, default False), `created_at` (timestamp)
  - **`addTask` behaviour:** validates title is non-empty, generates id, sets defaults, appends to list
  - **`list tasks` behaviour:** returns tasks in insertion order

- [x] **Step 3 — Clarify storage strategy** ✅ Confirmed: B — JSON file persistence
  `TaskService` reads from / writes to `taskManager/tasks.json`. Data survives between runs.

- [x] **Step 4 — Create `taskManager/` directory if it does not exist**

- [x] **Step 5 — Write `taskManager/task.py`**

  `Task` class mapping directly to the component model's data shape:

  | Python attribute | Type | Notes |
  |-----------------|------|-------|
  | `id` | `str` (UUID4) | Generated in `__init__` using `uuid` stdlib |
  | `title` | `str` | Required; validated non-empty by `TaskService` |
  | `description` | `str` | Defaults to `""` |
  | `completed` | `bool` | Defaults to `False` |
  | `created_at` | `float` | Unix timestamp via `time.time()` |

  The class will include a `__repr__` for readable output when listing tasks.

- [x] **Step 6 — Write `taskManager/task_service.py`**

  `TaskService` class exposing two public methods:

  | Method | Signature | Behaviour |
  |--------|-----------|-----------|
  | `add_task` | `(title: str, description: str = "") -> Task` | Raises `ValueError` if title is blank. Creates and stores a `Task`. Returns the new `Task`. |
  | `list_tasks` | `() -> list[Task]` | Returns all tasks in insertion order. Returns empty list if none. |

  Internal attribute: `_tasks: list[Task]` — the in-memory task store (or file-backed, per Step 3 answer).

- [x] **Step 7 — Review both files for correctness**
  Smoke-tested via Python assertions: add with title+description, add with title only, insertion-order listing, blank-title ValueError, and JSON round-trip reload. All passed. No out-of-scope behaviour included.

- [x] **Step 8 — Commit and push to branch**
