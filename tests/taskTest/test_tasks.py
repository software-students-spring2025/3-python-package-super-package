"""
Tests for the tasks module in the Pytask package.
"""

import os
import json
import pytest
from unittest.mock import patch, MagicMock
import datetime
from superTask.tasks import add_task, update_task, remove_task, reminder


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

@pytest.fixture
def cleanup_test_file():
    """Fixture to clean up the test file before and after tests."""
    if os.path.exists(TEST_TASKS_FILE):
        os.remove(TEST_TASKS_FILE)

    yield

    if os.path.exists(TEST_TASKS_FILE):
        os.remove(TEST_TASKS_FILE)



@pytest.fixture
def mock_smtp():
    """
    Fixture to mock smtplib.SMTP_SSL so we don't actually send emails during tests.
    Yields the mock instance, so we can assert calls, mail content, etc.
    """
    with patch("superTask.tasks.smtplib.SMTP_SSL", autospec=True) as mock_server_class:
        # mock_server_class is the mocked class
        # mock_server_instance is what reminder(...) will instantiate
        mock_server_instance = mock_server_class.return_value.__enter__.return_value
        yield mock_server_instance


class TestReminder:
    """Tests for the reminder function."""

    def test_reminder_no_upcoming_tasks(self, mock_smtp, cleanup_test_file):
        """
        If there are no tasks within deadline, the function should return early
        and not send any email.
        """
        # No tasks added => no upcoming tasks
        reminder(tasks_file=TEST_TASKS_FILE, to_email="test@example.com")

        # The reminder function returns early; mock_smtp.send_message should NOT be called
        mock_smtp.send_message.assert_not_called()

    def test_reminder_with_upcoming_tasks(self, mock_smtp, cleanup_test_file):
        """
        If we have tasks within the deadline, an email should be sent.
        We'll verify that send_message was called and the email content includes the tasks.
        """
        # Add a task 1 hour in the future
        future_time = (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat()
        add_task(future_time, "Task A", 10, TEST_TASKS_FILE)

        # Call reminder with deadline=2 => 2 hours
        reminder(
            tasks_file=TEST_TASKS_FILE,
            to_email="test@example.com",
            deadline=2
        )

        # Expect one call to send_message
        mock_smtp.send_message.assert_called_once()
        sent_message = mock_smtp.send_message.call_args[0][0]  # the first positional arg is the EmailMessage

        # Check the email subject, 'From', 'To'
        assert sent_message["Subject"] == "Upcoming Task Reminder"
        assert sent_message["From"] == "13601583609@163.com"  # default from_email
        assert sent_message["To"] == "test@example.com"

        # Check if HTML part has "Task A" in it
        payloads = sent_message.get_payload()  # returns list of message parts
        # The second part should be the HTML (subtype="html") if set_content was the plain text
        # and add_alternative was the HTML. Let's find it:
        html_part = None
        for part in payloads:
            if part.get_content_type() == "text/html":
                html_part = part
                break

        assert html_part is not None, "No HTML alternative found in the email."
        html_content = html_part.get_payload(decode=True).decode("utf-8")

        assert "Task A" in html_content, "HTML content should include 'Task A'"

    def test_reminder_deadline_too_short(self, mock_smtp, cleanup_test_file):
        """
        If tasks are in the future but beyond the set deadline, no email should be sent.
        """
        # Add a task 5 hours in the future
        future_time = (datetime.datetime.now() + datetime.timedelta(hours=5)).isoformat()
        add_task(future_time, "Task B", 10, TEST_TASKS_FILE)

        # deadline=2, so 5-hour-later tasks are not within upcoming
        reminder(tasks_file=TEST_TASKS_FILE, to_email="test@example.com", deadline=2)

        # Should not send email
        mock_smtp.send_message.assert_not_called()

    def test_reminder_rank_value(self, mock_smtp, cleanup_test_file):
        """
        Test that rank='value' sorts tasks by 'value' in ascending order in the HTML table.
        We'll check the order of tasks in the generated HTML.
        """
        now = datetime.datetime.now()
        # Add 2 tasks within 1 hour => both will be reminded
        add_task((now + datetime.timedelta(minutes=30)).isoformat(), "Task C", 20, TEST_TASKS_FILE)
        add_task((now + datetime.timedelta(minutes=30)).isoformat(), "Task D", 5,  TEST_TASKS_FILE)

        # rank="value" => we expect 'Task D' (value=5) to appear before 'Task C' (value=20)
        reminder(tasks_file=TEST_TASKS_FILE, to_email="test@example.com", rank="value")

        mock_smtp.send_message.assert_called_once()
        sent_message = mock_smtp.send_message.call_args[0][0]
        payloads = sent_message.get_payload()
        html_part = None
        for part in payloads:
            if part.get_content_type() == "text/html":
                html_part = part
                break

        assert html_part is not None, "No HTML part found in the email"
        html_content = html_part.get_payload(decode=True).decode("utf-8")

        # Check the order: we want 'Task D' row to appear before 'Task C'
        index_d = html_content.find("Task D")
        index_c = html_content.find("Task C")

        assert index_d < index_c, "Tasks should be sorted by value => Task D (value=5) comes before Task C (value=20)."