# dev-time

Keep track of the time you spend on your projects.

## Installation

Using `pip`:

```sh
$ python -m pip install dev-time
```

During development, you can install the package in editable mode with the following commands:

```sh
$ python -m pip install -e .
```

## Usage

```sh
$ dev-time --help

 Usage: dev-time [OPTIONS] COMMAND [ARGS]...

╭─ Commands ────────────────────────────────────────╮
│ create-project   Create a new project.                                       │
│ delete-project   Delete a project.                                           │
│ log-time         Log time spent on a project.                                │
│ summary          View a summary of all projects and their total logged time. │
│ snapshot         Export the project data to a CSV file.                      │
╰───────────────────────────────────────────────╯
$ dev-time create-project SWARM
OK! Project 'SWARM' created successfully.
$ dev-time create-project "Data Spaces"
OK! Project 'Data Spaces' created successfully.
$ dev-time log-time "Data Spaces" 1h
OK! Logged 60 minutes for 'Data Spaces'.
$ dev-time summary
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Project name          ┃ Time logged          ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ SWARM                 │ 0m                   │
│ Data Spaces           │ 1h 0m                │
└──────────────┴─────────────┘
$ dev-time delete-project "Data Spaces"
OK! Project 'Data Spaces' deleted successfully. 💥
$ dev-time delete-project "Data Spaces"
Error: Project 'Data Spaces' not found.
```
