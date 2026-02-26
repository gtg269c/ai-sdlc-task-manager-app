# Task Component Model

**Version:** 1.0
**Date:** 2026-02-26
**Author:** Software Engineer
**Stack:** React (functional components + hooks)
**Source:** `aidlc-docs/design-artifacts/task_management_unit.md`

---

## 1. Component Inventory

| # | Component | Layer | Kind | Responsibility |
|---|-----------|-------|------|----------------|
| 1 | `App` | UI — Root | React function component | Root container; wires all UI components to the state hook |
| 2 | `AddTaskForm` | UI | React function component | Captures title and optional description; validates and submits new task |
| 3 | `FilterControl` | UI | React function component | Renders the show-all / hide-completed toggle |
| 4 | `TaskList` | UI | React function component | Renders the ordered list of visible tasks or the empty state |
| 5 | `TaskItem` | UI | React function component | Renders one task row; handles completion toggle |
| 6 | `EmptyState` | UI | React function component | Renders a message when no tasks are visible |
| 7 | `useTaskStore` | State | Custom React hook | Owns all task data and filter state; exposes operations to UI |
| 8 | `StorageService` | Storage | Plain JS module | Persists and retrieves the task list from durable storage |

---

## 2. Data Shape: Task Object

All components that deal with task data share this shape (derived from the Task entity in the unit doc):

| Field | Type | Notes |
|-------|------|-------|
| `id` | `string` (UUID) | Generated on creation |
| `title` | `string` | Non-empty |
| `description` | `string` | Empty string when not provided |
| `completed` | `boolean` | `false` on creation |
| `createdAt` | `number` (Unix ms) | Set on creation; drives display order |

---

## 3. Component Specifications

---

### 3.1 `App`

**Layer:** UI — Root
**Kind:** React function component

#### Props (received)
_None_ — root component, no parent.

#### Internal State
_None_ — all state is owned by `useTaskStore`.

#### Consumed Hook
| Hook | Values consumed |
|------|----------------|
| `useTaskStore` | `visibleTasks`, `filter`, `addTask`, `toggleComplete`, `setFilter` |

#### Behaviours
| Behaviour | Description |
|-----------|-------------|
| `mount` | Renders the page shell; `useTaskStore` initialises and loads persisted tasks |
| `render` | Renders `AddTaskForm`, `FilterControl`, and `TaskList` (passing required props to each) |

#### Renders
```
App
├── AddTaskForm  (onAddTask → addTask)
├── FilterControl (currentFilter, onFilterChange → setFilter)
└── TaskList      (tasks → visibleTasks, onToggleComplete → toggleComplete)
```

---

### 3.2 `AddTaskForm`

**Layer:** UI
**Kind:** React function component

#### Props (received)
| Prop | Type | Description |
|------|------|-------------|
| `onAddTask` | `(title: string, description: string) => void` | Callback invoked on valid submission |

#### Internal State
| State field | Type | Initial value | Description |
|-------------|------|---------------|-------------|
| `titleValue` | `string` | `""` | Current value of the title input |
| `descriptionValue` | `string` | `""` | Current value of the description input |
| `titleError` | `string \| null` | `null` | Inline validation error; set when title is blank on submit |

#### Behaviours
| Behaviour | Trigger | Description |
|-----------|---------|-------------|
| `handleTitleChange` | Title input change event | Updates `titleValue`; clears `titleError` if set |
| `handleDescriptionChange` | Description input change event | Updates `descriptionValue` |
| `handleSubmit` | Form submit event | Validates `titleValue` is non-empty. If blank: sets `titleError`, does not call `onAddTask`. If valid: calls `onAddTask(titleValue, descriptionValue)`, then resets `titleValue`, `descriptionValue`, and `titleError` to initial values |

#### AC Coverage
| AC | Covered by |
|----|-----------|
| AC-001-1 | `handleSubmit` calls `onAddTask` → task appears in list |
| AC-001-2 | `handleSubmit` sets `titleError` when title is blank |
| AC-001-3 | `handleSubmit` calls `onAddTask` with empty `descriptionValue` |
| AC-001-4 | `handleSubmit` calls `onAddTask` with both `titleValue` and `descriptionValue` |
| AC-001-5 | `handleSubmit` resets both input fields after successful submission |

---

### 3.3 `FilterControl`

**Layer:** UI
**Kind:** React function component

