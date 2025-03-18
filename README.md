# Pytask

![Python Package](https://github.com/yourusername/pytask/actions/workflows/python-package.yml/badge.svg)

A simple, lightweight Python package for managing tasks with support for prioritization, reminders, and rewards. Pytask provides a clean API for organizing your tasks, reminding you of upcoming deadlines, and rewarding your accomplishments.

## Features

- **Task Management**: Add, update, and remove tasks with customizable time and value parameters
- **Task Listing**: List tasks with various sorting options (upcoming, by priority, etc.)
- **Task Completion**: Mark tasks as completed and track your progress
- **Reminder System**: Get email reminders for upcoming tasks to stay on track
- **Reward System**: Receive motivational rewards when completing tasks of sufficient value

## Installation

### From PyPI (Recommended)

```bash
pip install pytask-new
```

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/pytask.git
cd pytask

# Install in development mode
pip install -e .
```

## Usage

### Core Task Management

```python
import datetime
from pytask_new.tasks import add_task, update_task, remove_task

# Add a task with a string time (ISO format)
add_task("2023-06-15T09:00:00", "Morning meeting", 5)

# Add a task with a datetime object
tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
add_task(tomorrow, "Lunch with team", 3)

# Update a task's value
update_task("2023-06-15T09:00:00", "Morning meeting", 10)

# Remove a task
remove_task("2023-06-15T09:00:00", "Morning meeting")
```

### Task Listing (To be implemented by Lan)

```python
from pytask_new.list import list_tasks, mark_completed

# List all tasks sorted by time
tasks = list_tasks(sort_by="time")

# List tasks before a specific date
upcoming_tasks = list_tasks(before="2023-07-01T00:00:00")

# Mark a task as completed
mark_completed("2023-06-15T09:00:00", "Morning meeting")
```

### Reminder System (To be implemented by Yuquan)

```python
from pytask_new.reminder import reminder_mail

# Configure email reminders
reminder_mail("your_email@example.com", days_ahead=1)
```

### Reward System (To be implemented by Yilei)

```python
from pytask_new.reward import reward

# Check rewards when reaching a value threshold
motivational_message = reward(20)
print(motivational_message)  # Prints a joke or congratulatory message
```

## For Contributors

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/pytask.git
cd pytask

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package in development mode
pip install -e .

# Install development dependencies
pip install pytest build twine

# Run tests
pytest
```

### Development Workflow

1. Create a feature branch for your work
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Implement your changes and add tests

3. Make sure tests pass
   ```bash
   python -m pytest
   ```

4. Create a pull request to the main branch

## Project Structure

```
pytask/                            # Root project directory
├── pytask_new/                    # Main package source code
│   ├── __init__.py                # Package initialization and exports
│   └── tasks.py                   # Core task management (Xingjian)
│
├── tests/                         # Test directory
│   └── pytask/                    # Tests for pytask modules
│       ├── __init__.py            # Test package initialization
│       └── test_tasks.py          # Tests for tasks module
│
├── examples/                      # Example scripts
│   └── example_usage.py           # Example of using the package
│
├── .github/                       # GitHub specific files
│   └── workflows/                 # GitHub Actions workflows
│       └── python-package.yml     # CI workflow for testing and building
│
├── .venv/                         # Virtual environment (not in version control)
├── pytask_new.egg-info/           # Package metadata (not in version control)
├── .pytest_cache/                 # Pytest cache (not in version control)
│
├── pyproject.toml                 # Project configuration (PEP 517/518)
├── Pipfile                        # Pipenv dependency management
├── README.md                      # This documentation file
├── LICENSE                        # License information
└── .gitignore                     # Git ignore patterns
```

### Key Modules

- **tasks.py**: Core module for adding, updating, and removing tasks. Tasks are stored as JSON with timestamps, descriptions, values, and completion status.
  
- **list.py**: Module for listing tasks with various sorting and filtering options, and for marking tasks as completed.
  
- **reminder.py**: Module for setting up and sending email reminders for upcoming tasks.
  
- **reward.py**: Module for providing motivational rewards when users complete tasks of sufficient value.

## Data Storage

By default, tasks are stored in a JSON file at `~/.pytask_data.json`. Each task has the following structure:

```json
{
  "time": "2023-06-15T09:00:00",
  "event": "Morning meeting",
  "value": 5,
  "completed": false
}
```

You can specify a custom file path when using the API functions.

## Contributors

- [Xingjian](https://github.com/xingjian) - Core Task Management
- [Lan](https://github.com/lan) - Task Listing and Completion
- [Yuquan](https://github.com/yuquan) - Email Reminders
- [Yilei](https://github.com/ShadderD) - Reward System

## License

This project is licensed under the MIT License - see the LICENSE file for details.
