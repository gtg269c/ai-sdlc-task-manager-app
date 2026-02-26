# MVP User Stories — Personal Task Manager

**Version:** 1.0
**Date:** 2026-02-26
**Scope:** Minimum viable product — two core features (add task, view task list) plus task completion tracking as confirmed by product owner.

---

## Persona

**The Personal User** — An individual who uses this application solely for their own task management. There is only one user; no authentication or multi-user support is in scope.

---

## User Stories

---

### US-001: Add a New Task

**Title:** Add a new task

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

**Out of Scope:**
- Due dates, priority levels, categories, or any other task fields
- Editing a task after it has been added

---

### US-002: View My Task List

**Title:** View the task list

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

**Out of Scope:**
- Sorting, searching, or filtering by any field other than completion status (see US-003)
- Pagination

---

### US-003: Mark a Task as Complete

**Title:** Mark a task as complete and toggle completed task visibility

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

**Out of Scope:**
- Deleting tasks
- Archiving completed tasks
- Any permanent removal of tasks or task data

---

## Summary

| Story ID | Title | Priority |
|----------|-------|----------|
| US-001 | Add a new task | Must Have |
| US-002 | View my task list | Must Have |
| US-003 | Mark a task as complete | Must Have |
