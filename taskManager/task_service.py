import json
import os

from task import Task


class TaskService:
    """Manages the task list with JSON file persistence.

    Tasks are stored in a JSON file (default: tasks.json in the same
    directory as this module). The list is loaded once on construction
    and saved after every mutation.

    Public methods (the two in-scope features):
      add_task(title, description) -> Task
      list_tasks()                 -> list[Task]
    """

    _DEFAULT_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")

    def __init__(self, storage_file: str = None):
        self._storage_file: str = storage_file or self._DEFAULT_FILE
        self._tasks: list[Task] = self._load()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def add_task(self, title: str, description: str = "") -> Task:
        """Create a new task and persist it.

        Args:
            title:       Required. Raises ValueError if blank.
            description: Optional. Defaults to "".

        Returns:
            The newly created Task.
        """
        if not title or not title.strip():
            raise ValueError("Task title is required and cannot be blank.")
        task = Task(title.strip(), description)
        self._tasks.append(task)
        self._save()
        return task

    def list_tasks(self) -> list[Task]:
        """Return all tasks in insertion order.

        Returns an empty list when no tasks have been added.
        """
        return list(self._tasks)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load(self) -> list[Task]:
        """Load tasks from the JSON storage file.

        Returns an empty list if the file does not exist or is invalid.
        """
        if not os.path.exists(self._storage_file):
            return []
        try:
            with open(self._storage_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError):
            return []

    def _save(self) -> None:
        """Persist the current task list to the JSON storage file."""
        with open(self._storage_file, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in self._tasks], f, indent=2)
