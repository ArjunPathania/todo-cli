import json
from pathlib import Path
from typing import (
    Literal,
    TypeAlias,
    TypedDict,
)

TaskStatus: TypeAlias = Literal["done", "in-progress", "todo"]

DatabaseRow = TypedDict(
    "DatabaseRow",
    {"description": str, "status": TaskStatus, "createdAt": str, "updatedAt": str},
)

Database: TypeAlias = dict[str, DatabaseRow]


def load_db(path: Path) -> Database:
    """Load the database, returning an empty database if the file is missing."""
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"JSON file not found at {path}; starting with an empty database.")
        return {}
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON content in {path}") from exc

    if not isinstance(data, dict):
        raise TypeError(f"Expected a JSON object in {path}")

    return data


def save_db(database: Database, path: Path) -> None:
    """Save  the database as JSON."""
    with open(path, mode="w") as file:
        json.dump(database, file, indent=2, ensure_ascii=False)
