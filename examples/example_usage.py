#!/usr/bin/env python3
"""
Example usage of the Pytask package.

This script demonstrates the core functionality of the Pytask package,
including adding, updating, and removing tasks.
"""

import datetime
import json
import tempfile
import os
from superTask.tasks import add_task, update_task, remove_task, reminder

def main():
    """
    Demonstrate the core functionality of the Pytask package.
    """
    print("superTask Example - Core Task Management\n")
    
    # Create a temporary file that will be automatically deleted
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_tasks_file = temp_file.name
    
    try:
        # Add tasks
        print("Adding tasks...")
        
        # Add a task with string time
        task1 = add_task("2023-06-15T09:00:00", "Morning meeting", 5, temp_tasks_file)
        print(f"Added task: {task1['event']} at {task1['time']} with value {task1['value']}")
        
        # Add a task with datetime object
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        tomorrow_noon = tomorrow.replace(hour=12, minute=0, second=0, microsecond=0)
        task2 = add_task(tomorrow_noon, "Lunch with team", 3, temp_tasks_file)
        print(f"Added task: {task2['event']} at {task2['time']} with value {task2['value']}")
        
        # Add another task
        next_week = datetime.datetime.now() + datetime.timedelta(days=7)
        task3 = add_task(next_week, "Weekly review", 8, temp_tasks_file)
        print(f"Added task: {task3['event']} at {task3['time']} with value {task3['value']}")
        
        print("\n------------------------------\n")
        
        # Update a task
        print("Updating a task...")
        updated_task = update_task(tomorrow_noon, "Lunch with team", 5, temp_tasks_file)
        print(f"Updated task: {updated_task['event']} - value changed to {updated_task['value']}")
        
        print("\n------------------------------\n")
        
        # Remove a task
        print("Removing a task...")
        removed_task = remove_task("2023-06-15T09:00:00", "Morning meeting", temp_tasks_file)
        print(f"Removed task: {removed_task['event']} at {removed_task['time']}")
        
        print("\nExample completed successfully!")
        
        # Show the final state of tasks
        print("\nFinal tasks state:")
        with open(temp_tasks_file, 'r') as f:
            tasks = json.load(f)
            for task in tasks:
                print(f"- {task['event']} at {task['time']} (value: {task['value']}, completed: {task['completed']})")

        # Send a reminder email
        print("\nSending reminder email...")
        target_email = input("Enter your email address: ")
        reminder(to_email=target_email, tasks_file=temp_tasks_file)
        print("Reminder email sent successfully!")
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_tasks_file):
            os.remove(temp_tasks_file)


if __name__ == "__main__":
    main() 