"""
Tests for the tasks module in the Pytask package.
"""

import os
import json
import pytest
import datetime
from SuperTask_new.tasks import add_task, update_task, remove_task

# Use a test file instead of the default one
TEST_TASKS_FILE = "test_tasks_data.json"


@pytest.fixture
def cleanup_test_file():
    """Fixture to clean up the test file before and after tests."""
    # Remove the test file if it exists
    if os.path.exists(TEST_TASKS_FILE):
        os.remove(TEST_TASKS_FILE)
    
    yield
    
    # Clean up after the test
    if os.path.exists(TEST_TASKS_FILE):
        os.remove(TEST_TASKS_FILE)


class TestAddTask:
    """Tests for the add_task function."""
    
    def test_add_task_with_string_time(self, cleanup_test_file):
        """Test adding a task with a string time."""
        task = add_task("2023-01-01T10:00:00", "Test Event", 5, TEST_TASKS_FILE)
        
        assert task["time"] == "2023-01-01T10:00:00"
        assert task["event"] == "Test Event"
        assert task["value"] == 5
        assert task["completed"] is False
        
        # Verify the task was saved to the file
        with open(TEST_TASKS_FILE, 'r') as f:
            saved_tasks = json.load(f)
            assert len(saved_tasks) == 1
            assert saved_tasks[0] == task
    
    def test_add_task_with_datetime(self, cleanup_test_file):
        """Test adding a task with a datetime object."""
        task_time = datetime.datetime(2023, 1, 1, 10, 0, 0)
        task = add_task(task_time, "Test Event", 5, TEST_TASKS_FILE)
        
        assert task["time"] == task_time.isoformat()
        assert task["event"] == "Test Event"
        assert task["value"] == 5
        
        # Verify the task was saved to the file
        with open(TEST_TASKS_FILE, 'r') as f:
            saved_tasks = json.load(f)
            assert len(saved_tasks) == 1
            assert saved_tasks[0] == task
    
    def test_add_duplicate_task(self, cleanup_test_file):
        """Test adding a duplicate task."""
        # Add a task
        add_task("2023-01-01T10:00:00", "Test Event", 5, TEST_TASKS_FILE)
        
        # Try to add a duplicate task
        with pytest.raises(ValueError) as excinfo:
            add_task("2023-01-01T10:00:00", "Test Event", 10, TEST_TASKS_FILE)
        
        assert "already exists" in str(excinfo.value)
        
        # Verify only one task was saved
        with open(TEST_TASKS_FILE, 'r') as f:
            saved_tasks = json.load(f)
            assert len(saved_tasks) == 1
            assert saved_tasks[0]["value"] == 5  # Original value is preserved
    
    def test_add_task_invalid_time(self, cleanup_test_file):
        """Test adding a task with an invalid time format."""
        with pytest.raises(ValueError) as excinfo:
            add_task("not-a-valid-time", "Test Event", 5, TEST_TASKS_FILE)
        
        assert "Invalid time format" in str(excinfo.value)
        
        # Verify no task was saved
        assert not os.path.exists(TEST_TASKS_FILE)


class TestUpdateTask:
    """Tests for the update_task function."""
    
    def test_update_task(self, cleanup_test_file):
        """Test updating a task."""
        # Add a task
        add_task("2023-01-01T10:00:00", "Test Event", 5, TEST_TASKS_FILE)
        
        # Update the task
        updated_task = update_task("2023-01-01T10:00:00", "Test Event", 10, TEST_TASKS_FILE)
        
        assert updated_task["time"] == "2023-01-01T10:00:00"
        assert updated_task["event"] == "Test Event"
        assert updated_task["value"] == 10
        
        # Verify the task was updated in the file
        with open(TEST_TASKS_FILE, 'r') as f:
            saved_tasks = json.load(f)
            assert len(saved_tasks) == 1
            assert saved_tasks[0]["value"] == 10
    
    def test_update_nonexistent_task(self, cleanup_test_file):
        """Test updating a task that doesn't exist."""
        with pytest.raises(ValueError) as excinfo:
            update_task("2023-01-01T10:00:00", "Nonexistent Event", 10, TEST_TASKS_FILE)
        
        assert "No task found" in str(excinfo.value)
    
    def test_update_task_preserves_completion(self, cleanup_test_file):
        """Test updating a task preserves completion status."""
        # Add a task
        add_task("2023-01-01T10:00:00", "Test Event", 5, TEST_TASKS_FILE)
        
        # Manually mark the task as completed in the file
        with open(TEST_TASKS_FILE, 'r') as f:
            tasks = json.load(f)
        tasks[0]["completed"] = True
        with open(TEST_TASKS_FILE, 'w') as f:
            json.dump(tasks, f)
        
        # Update the task
        updated_task = update_task("2023-01-01T10:00:00", "Test Event", 10, TEST_TASKS_FILE)
        
        assert updated_task["completed"] is True
        assert updated_task["value"] == 10


class TestRemoveTask:
    """Tests for the remove_task function."""
    
    def test_remove_task(self, cleanup_test_file):
        """Test removing a task."""
        # Add tasks
        add_task("2023-01-01T10:00:00", "Test Event 1", 5, TEST_TASKS_FILE)
        add_task("2023-01-01T11:00:00", "Test Event 2", 10, TEST_TASKS_FILE)
        
        # Remove one task
        removed_task = remove_task("2023-01-01T10:00:00", "Test Event 1", TEST_TASKS_FILE)
        
        assert removed_task["time"] == "2023-01-01T10:00:00"
        assert removed_task["event"] == "Test Event 1"
        
        # Verify only one task remains in the file
        with open(TEST_TASKS_FILE, 'r') as f:
            saved_tasks = json.load(f)
            assert len(saved_tasks) == 1
            assert saved_tasks[0]["event"] == "Test Event 2"
    
    def test_remove_nonexistent_task(self, cleanup_test_file):
        """Test removing a task that doesn't exist."""
        with pytest.raises(ValueError) as excinfo:
            remove_task("2023-01-01T10:00:00", "Nonexistent Event", TEST_TASKS_FILE)
        
        assert "No task found" in str(excinfo.value)
    
    def test_remove_task_with_datetime(self, cleanup_test_file):
        """Test removing a task using a datetime object for time."""
        # Add a task
        add_task("2023-01-01T10:00:00", "Test Event", 5, TEST_TASKS_FILE)
        
        # Remove the task using a datetime object
        task_time = datetime.datetime(2023, 1, 1, 10, 0, 0)
        removed_task = remove_task(task_time, "Test Event", TEST_TASKS_FILE)
        
        assert removed_task["time"] == "2023-01-01T10:00:00"
        
        # Verify no tasks remain in the file
        with open(TEST_TASKS_FILE, 'r') as f:
            saved_tasks = json.load(f)
            assert len(saved_tasks) == 0 