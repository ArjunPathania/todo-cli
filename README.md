# Taskly — Task Tracker CLI

A simple command-line task tracker built with Python using only the standard library. Taskly lets you create, update, delete, and organize tasks directly from your terminal, with persistent JSON storage.

## Features

- Add tasks with automatically generated IDs
- Update task descriptions and statuses
- Delete tasks
- Mark tasks as `todo`, `in-progress`, or `done`
- List all tasks or filter by status
- Persist tasks in a local JSON database
- Validate task data and command-line arguments
- Configure the database file path
- Automatically display the task list after mutations

## Requirements

- Python 3.10 or newer
- Git (for development)

No third-party runtime dependencies are required.

## Setup

Clone the repository and enter the project directory:

```bash
git clone https://github.com/ArjunPathania/todo-cli
cd todo-cli
```

<https://github.com/ArjunPathania/todo-cli>
Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Taskly in editable mode:

```bash
python -m pip install -e .
```

After installation, the `taskly` command should be available in your activated environment.

## Usage

### Add a task

```bash
taskly add "Learn Python file handling"
```

Taskly assigns an ID, sets the initial status to `todo`, records timestamps, and saves the task.

### List tasks

List all tasks:

```bash
taskly list
```

Filter tasks by status:

```bash
taskly list --status todo
taskly list --status in-progress
taskly list --status done
```

### Update a task

Update its description:

```bash
taskly update --id 1 --desc "Learn Python JSON handling"
```

Update its status:

```bash
taskly update --id 1 --status in-progress
```

Update both fields:

```bash
taskly update --id 1 --desc "Finish the CLI project" --status done
```

At least one of `--desc` or `--status` must be supplied.

### Change task status

Mark a task as in progress:

```bash
taskly mark-in-progress --id 1
```

Mark a task as done:

```bash
taskly mark-done --id 1
```

### Delete a task

```bash
taskly delete --id 1
```

### Choose a database file

By default, Taskly stores data in `~/taskly.json`.

Specify a different database file with `--db`:

```bash
taskly --db ./tasks.json add "Write unit tests"
taskly --db ./tasks.json list
```

The `--db` option goes before the subcommand.

## Storage

Tasks are stored in JSON format. Each task contains:

- `description`: Task description
- `status`: Current status (`todo`, `in-progress`, or `done`)
- `createdAt`: Creation timestamp
- `updatedAt`: Last modification timestamp

Task IDs are represented by the JSON object's keys.

Example:

```json
{
  "1": {
    "description": "Learn Python file handling",
    "status": "todo",
    "createdAt": "2026-10-24T10:00:00",
    "updatedAt": "2026-10-24T10:00:00"
  }
}
```

A missing database file is initialized as an empty database when loaded. Invalid JSON or invalid task data is reported as an error.

## Project Structure

```text
task-tracker/
├── main.py          # CLI argument parsing and command handlers
├── manager.py       # Task management operations
├── storage.py       # JSON loading, validation, and saving
├── tests/           # Automated tests
├── pyproject.toml   # Project metadata and CLI entry point
├── README.md        # Project documentation
└── .gitignore
```

## Development

Run the CLI directly without installing it:

```bash
python main.py --help
```

Run the automated tests:

```bash
python -m unittest discover -s tests -v
```

Install the project in editable mode after making changes to its source files:

```bash
python -m pip install -e .
```

## Project Status

In development. Core task operations and JSON persistence are implemented; automated test coverage and further improvements are ongoing.
