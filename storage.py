import json
from pathlib import Path
from typing import Literal, TypeAlias, TypedDict

TaskStatus: TypeAlias = Literal["done", "in-progress", "todo"]


DatabaseRow = TypedDict(
    "DatabaseRow",
    {
        "description": str,
        "status": TaskStatus,
        "createdAt": str,
        "updatedAt": str,
    },
)

# JSON object keys are strings, so IDs are stored as strings in this mapping.
Database: TypeAlias = dict[str, DatabaseRow]


def load_db(path: Path) -> Database:
    """Load the database, returning an empty database if the file is missing."""
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON content in {path}: {exc.msg} "
            f"(line {exc.lineno}, column {exc.colno})"
        ) from exc

    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object in {path}")

    # Validate the loaded data at runtime; TypedDict alone does not validate JSON.
    for task_id, task in data.items():
        if not isinstance(task_id, str) or not task_id.isdigit():
            raise ValueError(f"Invalid task ID key {task_id!r} in {path}")
        if not isinstance(task, dict):
            raise ValueError(f"Task {task_id} must be a JSON object")

        required_fields = {"description", "status", "createdAt", "updatedAt"}
        if set(task) != required_fields:
            raise ValueError(
                f"Task {task_id} must contain exactly these fields: "
                f"{', '.join(sorted(required_fields))}"
            )
        if not isinstance(task["description"], str):
            raise ValueError(f"Task {task_id}: description must be a string")
        if task["status"] not in ("todo", "in-progress", "done"):
            raise ValueError(f"Task {task_id}: invalid status {task['status']!r}")
        if not isinstance(task["createdAt"], str) or not isinstance(
            task["updatedAt"], str
        ):
            raise ValueError(f"Task {task_id}: timestamps must be strings")

    return data


def save_db(database: Database, path: Path) -> None:
    """Save the database as formatted UTF-8 JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(database, file, indent=2, ensure_ascii=False)
        file.write("\n")
