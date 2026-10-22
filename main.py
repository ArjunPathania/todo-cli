from argparse import ArgumentParser
from pathlib import Path

from storage import load_db


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="task-cli",
        description="A simple command-line task tracker",
    )

    parser.add_argument(
        "--db",
        help="Path to the database file (default: ~/taskly.json)",
        default="~/taskly.json",
    )

    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        required=True,
    )

    add_parser = subparsers.add_parser(
        "add",
        help="Add a task",
    )
    add_parser.add_argument(
        "description",
        help="Description of the task",
    )

    list_parser = subparsers.add_parser(
        "list",
        help="List tasks",
    )
    list_parser.add_argument(
        "status",
        nargs="?",
        choices=["todo", "in-progress", "done"],
        help="Filter tasks by status",
    )

    update_parser = subparsers.add_parser(
        "update",
        help="Update a task's description",
    )
    update_parser.add_argument(
        "-i",
        "--id",
        required=True,
        type=int,
        help="ID of the task to update",
    )
    update_parser.add_argument(
        "-s",
        "--status",
        choices=["todo", "in-progress", "done"],
        help="New task status",
    )

    mark_in_progress = subparsers.add_parser(
        "mark-inprogress", help="Change a task's status to in progress"
    )
    mark_in_progress.add_argument(
        "--id", required=True, type=int, help="ID of the task to mark in progress"
    )

    mark_done = subparsers.add_parser(
        "mark-done", help="Change a task's status to mark-done"
    )
    mark_done.add_argument("--id", required=True, help="ID of the task to mark as done")

    delete = subparsers.add_parser("delete", help="Delete a task")
    delete.add_argument(
        "--id", requiired=True, required=True, help="ID of the task to delete"
    )

    return parser


def main() -> None:
    path = Path("tasks.json")

    parser = create_parser()
    args = parser.parse_args()

    print(args)

    try:
        database = load_db(path)
        print(database)

    except ValueError as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
