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
from superTask.tasks import add_task, update_task, remove_task, complete, list_tasks, reminder, reward

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

        # Mark a Task as completed
        print("Marking a task as completed...")
        completed_task = complete("Lunch with team", temp_tasks_file)
        print(f"Task completed: {completed_task['event']} - Status: {completed_task['completed']}")

        print("\n------------------------------\n")

        # List Tasks by Deadline**
        print("Listing tasks sorted by deadline (default)...")
        sorted_by_time = list_tasks(order_by="time", tasks_file=temp_tasks_file)
        for task in sorted_by_time:
            print(f"- {task['event']} at {task['time']} (value: {task['value']}, completed: {task.get('completed', False)})")

        print("\n------------------------------\n")

        # List Tasks by Value**
        print("Listing tasks sorted by value...")
        sorted_by_value = list_tasks(order_by="value", tasks_file=temp_tasks_file)
        for task in sorted_by_value:
            print(f"- {task['event']} at {task['time']} (value: {task['value']}, completed: {task.get('completed', False)})")


        print("\n------------------------------\n")
        
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

        # Demonstrate the reward function
        print("\nDemonstrating the reward function...")

        # For demonstration, mark tasks as completed
        with open(temp_tasks_file, 'r') as f:
            tasks = json.load(f)
            for task in tasks:
                # Mark at least one task as completed for the demo
                if task['event'] == "Lunch with team":
                    task['completed'] = True
            
            # Save the modified tasks back to the file
            with open(temp_tasks_file, 'w') as f_write:
                json.dump(tasks, f_write, indent=2)

        # Get user inputs
        while True:
            try:
                reward_threshold = int(input("Enter the reward threshold value: "))
                break  # Exit the loop if input was successfully converted to int
            except ValueError:
                print("Invalid input. Please enter a valid integer value.")

        # Call the reward function with user inputs
        reward_result = reward(
            threshold_value=reward_threshold,
            tasks_file=temp_tasks_file,
            to_email=target_email,
            reward_message="You've made great progress! Keep going!",
            include_joke=True
        )

        if reward_result:
            print(f"Reward email sent - you've reached the {reward_threshold} point threshold!")
        else:
            print(f"No reward sent - you haven't reached the {reward_threshold} point threshold yet.")
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_tasks_file):
            os.remove(temp_tasks_file)


if __name__ == "__main__":
    main() 