#### Props (received)
| Prop | Type | Description |
|------|------|-------------|
| `currentFilter` | `'all' \| 'incomplete'` | The active filter; drives the toggle's visual state |
| `onFilterChange` | `(filter: 'all' \| 'incomplete') => void` | Callback invoked when the user toggles the filter |

#### Internal State
_None._

#### Behaviours
| Behaviour | Trigger | Description |
|-----------|---------|-------------|
| `handleToggle` | Toggle control interaction | If `currentFilter` is `'all'`, calls `onFilterChange('incomplete')`. If `currentFilter` is `'incomplete'`, calls `onFilterChange('all')` |

#### AC Coverage
| AC | Covered by |
|----|-----------|
| AC-003-3 | `handleToggle` → `onFilterChange('incomplete')` → only incomplete tasks shown |
| AC-003-4 | `handleToggle` → `onFilterChange('all')` → all tasks shown |

---

### 3.4 `TaskList`

**Layer:** UI
**Kind:** React function component

#### Props (received)
| Prop | Type | Description |
|------|------|-------------|
| `tasks` | `Task[]` | The visible (already filtered) list of tasks in insertion order |
| `onToggleComplete` | `(taskId: string) => void` | Passed down to each `TaskItem` |

#### Internal State
_None._

#### Behaviours
| Behaviour | Condition | Description |
|-----------|-----------|-------------|
| `render — empty state` | `tasks.length === 0` | Renders `EmptyState` |
| `render — list` | `tasks.length > 0` | Renders a `TaskItem` for each task, in array order (insertion order maintained by `useTaskStore`) |

#### AC Coverage
| AC | Covered by |
|----|-----------|
| AC-002-1 | Renders all tasks passed in `tasks` prop |
| AC-002-4 | Renders `EmptyState` when `tasks` is empty |
| AC-002-5 | Preserves order of `tasks` prop (order enforced by `useTaskStore`) |

---

### 3.5 `TaskItem`

**Layer:** UI
**Kind:** React function component

#### Props (received)
| Prop | Type | Description |
|------|------|-------------|
| `task` | `Task` | The task object to render |
| `onToggleComplete` | `(taskId: string) => void` | Callback invoked when the user clicks the completion control |

#### Internal State
_None._

#### Behaviours
| Behaviour | Trigger | Description |
|-----------|---------|-------------|
| `handleToggle` | Completion control click | Calls `onToggleComplete(task.id)` |
| `render — title` | Always | Renders `task.title` |
| `render — description` | `task.description` is non-empty | Renders `task.description` |
| `render — completed style` | `task.completed === true` | Applies a visual distinction (e.g. strikethrough styling) to the task row |
| `render — incomplete style` | `task.completed === false` | Renders with standard (non-distinguished) styling |

#### AC Coverage
| AC | Covered by |
|----|-----------|
| AC-002-2 | Renders only title when `task.description` is empty |
| AC-002-3 | Renders both title and description when `task.description` is non-empty |
| AC-003-1 | Applies completed visual style when `task.completed` is `true` |
| AC-003-2 | Title and description are always rendered regardless of `task.completed` |
| AC-003-5 | `handleToggle` → `onToggleComplete` → `useTaskStore.toggleComplete` flips the boolean |

---

### 3.6 `EmptyState`

**Layer:** UI
**Kind:** React function component

#### Props (received)
_None._

#### Internal State
_None._

#### Behaviours
| Behaviour | Description |
|-----------|-------------|
| `render` | Renders a static informational message (e.g. "No tasks yet. Add one above.") |

#### AC Coverage
| AC | Covered by |
|----|-----------|
| AC-002-4 | Provides the empty-state message when no tasks are visible |

---

### 3.7 `useTaskStore`

**Layer:** State
**Kind:** Custom React hook

#### Internal State
| State field | Type | Initial value | Description |
|-------------|------|---------------|-------------|
| `tasks` | `Task[]` | Loaded from `StorageService.load()` on first render | The authoritative, ordered list of all tasks |
| `filter` | `'all' \| 'incomplete'` | `'all'` | The active filter selection |

#### Derived Values
| Value | Derivation |
|-------|-----------|
| `visibleTasks` | If `filter === 'all'`: returns `tasks` unchanged. If `filter === 'incomplete'`: returns `tasks` filtered to those where `completed === false`. Order is always preserved. |

#### Exposed Interface
```
{
  tasks: Task[],
  visibleTasks: Task[],
  filter: 'all' | 'incomplete',
  addTask(title: string, description: string): void,
  toggleComplete(taskId: string): void,
  setFilter(filter: 'all' | 'incomplete'): void
}
```

