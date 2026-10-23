from argparse import ArgumentParser, Namespace
from pathlib import Path

from storage import load_db, save_db


def handle_add(args: Namespace) -> None:
    print(f"Adding task: {args.description}")


def handle_list(args: Namespace) -> None:
    print(f"Listing tasks with status: {args.status or 'all'}")


def handle_update(args: Namespace) -> None:
    if args.status is None and args.desc is None:
        raise ValueError("Provide at least one of --status or --desc.")

    print(f"Updating task {args.id}: status={args.status},description={args.desc}")


def handle_mark_in_progress(args: Namespace) -> None:
    print(f"Marking task {args.id} as in-progress")


def handle_mark_done(args: Namespace) -> None:
    print(f"Marking task {args.id} as done")


def handle_delete(args: Namespace) -> None:
    print(f"Deleting task {args.id}")


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
    add_parser.set_defaults(handler=handle_add)

    list_parser = subparsers.add_parser(
        "list",
        help="List tasks",
    )

    list_parser.add_argument(
        "-s",
        "--status",
        choices=["todo", "in-progress", "done"],
        help="Filter tasks by status",
    )
    list_parser.set_defaults(handler=handle_list)

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
    update_parser.set_defaults(handler=handle_update)

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
    mark_in_progress.set_defaults(handler=handle_mark_in_progress)

    mark_done = subparsers.add_parser(
        "mark-done",
        help="Mark a task as done",
    )
    mark_done.add_argument(
        "-i",
        "--id",
        required=True,
        type=int,
        help="ID of the task to mark as done",
    )
    mark_done.set_defaults(handler=handle_mark_done)

    delete = subparsers.add_parser(
        "delete",
        help="Delete a task",
    )
    delete.add_argument(
        "-i",
        "--id",
        required=True,
        type=int,
        help="ID of the task to delete",
    )
    delete.set_defaults(handler=handle_delete)

    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    path = Path(args.db).expanduser()

    try:
        database = load_db(path)
        print(database)
        args.handler(args)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))

    save_db(database=database, path=path)


if __name__ == "__main__":
    main()
