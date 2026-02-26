import time
import uuid


class Task:
    """Represents a single task.

    Attributes mirror the data shape defined in task_component_model.md:
      id          -- unique identifier (UUID4 string), generated on creation
      title       -- required, non-empty string
      description -- optional string, defaults to ""
      completed   -- bool, defaults to False
      created_at  -- Unix timestamp (float), set on creation
    """

    def __init__(self, title: str, description: str = ""):
        self.id: str = str(uuid.uuid4())
        self.title: str = title
        self.description: str = description
        self.completed: bool = False
        self.created_at: float = time.time()

    def __repr__(self) -> str:
        status = "done" if self.completed else "todo"
        desc_part = f" | {self.description}" if self.description else ""
        return f"Task({status!r}, title={self.title!r}{desc_part})"

    def to_dict(self) -> dict:
        """Serialise to a plain dict suitable for JSON storage."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Deserialise from a dict loaded from JSON storage."""
        task = cls.__new__(cls)
        task.id = data["id"]
        task.title = data["title"]
        task.description = data.get("description", "")
        task.completed = data.get("completed", False)
        task.created_at = data.get("created_at", time.time())
        return task