#### Behaviours
| Behaviour | Description |
|-----------|-------------|
| `initialize` | On first render, calls `StorageService.load()` to populate `tasks`. If storage is empty, `tasks` starts as `[]`. |
| `addTask(title, description)` | Creates a new Task object: generates a unique `id`, sets `title`, sets `description` (empty string if not provided), sets `completed = false`, sets `createdAt = Date.now()`. Appends to `tasks`. Calls `StorageService.save(updatedTasks)`. |
| `toggleComplete(taskId)` | Finds the task with matching `id`. Flips its `completed` boolean. Calls `StorageService.save(updatedTasks)`. |
| `setFilter(filter)` | Updates `filter` state to the provided value. No storage write needed (filter is UI-session state only). |

#### AC Coverage
| AC | Covered by |
|----|-----------|
| AC-001-1 | `addTask` appends task → `visibleTasks` updates → `TaskList` re-renders |
| AC-001-3 | `addTask` stores empty `description` without error |
| AC-001-4 | `addTask` stores both `title` and `description` |
| AC-002-1 | `visibleTasks` returns all tasks when `filter === 'all'` |
| AC-002-5 | `tasks` array is append-only; insertion order preserved |
| AC-003-3 | `setFilter('incomplete')` → `visibleTasks` excludes completed tasks |
| AC-003-4 | `setFilter('all')` → `visibleTasks` returns all tasks |
| AC-003-5 | `toggleComplete` flips `completed` boolean |

---

### 3.8 `StorageService`

**Layer:** Storage
**Kind:** Plain JavaScript module (no React)

#### Attributes
_None_ — stateless module; holds no data of its own.

#### Interface
```
StorageService.load(): Task[]
StorageService.save(tasks: Task[]): void
```

#### Behaviours
| Behaviour | Description |
|-----------|-------------|
| `load()` | Reads the persisted task array from durable storage. Returns the parsed `Task[]`. Returns `[]` if no data is found or if parsing fails. |
| `save(tasks)` | Serialises the `Task[]` and writes it to durable storage. Called by `useTaskStore` after every mutation (`addTask`, `toggleComplete`). |

> **Implementation note:** The storage mechanism (localStorage, IndexedDB, etc.) is not specified here — that decision is deferred to implementation. The contract above is the only constraint.

#### AC Coverage
| AC | Covered by |
|----|-----------|
| AC-001-1 | `save()` called after `addTask`; `load()` restores tasks on next session |
| AC-003-5 | `save()` called after `toggleComplete`; persists the toggled state |

---

## 4. Component Interaction Model

### 4.1 Initialisation Flow

```
Browser loads page
  └─▶ App mounts
        └─▶ useTaskStore (initialize)
              └─▶ StorageService.load()
                    └─▶ returns Task[] (or [])
                          └─▶ tasks state populated
                                └─▶ App renders
                                      ├─▶ AddTaskForm (empty)
                                      ├─▶ FilterControl (filter = 'all')
                                      └─▶ TaskList
                                            ├─▶ [no tasks] → EmptyState
                                            └─▶ [tasks exist] → TaskItem × N
```

### 4.2 Add Task Flow (US-001)

```
User types title [+ description] and submits AddTaskForm
  └─▶ AddTaskForm.handleSubmit
        ├─▶ [title blank] → sets titleError, stops here
        └─▶ [title valid]
              └─▶ calls props.onAddTask(titleValue, descriptionValue)
                    └─▶ App passes useTaskStore.addTask
                          └─▶ useTaskStore.addTask(title, description)
                                ├─▶ Creates Task { id, title, description, completed:false, createdAt }
                                ├─▶ Appends to tasks[]
                                ├─▶ StorageService.save(tasks)
                                └─▶ React re-renders
                                      └─▶ AddTaskForm resets fields
                                      └─▶ TaskList shows updated visibleTasks
```

### 4.3 View Task List Flow (US-002)

```
App renders (after init or after any state change)
  └─▶ useTaskStore derives visibleTasks from tasks + filter
        └─▶ TaskList receives visibleTasks as props.tasks
              ├─▶ [visibleTasks.length === 0] → renders EmptyState
              └─▶ [visibleTasks.length > 0]
                    └─▶ renders TaskItem for each task
                          ├─▶ always renders task.title
                          ├─▶ renders task.description only if non-empty
                          └─▶ applies completed visual style if task.completed === true
```

### 4.4 Toggle Completion Flow (US-003)

