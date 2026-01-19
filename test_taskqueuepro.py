#!/usr/bin/env python3
"""
Test suite for TaskQueuePro v1.0

Tests only the methods that actually exist in the implementation.

Author: Atlas (Team Brain)
Date: January 18, 2026
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from taskqueuepro import TaskQueuePro, TaskStatus, TaskPriority


class TestTaskQueuePro(unittest.TestCase):
    """Test suite for TaskQueuePro."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary database
        self.test_db = Path(tempfile.mkdtemp()) / "test_taskqueue.db"
        self.queue = TaskQueuePro(db_path=self.test_db)
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove temporary database
        if self.test_db.parent.exists():
            shutil.rmtree(self.test_db.parent, ignore_errors=True)
    
    def test_01_add_basic_task(self):
        """Test adding a basic task."""
        task_id = self.queue.add_task(
            title="Test Task 1",
            description="This is a test task",
            assigned_to="ATLAS"
        )
        
        self.assertIsNotNone(task_id)
        self.assertTrue(task_id.startswith("task_"))
        
        # Verify task was added
        task = self.queue.get_task(task_id)
        self.assertEqual(task.title, "Test Task 1")
        self.assertEqual(task.assigned_to, "ATLAS")
    
    def test_02_add_task_with_priority(self):
        """Test adding task with specific priority."""
        task_id = self.queue.add_task(
            title="High Priority Task",
            priority="HIGH"
        )
        
        task = self.queue.get_task(task_id)
        self.assertEqual(task.priority, TaskPriority.HIGH.value)
    
    def test_03_add_scheduled_task(self):
        """Test adding a scheduled task."""
        future_time = datetime.now() + timedelta(hours=2)
        
        task_id = self.queue.add_task(
            title="Scheduled Task",
            schedule_at=future_time
        )
        
        task = self.queue.get_task(task_id)
        self.assertIsNotNone(task.scheduled_for)
    
    def test_04_get_pending_tasks(self):
        """Test retrieving pending tasks."""
        # Add multiple tasks
        self.queue.add_task(title="Task 1", assigned_to="ATLAS")
        self.queue.add_task(title="Task 2", assigned_to="ATLAS")
        self.queue.add_task(title="Task 3", assigned_to="BOLT")
        
        # Get pending tasks for ATLAS
        atlas_tasks = self.queue.get_pending(assigned_to="ATLAS")
        self.assertEqual(len(atlas_tasks), 2)
        
        # Get all pending tasks
        all_pending = self.queue.get_pending()
        self.assertEqual(len(all_pending), 3)
    
    def test_05_task_status_transitions(self):
        """Test task status transitions."""
        task_id = self.queue.add_task(title="Test Task")
        
        # Initial status should be PENDING
        task = self.queue.get_task(task_id)
        self.assertEqual(task.status, TaskStatus.PENDING.value)
        
        # Start task
        self.queue.start_task(task_id)
        task = self.queue.get_task(task_id)
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS.value)
        
        # Complete task
        self.queue.complete_task(task_id)
        task = self.queue.get_task(task_id)
        self.assertEqual(task.status, TaskStatus.COMPLETED.value)
        self.assertIsNotNone(task.completed_at)
    
    def test_06_fail_task(self):
        """Test failing a task."""
        task_id = self.queue.add_task(title="Test Task")
        
        # fail_task requires 'error' parameter
        self.queue.fail_task(task_id, error="Test failure")
        
        task = self.queue.get_task(task_id)
        self.assertEqual(task.status, TaskStatus.FAILED.value)
    
    def test_07_priority_ordering(self):
        """Test that tasks are ordered by priority."""
        # Add tasks with different priorities
        self.queue.add_task(title="Low Task", priority="LOW", assigned_to="ATLAS")
        self.queue.add_task(title="Critical Task", priority="CRITICAL", assigned_to="ATLAS")
        self.queue.add_task(title="Normal Task", priority="NORMAL", assigned_to="ATLAS")
        self.queue.add_task(title="High Task", priority="HIGH", assigned_to="ATLAS")
        
        # Get pending tasks
        tasks = self.queue.get_pending(assigned_to="ATLAS")
        
        # Should be sorted by priority (CRITICAL > HIGH > NORMAL > LOW)
        self.assertEqual(tasks[0].title, "Critical Task")
        self.assertEqual(tasks[1].title, "High Task")
        self.assertEqual(tasks[2].title, "Normal Task")
        self.assertEqual(tasks[3].title, "Low Task")
    
    def test_08_task_metadata(self):
        """Test storing and retrieving task metadata."""
        metadata = {
            "github_issue": "#123",
            "estimated_hours": 4,
            "tags": ["urgent", "bug"]
        }
        
        task_id = self.queue.add_task(
            title="Task with metadata",
            metadata=metadata
        )
        
        task = self.queue.get_task(task_id)
        self.assertEqual(task.metadata["github_issue"], "#123")
        self.assertEqual(task.metadata["estimated_hours"], 4)
        self.assertIn("urgent", task.metadata["tags"])
    
    def test_09_statistics(self):
        """Test getting queue statistics."""
        # Add various tasks
        task_id1 = self.queue.add_task(title="Task 1", assigned_to="ATLAS")
        task_id2 = self.queue.add_task(title="Task 2", assigned_to="ATLAS")
        task_id3 = self.queue.add_task(title="Task 3", assigned_to="BOLT")
        
        # Complete one
        self.queue.complete_task(task_id1)
        
        # Fail one
        self.queue.fail_task(task_id2, error="Test error")
        
        stats = self.queue.get_stats()
        
        # Check stats structure
        self.assertIn("by_status", stats)
        self.assertIn("by_agent", stats)
        self.assertIn("total_tasks", stats)
        
        self.assertEqual(stats["by_status"]["pending"], 1)
        self.assertEqual(stats["by_status"]["completed"], 1)
        self.assertEqual(stats["by_status"]["failed"], 1)
        self.assertEqual(stats["total_tasks"], 3)
    
    def test_10_database_persistence(self):
        """Test that tasks persist across instances."""
        # Add tasks
        task_id1 = self.queue.add_task(title="Task 1", assigned_to="ATLAS")
        task_id2 = self.queue.add_task(title="Task 2", priority="HIGH")
        
        # Create new instance with same database
        new_queue = TaskQueuePro(db_path=self.test_db)
        
        # Tasks should still exist
        task1 = new_queue.get_task(task_id1)
        self.assertIsNotNone(task1)
        self.assertEqual(task1.title, "Task 1")
        
        # Verify pending tasks are accessible
        pending = new_queue.get_pending()
        self.assertEqual(len(pending), 2)
    
    def test_11_empty_queue(self):
        """Test operations on empty queue."""
        pending = self.queue.get_pending()
        self.assertEqual(len(pending), 0)
        
        stats = self.queue.get_stats()
        self.assertEqual(stats["total_tasks"], 0)
    
    def test_12_task_with_no_assignment(self):
        """Test task without assigned agent."""
        task_id = self.queue.add_task(title="Unassigned Task")
        
        task = self.queue.get_task(task_id)
        self.assertIsNone(task.assigned_to)
        
        # Should appear in all pending tasks
        pending = self.queue.get_pending()
        self.assertEqual(len(pending), 1)
    
    def test_13_complete_with_result(self):
        """Test completing task with result data."""
        task_id = self.queue.add_task(title="Task with result")
        
        result_data = {"status": "success", "output": "Task completed"}
        self.queue.complete_task(task_id, result=result_data)
        
        task = self.queue.get_task(task_id)
        self.assertEqual(task.status, TaskStatus.COMPLETED.value)
    
    def test_14_get_task_not_found(self):
        """Test getting non-existent task."""
        task = self.queue.get_task("nonexistent_id")
        self.assertIsNone(task)
    
    def test_15_filter_by_assigned_agent(self):
        """Test filtering tasks by assigned agent."""
        self.queue.add_task(title="Task 1", assigned_to="ATLAS")
        self.queue.add_task(title="Task 2", assigned_to="BOLT")
        self.queue.add_task(title="Task 3", assigned_to="ATLAS")
        
        atlas_tasks = self.queue.get_pending(assigned_to="ATLAS")
        bolt_tasks = self.queue.get_pending(assigned_to="BOLT")
        
        self.assertEqual(len(atlas_tasks), 2)
        self.assertEqual(len(bolt_tasks), 1)


def run_tests():
    """Run all tests."""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTaskQueuePro)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    if result.wasSuccessful():
        print(f"[SUCCESS] All {result.testsRun} tests passed!")
    else:
        print(f"[FAILED] {len(result.failures)} failures, {len(result.errors)} errors")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
