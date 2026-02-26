# Task Management Unit

**Version:** 1.0
**Date:** 2026-02-26
**Author:** Software Architect
**Source Stories:** `aidlc-docs/story-artifacts/mvp_user_stories.md`

---

## 1. Unit Overview

| Field | Value |
|-------|-------|
| **Unit Name** | Task Management Unit |
| **Persona** | Personal User (single user, no authentication) |
| **Purpose** | Encapsulates all behaviour for creating, viewing, and completing tasks |
| **Stories Included** | US-001, US-002, US-003 |

This unit is the sole functional unit of the MVP. It owns the full lifecycle of a task from creation through completion. There are no dependencies on other units.

---

## 2. In Scope

- Creating a task with a required title and an optional description
- Displaying all tasks in a list ordered by insertion
- Marking a task as complete or toggling it back to incomplete
- Filtering the task list to show all tasks or only incomplete tasks
- Showing an empty-state message when no tasks exist

## 3. Out of Scope

- User authentication or multi-user support
- Editing a task after it has been created
- Deleting or archiving tasks
- Due dates, priorities, categories, or any additional task fields
- Sorting or searching tasks
- Pagination

---

## 4. Data Model

### 4.1 Task Entity

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | string / uuid | Yes | Unique identifier, generated on creation |
| `title` | string | Yes | Cannot be empty |
| `description` | string | No | Defaults to empty / null |
| `completed` | boolean | Yes | Defaults to `false` on creation |
| `createdAt` | timestamp | Yes | Set on creation, used for insertion-order display |

> **Note:** No update timestamp is needed — tasks are not editable after creation.

---

## 5. Component Responsibilities

### 5.1 UI Layer

- Render the task input form (title field + description field + submit button)
- Validate that the title field is non-empty before submission; display an inline error if blank
- Clear the form after a successful submission
- Render the task list, showing each task's title and (if present) description
- Render the completion toggle control on each task item
- Apply a visual distinction (e.g. strikethrough, muted colour) to completed tasks
- Render the show/hide toggle for completed tasks
- Render an empty-state message when the list is empty

### 5.2 State Layer

- Hold the authoritative list of tasks in memory
- Expose operations: `addTask(title, description)`, `toggleComplete(taskId)`, `setFilter(all | incomplete)`
- Derive the visible task list by applying the active filter before passing to the UI layer
- Maintain insertion order (tasks are appended; no reordering)

### 5.3 Storage Layer

- Persist the task list so it survives page refresh
- Provide `load()` and `save(tasks)` operations consumed by the state layer
- Implementation detail (localStorage, IndexedDB, etc.) is left to the developer — the interface contract is the only constraint here

---

## 6. Component Interaction Diagram

```
┌──────────────────────────────────────────┐
│               UI Layer                   │
│  ┌─────────────────┐  ┌───────────────┐  │
│  │  Add Task Form  │  │  Task List    │  │
│  └────────┬────────┘  └───────┬───────┘  │
│           │  addTask()        │ toggleComplete()
│           │                  │ setFilter()
└───────────┼──────────────────┼───────────┘
            ▼                  ▼
┌──────────────────────────────────────────┐
│             State Layer                  │
│  tasks[], filter, derived visibleTasks   │
└───────────────────┬──────────────────────┘
                    │ load() / save()
                    ▼
┌──────────────────────────────────────────┐
│            Storage Layer                 │
│  (localStorage or equivalent)            │
└──────────────────────────────────────────┘
```

---

## 7. User Stories (Embedded in Full)

---

### US-001: Add a New Task

**Story:**
> As a personal user,
> I want to add a new task with a title and an optional description,
> so that I can capture things I need to do.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| AC-001-1 | I am on the task manager | I enter a task title and submit | The new task appears in my task list |
| AC-001-2 | I am adding a task | I leave the title field empty and submit | The task is not saved and I am informed the title is required |
| AC-001-3 | I am adding a task | I enter a title but no description and submit | The task is saved with only the title |
| AC-001-4 | I am adding a task | I enter both a title and a description and submit | The task is saved with both the title and the description |
| AC-001-5 | I have successfully submitted a task | — | The input form is cleared so I can immediately add another task |

**Out of Scope:** Due dates, priority levels, categories, or any other task fields. Editing a task after it has been added.

---

### US-002: View My Task List

**Story:**
> As a personal user,
> I want to see all my tasks displayed in a list,
> so that I can review everything I need to do at a glance.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| AC-002-1 | I have added one or more tasks | I view the task list | All tasks are displayed |
| AC-002-2 | A task has a title only | It appears in the list | Only the title is shown |
| AC-002-3 | A task has a title and a description | It appears in the list | Both the title and description are shown |
| AC-002-4 | I have not added any tasks yet | I view the task list | An empty-state message is shown indicating there are no tasks |
| AC-002-5 | I have added multiple tasks | I view the task list | Tasks are displayed in the order they were added |

**Out of Scope:** Sorting, searching, or filtering by any field other than completion status. Pagination.

---

### US-003: Mark a Task as Complete

**Story:**
> As a personal user,
> I want to mark a task as complete and control whether completed tasks are visible,
> so that I can track my progress and keep my active list focused.

**Acceptance Criteria:**

| # | Given | When | Then |
|---|-------|------|------|
| AC-003-1 | I am viewing my task list | I mark a task as complete | The task is visually distinguished from incomplete tasks |
| AC-003-2 | A task is marked as complete | I view the task | Its title and description are still visible and unchanged |
| AC-003-3 | I am viewing all tasks | I choose to hide completed tasks | Only incomplete tasks are shown |
| AC-003-4 | I am viewing only incomplete tasks | I choose to show all tasks | All tasks (complete and incomplete) are shown |
| AC-003-5 | A task has been marked complete | I interact with it again | It is toggled back to incomplete |

**Out of Scope:** Deleting tasks. Archiving completed tasks. Any permanent removal of tasks or task data.

---

## 8. Story Traceability Summary

| Story ID | Title | AC Count | Component Owners |
|----------|-------|----------|-----------------|
| US-001 | Add a new task | 5 | UI Layer, State Layer, Storage Layer |
| US-002 | View my task list | 5 | UI Layer, State Layer |
| US-003 | Mark a task as complete | 5 | UI Layer, State Layer, Storage Layer |
