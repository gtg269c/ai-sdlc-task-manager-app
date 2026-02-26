from flask import Flask, jsonify, request

from task_service import TaskService

app = Flask(__name__)
service = TaskService()


@app.route("/tasks", methods=["POST"])
def add_task():
    """Create a new task.

    Request body (JSON):
        {
            "title":       "<string, required>",
            "description": "<string, optional>"
        }

    Responses:
        201  { "id": "...", "title": "...", "description": "...",
               "completed": false, "created_at": ... }
        400  { "error": "Task title is required and cannot be blank." }
    """
    body = request.get_json(silent=True) or {}
    title = body.get("title", "")
    description = body.get("description", "")

    try:
        task = service.add_task(title, description)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(task.to_dict()), 201


@app.route("/tasks", methods=["GET"])
def list_tasks():
    """Return all tasks in insertion order.

    Response:
        200  [ { "id": "...", "title": "...", "description": "...",
                 "completed": false, "created_at": ... }, ... ]
    """
    tasks = service.list_tasks()
    return jsonify([task.to_dict() for task in tasks]), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
