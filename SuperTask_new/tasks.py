"""
Tasks module for the Pytask package.

This module provides core functionality for managing tasks, including
adding, updating, and removing tasks.
"""

import json
import os
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# Define the default location for the tasks data file
DEFAULT_TASKS_FILE = os.path.expanduser("~/.pytask_data.json")


def _get_tasks(tasks_file: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Internal function to get tasks from the data file.
    
    Args:
        tasks_file: Optional path to the tasks file. Defaults to DEFAULT_TASKS_FILE.
        
    Returns:
        List of task dictionaries.
    """
    tasks_file = tasks_file or DEFAULT_TASKS_FILE
    
    # If the file doesn't exist, return an empty list
    if not os.path.exists(tasks_file):
        return []
    
    try:
        with open(tasks_file, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # If there's an error reading the file, return an empty list
        return []


def _save_tasks(tasks: List[Dict[str, Any]], tasks_file: Optional[str] = None) -> None:
    """
    Internal function to save tasks to the data file.
    
    Args:
        tasks: List of task dictionaries to save.
        tasks_file: Optional path to the tasks file. Defaults to DEFAULT_TASKS_FILE.
    """
    tasks_file = tasks_file or DEFAULT_TASKS_FILE
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(tasks_file)), exist_ok=True)
    
    with open(tasks_file, 'w') as f:
        json.dump(tasks, f, indent=2)


def _validate_task(time: Union[str, datetime.datetime], event: str, value: int) -> Dict[str, Any]:
    """
    Validate and format task data.
    
    Args:
        time: Task time as string (ISO format) or datetime object.
        event: Task description/name.
        value: Task value (integer).
        
    Returns:
        Dictionary with validated task data.
        
    Raises:
        ValueError: If any of the arguments are invalid.
    """
    # Validate time
    if isinstance(time, str):
        try:
            parsed_time = datetime.datetime.fromisoformat(time)
            time_str = time
        except ValueError:
            raise ValueError(f"Invalid time format: {time}. Use ISO format (YYYY-MM-DDThh:mm:ss).")
    elif isinstance(time, datetime.datetime):
        time_str = time.isoformat()
    else:
        raise ValueError(f"Time must be a string in ISO format or a datetime object, got {type(time)}")
    
    # Validate event
    if not isinstance(event, str) or not event.strip():
        raise ValueError("Event must be a non-empty string")
    
    # Validate value
    if not isinstance(value, int):
        raise ValueError(f"Value must be an integer, got {type(value)}")
    
    return {
        "time": time_str,
        "event": event.strip(),
        "value": value,
        "completed": False
    }


def add_task(time: Union[str, datetime.datetime], event: str, value: int, 
             tasks_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Add a new task.
    
    Args:
        time: Task time as string (ISO format) or datetime object.
        event: Task description/name.
        value: Task value (integer).
        tasks_file: Optional path to the tasks file. Defaults to DEFAULT_TASKS_FILE.
        
    Returns:
        The newly added task as a dictionary.
        
    Raises:
        ValueError: If a task with the same time and event already exists or if 
                    any of the arguments are invalid.
    """
    # Get existing tasks
    tasks = _get_tasks(tasks_file)
    
    # Validate task data
    new_task = _validate_task(time, event, value)
    
    # Check if a task with the same time and event already exists
    for task in tasks:
        if task["time"] == new_task["time"] and task["event"] == new_task["event"]:
            raise ValueError(f"Task with time '{new_task['time']}' and event '{new_task['event']}' already exists")
    
    # Add the new task
    tasks.append(new_task)
    
    # Save tasks
    _save_tasks(tasks, tasks_file)
    
    return new_task


def update_task(time: Union[str, datetime.datetime], event: str, value: int, 
                tasks_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Update an existing task.
    
    Args:
        time: Task time as string (ISO format) or datetime object.
        event: Task description/name to identify the task.
        value: New task value.
        tasks_file: Optional path to the tasks file. Defaults to DEFAULT_TASKS_FILE.
        
    Returns:
        The updated task as a dictionary.
        
    Raises:
        ValueError: If the task doesn't exist or if any of the arguments are invalid.
    """
    # Validate task data
    validated_task = _validate_task(time, event, value)
    time_str = validated_task["time"]
    event_str = validated_task["event"]
    
    # Get existing tasks
    tasks = _get_tasks(tasks_file)
    
    # Find and update the task
    for i, task in enumerate(tasks):
        if task["time"] == time_str and task["event"] == event_str:
            # Update the value (keeping completion status intact)
            tasks[i]["value"] = value
            
            # Save tasks
            _save_tasks(tasks, tasks_file)
            
            return tasks[i]
    
    # If we get here, the task wasn't found
    raise ValueError(f"No task found with time '{time_str}' and event '{event_str}'")


def remove_task(time: Union[str, datetime.datetime], event: str, 
                tasks_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Remove an existing task.
    
    Args:
        time: Task time as string (ISO format) or datetime object.
        event: Task description/name to identify the task.
        tasks_file: Optional path to the tasks file. Defaults to DEFAULT_TASKS_FILE.
        
    Returns:
        The removed task as a dictionary.
        
    Raises:
        ValueError: If the task doesn't exist or if any of the arguments are invalid.
    """
    # Convert time to string if it's a datetime object
    if isinstance(time, datetime.datetime):
        time_str = time.isoformat()
    else:
        time_str = time
    
    # Get existing tasks
    tasks = _get_tasks(tasks_file)
    
    # Find and remove the task
    for i, task in enumerate(tasks):
        if task["time"] == time_str and task["event"] == event:
            # Remove the task
            removed_task = tasks.pop(i)
            
            # Save tasks
            _save_tasks(tasks, tasks_file)
            
            return removed_task
    
    # If we get here, the task wasn't found
    raise ValueError(f"No task found with time '{time_str}' and event '{event}'") 