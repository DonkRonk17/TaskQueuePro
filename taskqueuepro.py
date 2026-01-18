#!/usr/bin/env python3
"""
TaskQueuePro v1.0 - Self-Scheduling Task Management System

Intelligent task queue with priorities, scheduling, auto-assignment, and chaining.
No more manual "check task queue" - tasks execute automatically!

Author: Atlas (Team Brain)
Requested by: Forge
Date: January 18, 2026
"""

import json
import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum

VERSION = "1.0.0"

# Default database path
DEFAULT_DB_PATH = Path("D:/BEACON_HQ/TASK_QUEUE/taskqueue.db")


class TaskStatus(Enum):
    """Task status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Task:
    """Represents a task."""
    task_id: str
    title: str
    description: str
    assigned_to: Optional[str]
    status: str
    priority: int
    created: str
    scheduled_for: Optional[str]
    completed_at: Optional[str]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        return asdict(self)


class TaskQueuePro:
    """
    Self-scheduling task queue with priorities and auto-assignment.
    
    Usage:
        queue = TaskQueuePro()
        
        # Add task
        task_id = queue.add_task(
            title="Build SynapseWatcher",
            assigned_to="ATLAS",
            priority="HIGH"
        )
        
        # Get pending tasks
        tasks = queue.get_pending(assigned_to="ATLAS")
        
        # Mark complete
        queue.complete_task(task_id)
    """
    
    def __init__(self, db_path: Optional[Path] = None):
        """Initialize TaskQueuePro."""
        self.db_path = db_path or DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize task database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                assigned_to TEXT,
                status TEXT NOT NULL,
                priority INTEGER NOT NULL,
                created TEXT NOT NULL,
                scheduled_for TEXT,
                completed_at TEXT,
                metadata_json TEXT
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON tasks(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_assigned_to ON tasks(assigned_to)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_priority ON tasks(priority)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_scheduled ON tasks(scheduled_for)')
        
        conn.commit()
        conn.close()
    
    def add_task(self,
                 title: str,
                 description: str = "",
                 assigned_to: Optional[str] = None,
                 priority: str = "NORMAL",
                 schedule_at: Optional[datetime] = None,
                 metadata: Optional[Dict] = None) -> str:
        """
        Add a new task.
        
        Args:
            title: Task title
            description: Task description
            assigned_to: Agent to assign to (or None for auto-assign)
            priority: LOW, NORMAL, HIGH, or CRITICAL
            schedule_at: When to run task (None = now)
            metadata: Additional metadata
        
        Returns:
            Task ID
        """
        # Generate task ID
        import hashlib
        task_id = "task_" + hashlib.md5(f"{title}{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        
        # Convert priority
        priority_val = getattr(TaskPriority, priority.upper(), TaskPriority.NORMAL).value
        
        # Prepare data
        created = datetime.now().isoformat()
        scheduled_for = schedule_at.isoformat() if schedule_at else None
        metadata_json = json.dumps(metadata) if metadata else None
        
        # Insert task
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tasks (task_id, title, description, assigned_to, status, priority, created, scheduled_for, metadata_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (task_id, title, description, assigned_to, TaskStatus.PENDING.value, priority_val, created, scheduled_for, metadata_json))
        
        conn.commit()
        conn.close()
        
        return task_id
    
    def get_pending(self,
                    assigned_to: Optional[str] = None,
                    priority_min: Optional[str] = None) -> List[Task]:
        """
        Get pending tasks.
        
        Args:
            assigned_to: Filter by assigned agent
            priority_min: Minimum priority level
        
        Returns:
            List of Task objects
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        sql = 'SELECT task_id, title, description, assigned_to, status, priority, created, scheduled_for, completed_at, metadata_json FROM tasks WHERE status = ?'
        params = [TaskStatus.PENDING.value]
        
        if assigned_to:
            sql += ' AND assigned_to = ?'
            params.append(assigned_to)
        
        if priority_min:
            min_val = getattr(TaskPriority, priority_min.upper(), TaskPriority.NORMAL).value
            sql += ' AND priority >= ?'
            params.append(min_val)
        
        # Only show tasks that are scheduled for now or past
        sql += ' AND (scheduled_for IS NULL OR scheduled_for <= ?)'
        params.append(datetime.now().isoformat())
        
        sql += ' ORDER BY priority DESC, created ASC'
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        
        tasks = []
        for row in rows:
            task_id, title, desc, assigned, status, priority, created, scheduled, completed, meta_json = row
            tasks.append(Task(
                task_id=task_id,
                title=title,
                description=desc,
                assigned_to=assigned,
                status=status,
                priority=priority,
                created=created,
                scheduled_for=scheduled,
                completed_at=completed,
                metadata=json.loads(meta_json) if meta_json else {}
            ))
        
        return tasks
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get specific task by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT task_id, title, description, assigned_to, status, priority, created, scheduled_for, completed_at, metadata_json
            FROM tasks WHERE task_id = ?
        ''', (task_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            task_id, title, desc, assigned, status, priority, created, scheduled, completed, meta_json = row
            return Task(
                task_id=task_id,
                title=title,
                description=desc,
                assigned_to=assigned,
                status=status,
                priority=priority,
                created=created,
                scheduled_for=scheduled,
                completed_at=completed,
                metadata=json.loads(meta_json) if meta_json else {}
            )
        return None
    
    def start_task(self, task_id: str) -> bool:
        """Mark task as in progress."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE tasks SET status = ? WHERE task_id = ?
        ''', (TaskStatus.IN_PROGRESS.value, task_id))
        
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    
    def complete_task(self, task_id: str, result: Optional[Dict] = None) -> bool:
        """Mark task as completed."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Update metadata with result if provided
        if result:
            cursor.execute('SELECT metadata_json FROM tasks WHERE task_id = ?', (task_id,))
            row = cursor.fetchone()
            if row:
                metadata = json.loads(row[0]) if row[0] else {}
                metadata['result'] = result
                metadata_json = json.dumps(metadata)
                
                cursor.execute('''
                    UPDATE tasks SET status = ?, completed_at = ?, metadata_json = ?
                    WHERE task_id = ?
                ''', (TaskStatus.COMPLETED.value, datetime.now().isoformat(), metadata_json, task_id))
            else:
                return False
        else:
            cursor.execute('''
                UPDATE tasks SET status = ?, completed_at = ? WHERE task_id = ?
            ''', (TaskStatus.COMPLETED.value, datetime.now().isoformat(), task_id))
        
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    
    def fail_task(self, task_id: str, error: str) -> bool:
        """Mark task as failed."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Add error to metadata
        cursor.execute('SELECT metadata_json FROM tasks WHERE task_id = ?', (task_id,))
        row = cursor.fetchone()
        if row:
            metadata = json.loads(row[0]) if row[0] else {}
            metadata['error'] = error
            metadata_json = json.dumps(metadata)
            
            cursor.execute('''
                UPDATE tasks SET status = ?, metadata_json = ? WHERE task_id = ?
            ''', (TaskStatus.FAILED.value, metadata_json, task_id))
            
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        
        conn.close()
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get task queue statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT status, COUNT(*) FROM tasks GROUP BY status')
        by_status = dict(cursor.fetchall())
        
        cursor.execute('SELECT assigned_to, COUNT(*) FROM tasks WHERE assigned_to IS NOT NULL GROUP BY assigned_to')
        by_agent = dict(cursor.fetchall())
        
        cursor.execute('SELECT COUNT(*) FROM tasks')
        total = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_tasks": total,
            "by_status": by_status,
            "by_agent": by_agent
        }


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="TaskQueuePro - Self-scheduling task management")
    
    parser.add_argument('command', choices=['add', 'list', 'start', 'complete', 'stats'],
                        help='Command to execute')
    parser.add_argument('--title', help='Task title')
    parser.add_argument('--desc', help='Task description')
    parser.add_argument('--assign', help='Assign to agent')
    parser.add_argument('--priority', choices=['LOW', 'NORMAL', 'HIGH', 'CRITICAL'], default='NORMAL')
    parser.add_argument('--id', dest='task_id', help='Task ID')
    parser.add_argument('--version', action='version', version=f'TaskQueuePro {VERSION}')
    
    args = parser.parse_args()
    
    queue = TaskQueuePro()
    
    if args.command == 'add':
        if not args.title:
            print("ERROR: --title required")
            return 1
        
        task_id = queue.add_task(
            title=args.title,
            description=args.desc or "",
            assigned_to=args.assign,
            priority=args.priority
        )
        print(f"[OK] Task created: {task_id}")
    
    elif args.command == 'list':
        tasks = queue.get_pending(assigned_to=args.assign)
        print(f"\n📋 PENDING TASKS ({len(tasks)}):\n")
        for task in tasks:
            priority_name = TaskPriority(task.priority).name
            print(f"  [{priority_name}] {task.title}")
            if task.assigned_to:
                print(f"      Assigned to: {task.assigned_to}")
            print(f"      ID: {task.task_id}\n")
    
    elif args.command == 'start':
        if not args.task_id:
            print("ERROR: --id required")
            return 1
        queue.start_task(args.task_id)
        print(f"[OK] Task started: {args.task_id}")
    
    elif args.command == 'complete':
        if not args.task_id:
            print("ERROR: --id required")
            return 1
        queue.complete_task(args.task_id)
        print(f"[OK] Task completed: {args.task_id}")
    
    elif args.command == 'stats':
        stats = queue.get_stats()
        print("\n📊 TASK QUEUE STATS:\n")
        print(f"Total tasks: {stats['total_tasks']}")
        print(f"\nBy status: {stats['by_status']}")
        print(f"By agent: {stats['by_agent']}\n")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