```
User clicks completion control on a TaskItem
  └─▶ TaskItem.handleToggle
        └─▶ calls props.onToggleComplete(task.id)
              └─▶ App passes useTaskStore.toggleComplete
                    └─▶ useTaskStore.toggleComplete(taskId)
                          ├─▶ Finds task by id
                          ├─▶ Flips task.completed boolean
                          ├─▶ StorageService.save(tasks)
                          └─▶ React re-renders
                                └─▶ TaskItem reflects new completed state
                                └─▶ FilterControl-driven filter may now affect visibleTasks
```

### 4.5 Filter Toggle Flow (US-003)

```
User interacts with FilterControl
  └─▶ FilterControl.handleToggle
        └─▶ calls props.onFilterChange(newFilter)
              └─▶ App passes useTaskStore.setFilter
                    └─▶ useTaskStore.setFilter(newFilter)
                          ├─▶ updates filter state
                          └─▶ React re-renders
                                └─▶ useTaskStore re-derives visibleTasks
                                └─▶ TaskList re-renders with filtered list
```

### 4.6 Component Dependency Diagram

```
┌─────────────────────────────────────────────────────────┐
│                         App                              │
│                                                          │
│  ┌──────────────────┐  ┌────────────┐  ┌─────────────┐  │
│  │   AddTaskForm    │  │FilterControl│  │  TaskList   │  │
│  │                  │  │            │  │             │  │
│  │ props:           │  │ props:     │  │ props:      │  │
│  │  onAddTask()     │  │  current   │  │  tasks[]    │  │
│  │                  │  │  Filter    │  │  onToggle   │  │
│  │ state:           │  │  onChange()│  │  Complete() │  │
│  │  titleValue      │  └────────────┘  │             │  │
│  │  descValue       │                  │  renders:   │  │
│  │  titleError      │                  │  TaskItem×N │  │
│  └──────────────────┘                  │  EmptyState │  │
│                                        └──────┬──────┘  │
│                                               │          │
│                           ┌───────────────────┘          │
│                           │  TaskItem                    │
│                           │  props: task, onToggle()     │
│                           └──────────────────────────────│
└──────────────┬──────────────────────────────────────────┘
               │ consumes
               ▼
┌─────────────────────────────────────────────────────────┐
│                    useTaskStore (hook)                    │
│                                                          │
│  state:  tasks[], filter                                 │
│  derived: visibleTasks[]                                 │
│  exposes: addTask(), toggleComplete(), setFilter()       │
└──────────────────────────┬──────────────────────────────┘
                           │ load() / save()
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    StorageService (module)                │
│                                                          │
│  load(): Task[]        save(tasks: Task[]): void         │
└─────────────────────────────────────────────────────────┘
```

---

## 5. Acceptance Criteria Traceability

All 15 acceptance criteria from the three user stories are covered.

| AC | Story | Primary Component | Supporting Component(s) |
|----|-------|-------------------|-------------------------|
| AC-001-1 | US-001 | `AddTaskForm.handleSubmit` | `useTaskStore.addTask`, `TaskList` |
| AC-001-2 | US-001 | `AddTaskForm.handleSubmit` (validation) | — |
| AC-001-3 | US-001 | `AddTaskForm.handleSubmit` | `useTaskStore.addTask` |
| AC-001-4 | US-001 | `AddTaskForm.handleSubmit` | `useTaskStore.addTask` |
| AC-001-5 | US-001 | `AddTaskForm.handleSubmit` (form reset) | — |
| AC-002-1 | US-002 | `TaskList` | `useTaskStore` (visibleTasks) |
| AC-002-2 | US-002 | `TaskItem` (conditional description render) | — |
| AC-002-3 | US-002 | `TaskItem` (title + description render) | — |
| AC-002-4 | US-002 | `TaskList` → `EmptyState` | — |
| AC-002-5 | US-002 | `useTaskStore` (append-only tasks[]) | `TaskList` |
| AC-003-1 | US-003 | `TaskItem` (completed visual style) | — |
| AC-003-2 | US-003 | `TaskItem` (always renders title + description) | — |
| AC-003-3 | US-003 | `FilterControl.handleToggle` | `useTaskStore.setFilter`, `useTaskStore` (visibleTasks) |
| AC-003-4 | US-003 | `FilterControl.handleToggle` | `useTaskStore.setFilter`, `useTaskStore` (visibleTasks) |
| AC-003-5 | US-003 | `TaskItem.handleToggle` | `useTaskStore.toggleComplete` |
