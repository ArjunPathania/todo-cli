from datetime import datetime

from storage import Database, DatabaseRow, TaskStatus


def _next_task_id(database: Database) -> int:
    """Return the next ID without reusing IDs left by deleted tasks."""
    return max((int(task_id) for task_id in database), default=0) + 1


def _get_task(database: Database, task_id: int) -> DatabaseRow:
    """Return a task or raise a helpful error if it does not exist."""
    key = str(task_id)
    try:
        return database[key]
    except KeyError:
        raise KeyError(f"Task with ID {task_id} does not exist.") from None


def add_task(database: Database, description: str) -> int:
    """Add a task to the in-memory database and return its ID."""
    description = description.strip()
    if not description:
        raise ValueError("Task description cannot be empty.")

    task_id = _next_task_id(database)
    timestamp = datetime.now().isoformat(timespec="seconds")

    task: DatabaseRow = {
        "description": description,
        "status": "todo",
        "createdAt": timestamp,
        "updatedAt": timestamp,
    }
    database[str(task_id)] = task
    return task_id


def list_tasks(
    database: Database,
    status: TaskStatus | None = None,
) -> list[tuple[int, DatabaseRow]]:
    tasks = [
        (int(task_id), task)
        for task_id, task in database.items()
        if status is None or task["status"] == status
    ]

    return sorted(tasks, key=lambda item: item[0])


def update_task(
    database: Database,
    task_id: int,
    description: str | None = None,
    status: TaskStatus | None = None,
) -> None:
    """Update a task's description and/or status in memory."""
    if description is None and status is None:
        raise ValueError("Provide at least one of description or status.")

    task = _get_task(database, task_id)

    if description is not None:
        description = description.strip()
        if not description:
            raise ValueError("Task description cannot be empty.")
        task["description"] = description

    if status is not None:
        task["status"] = status

    task["updatedAt"] = datetime.now().isoformat(timespec="seconds")


def set_task_status(
    database: Database,
    task_id: int,
    status: TaskStatus,
) -> None:
    """Set a task's status and update its timestamp."""
    task = _get_task(database, task_id)
    task["status"] = status
    task["updatedAt"] = datetime.now().isoformat(timespec="seconds")


def delete_task(database: Database, task_id: int) -> None:
    """Delete a task from the in-memory database."""
    key = str(task_id)

    if key not in database:
        raise KeyError(f"Task with ID {task_id} does not exist.")
    for id in database:
        if int(id) > int(key):
            database[str(int(id) - 1)] = database[id]
    max_id = max(int(task_id) for task_id in database)
    database.pop(str(max_id))
