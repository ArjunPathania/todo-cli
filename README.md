# Task Tracker CLI

A command-line task tracker written in Python using only the standard library.

## Features

- Add, update, and delete tasks
- Track task status: `todo`, `in-progress`, and `done`
- List all tasks or filter them by status
- Store tasks persistently in a local JSON file
- Validate command arguments and handle errors

## Requirements

- Python 3
- Git (for development)

## Setup

```bash
git clone <your-repository-url>
cd task-tracker
python3 -m venv .venv
source .venv/bin/activate
```

No third-party Python packages are required.

## Usage

Examples will be added as commands are implemented.

## Storage

Tasks are stored in `tasks.json` in the working directory.

## Development

Run the automated tests with:

```bash
python -m unittest discover -s tests -v
```

## Project Status

In development.
