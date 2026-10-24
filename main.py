from argparse import ArgumentParser, Namespace
from pathlib import Path

import manager
from storage import Database, load_db, save_db


def handle_add(args: Namespace, database: Database) -> None:
    task_id = manager.add_task(database, args.description)
    print(f"Task added successfully (ID: {task_id})")


def handle_list(args: Namespace, database: Database) -> None:
    status = getattr(args, "status", None)
    tasks = manager.list_tasks(database, status)

    if not tasks:
        print("No tasks found.")
        return

    for task_id, task in tasks:
        print(
            f"[{task_id}] {task['description']} "
            f"| status: {task['status']} "
            f"| created: {task['createdAt']} "
            f"| updated: {task['updatedAt']}"
        )


def handle_update(args: Namespace, database: Database) -> None:
    manager.update_task(
        database,
        task_id=args.id,
        description=args.desc,
        status=args.status,
    )
    print(f"Task {args.id} updated successfully.")


def handle_mark_in_progress(args: Namespace, database: Database) -> None:
    manager.set_task_status(database, args.id, "in-progress")
    print(f"Task {args.id} marked as in-progress.")


def handle_mark_done(args: Namespace, database: Database) -> None:
    manager.set_task_status(database, args.id, "done")
    print(f"Task {args.id} marked as done.")


def handle_delete(args: Namespace, database: Database) -> None:
    manager.delete_task(database, args.id)
    print(f"Task {args.id} deleted successfully.")


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="task-cli",
        description="A simple command-line task tracker",
    )
    parser.add_argument(
        "--db",
        default="~/taskly.json",
        help="Path to the database file (default: ~/taskly.json)",
    )

    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        required=True,
    )

    add_parser = subparsers.add_parser("add", help="Add a task")
    add_parser.add_argument("description", help="Description of the task")
    add_parser.set_defaults(handler=handle_add, mutates=True)

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "-s",
        "--status",
        choices=["todo", "in-progress", "done"],
        help="Filter tasks by status",
    )
    list_parser.set_defaults(handler=handle_list, mutates=False)

    update_parser = subparsers.add_parser(
        "update",
        help="Update a task's description or status",
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
    update_parser.add_argument(
        "-d",
        "--desc",
        help="New task description",
    )
    update_parser.set_defaults(handler=handle_update, mutates=True)

    mark_in_progress = subparsers.add_parser(
        "mark-in-progress",
        help="Mark a task as in progress",
    )
    mark_in_progress.add_argument(
        "-i",
        "--id",
        required=True,
        type=int,
        help="ID of the task to mark in progress",
    )
    mark_in_progress.set_defaults(
        handler=handle_mark_in_progress,
        mutates=True,
    )

    mark_done = subparsers.add_parser("mark-done", help="Mark a task as done")
    mark_done.add_argument(
        "-i",
        "--id",
        required=True,
        type=int,
        help="ID of the task to mark as done",
    )
    mark_done.set_defaults(handler=handle_mark_done, mutates=True)

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument(
        "-i",
        "--id",
        required=True,
        type=int,
        help="ID of the task to delete",
    )
    delete_parser.set_defaults(handler=handle_delete, mutates=True)

    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    path = Path(args.db).expanduser()

    try:
        database = load_db(path)
        args.handler(args, database)

        # Persist once, and only after a successful mutating command.
        # We save db only if a command mutstes it eg : add, update etc
        if args.mutates:
            save_db(database, path)
            handle_list(args, database)
    except (ValueError, TypeError, KeyError, OSError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
