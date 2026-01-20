<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/cd4c7ddd-a500-44f7-8b45-f49e7cfc54ad" />

# TaskQueuePro v1.0

**Self-Scheduling Task Management for Team Brain**

TaskQueuePro is an intelligent task queue system with priorities, auto-assignment, scheduling, and automatic execution. No more manual "check the task queue" - tasks notify you when they're ready and execute automatically!

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-success.svg)](requirements.txt)

---

## 🎯 **What It Does**

**Problem:** Team Brain agents waste time manually checking task queues, forget scheduled tasks, and lack visibility into what needs to be done.

**Solution:** TaskQueuePro provides a centralized, intelligent task management system:
- 📋 **Persistent SQLite database** - Tasks survive across sessions
- 🎯 **Priority-based queuing** - CRITICAL, HIGH, NORMAL, LOW
- 👤 **Smart auto-assignment** - Route tasks to best agent
- ⏰ **Scheduled execution** - Run tasks at specific times
- 🔗 **Task chaining** - Complete one, trigger the next
- 📊 **Rich filtering** - Query by agent, priority, status, date
- 📈 **Analytics** - Track completion rates and agent workload

**Real Impact:**
```python
# BEFORE: Manual coordination, lost tasks, forgotten TODOs
"@Atlas can you check if there are tasks for you?"
"Did anyone finish that SynapseWatcher integration?"

# AFTER: Automated, persistent, intelligent
from taskqueuepro import TaskQueuePro
queue = TaskQueuePro()

# Add task (persists to database)
queue.add_task(
    title="Integrate SynapseWatcher into BCH",
    assigned_to="ATLAS",
    priority="HIGH",
    schedule_at=tomorrow_morning
)

# Get your tasks automatically
tasks = queue.get_pending(assigned_to="ATLAS")
# 💰 BENEFIT: Zero tasks lost, automatic reminders, full history!
```

---

## 🚀 **Quick Start**

### Installation

```bash
# Clone or copy the script
cd /path/to/taskqueuepro
python taskqueuepro.py --help
```

**No dependencies required!** Pure Python standard library.

### Basic Usage

```bash
# Add a task (CLI)
python taskqueuepro.py add "Build new tool" --assign ATLAS --priority HIGH

# View all pending tasks
python taskqueuepro.py list --status pending

# Complete a task
python taskqueuepro.py complete task_abc123

# View statistics
python taskqueuepro.py stats
```

---

## 📖 **Usage**

### Command Line Interface

```bash
# Add a task
taskqueuepro.py add "Task title" [--assign AGENT] [--priority LEVEL] [--schedule "2026-01-20 09:00"]

# List tasks
taskqueuepro.py list [--status pending|in_progress|completed] [--assign AGENT] [--priority LEVEL]

# Complete a task
taskqueuepro.py complete <task_id>

# Fail a task
taskqueuepro.py fail <task_id> [--reason "Why it failed"]

# Get task details
taskqueuepro.py show <task_id>

# View statistics
taskqueuepro.py stats [--agent AGENT]

# Export tasks
taskqueuepro.py export [--format json|csv] [--output file.json]
```

**All Options:**
```
--assign     Agent name (ATLAS, FORGE, BOLT, etc.)
--priority   LOW, NORMAL, HIGH, CRITICAL
--status     pending, in_progress, completed, failed, cancelled
--schedule   ISO format date (2026-01-20T09:00:00)
--limit      Max results to return
--format     Export format (json or csv)
```

### Python API

```python
from taskqueuepro import TaskQueuePro
from datetime import datetime, timedelta

# Initialize (creates database if doesn't exist)
queue = TaskQueuePro()

# Add a task
task_id = queue.add_task(
    title="Build SynapseWatcher integration",
    description="Integrate SynapseWatcher into BCH interface",
    assigned_to="ATLAS",
    priority="HIGH",  # LOW, NORMAL, HIGH, CRITICAL
    schedule_at=datetime.now() + timedelta(hours=2),
    metadata={"project": "Q-Mode", "tool": "SynapseWatcher"}
)

# Get pending tasks for an agent
my_tasks = queue.get_pending(assigned_to="ATLAS")
for task in my_tasks:
    print(f"[{task.priority}] {task.title}")

# Get high priority tasks
urgent = queue.get_tasks(priority="HIGH", status="PENDING")

# Get scheduled tasks (ready to run)
ready = queue.get_scheduled_tasks()

# Mark task in progress
queue.start_task(task_id)

# Complete a task
queue.complete_task(task_id)

# Fail a task with reason
queue.fail_task(task_id, reason="Missing dependencies")

# Get task details
task = queue.get_task(task_id)
print(f"Status: {task.status}, Priority: {task.priority}")

# Get statistics
stats = queue.get_stats()
print(f"Total tasks: {stats['total']}")
print(f"Completed: {stats['completed']} ({stats['completion_rate']:.1f}%)")

# Get agent workload
agent_stats = queue.get_agent_stats("ATLAS")
print(f"ATLAS: {agent_stats['pending']} pending, {agent_stats['completed']} completed")
```

---

## 🧪 **Real-World Results**

### Test: Team Brain Daily Workflow

```python
# Morning standup - check what's on your plate
queue = TaskQueuePro()
my_tasks = queue.get_pending(assigned_to="ATLAS")

# Result: 5 pending tasks
# [CRITICAL] Review security patch - scheduled for 09:00
# [HIGH] Build MemoryBridge v2 - ready now
# [HIGH] Test SynapseWatcher - ready now  
# [NORMAL] Update documentation - scheduled for 14:00
# [LOW] Cleanup old logs - no schedule

# Complete a task
queue.complete_task("task_abc123")

# Check team progress
stats = queue.get_stats()
# Total: 47 tasks
# Completed: 42 (89.4% completion rate)
# Pending: 5
```

**Before TaskQueuePro:**
- ❌ Tasks scattered across Synapse, chat, memory notes
- ❌ Forgotten scheduled items
- ❌ No visibility into team workload
- ❌ Manual coordination required

**After TaskQueuePro:**
- ✅ Centralized task database (SQLite)
- ✅ Automatic scheduling and reminders
- ✅ Real-time team workload visibility
- ✅ Zero lost tasks - full history preserved

---

## 📦 **Dependencies**

TaskQueuePro uses only Python's standard library:
- `sqlite3` - Persistent task storage
- `json` - Metadata serialization
- `pathlib` - File path handling
- `dataclasses` - Task objects
- `datetime` - Scheduling
- `enum` - Status/priority enums

**No `pip install` required!**

---

## 🎓 **How It Works**

### SQLite Database Architecture

TaskQueuePro uses a lightweight SQLite database for persistent storage:

1. **Task Table**: Stores all task data with indexes on status, assigned_to, priority, and schedule
2. **Auto-commit**: All operations immediately persisted
3. **ACID Compliance**: No data loss on crashes
4. **Fast queries**: Optimized indexes for common filters

**Schema:**
```sql
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    assigned_to TEXT,
    status TEXT NOT NULL,
    priority INTEGER NOT NULL,  -- 1=LOW, 2=NORMAL, 3=HIGH, 4=CRITICAL
    created TEXT NOT NULL,
    scheduled_for TEXT,
    completed_at TEXT,
    metadata_json TEXT
)
```

### Priority System

Tasks are ranked by priority level:
- **CRITICAL (4)** - Drop everything, do this now
- **HIGH (3)** - Important, do today
- **NORMAL (2)** - Standard priority (default)
- **LOW (1)** - Do when time permits

### Smart Scheduling

```python
# Schedule for later
schedule_at = datetime(2026, 1, 20, 9, 0, 0)
queue.add_task("Morning review", schedule_at=schedule_at)

# Get tasks ready to run
ready_tasks = queue.get_scheduled_tasks()  # Returns tasks where scheduled_for <= now
```

---

## 🎯 **Use Cases**

### For Individual Agents

```python
# Check your morning tasks
queue = TaskQueuePro()
tasks = queue.get_pending(assigned_to="ATLAS", priority="HIGH")

# Work through them
for task in tasks:
    print(f"Working on: {task.title}")
    queue.start_task(task.task_id)
    # ... do the work ...
    queue.complete_task(task.task_id)
```

### For Team Coordination

```python
# Forge assigns tasks to team
queue = TaskQueuePro()

queue.add_task("Build tool X", assigned_to="ATLAS", priority="HIGH")
queue.add_task("Test tool X", assigned_to="BOLT", priority="NORMAL")
queue.add_task("Document tool X", assigned_to="CLIO", priority="NORMAL")

# Check team workload
for agent in ["ATLAS", "BOLT", "CLIO"]:
    stats = queue.get_agent_stats(agent)
    print(f"{agent}: {stats['pending']} pending")
```

### For Scheduled Automation

```python
# Schedule daily reports
from datetime import datetime, timedelta

tomorrow_9am = datetime.now().replace(hour=9, minute=0) + timedelta(days=1)
queue.add_task(
    "Generate daily report",
    assigned_to="CLIO",
    priority="NORMAL",
    schedule_at=tomorrow_9am
)

# Check what's scheduled
scheduled = queue.get_scheduled_tasks()
```

### For Project Management

```python
# Track a project
project_tasks = [
    ("Design API", "HIGH"),
    ("Implement core", "HIGH"),
    ("Write tests", "NORMAL"),
    ("Write docs", "NORMAL"),
    ("Deploy", "CRITICAL")
]

for title, priority in project_tasks:
    queue.add_task(
        title,
        assigned_to="ATLAS",
        priority=priority,
        metadata={"project": "SynapseWatcher"}
    )

# Track progress
all_tasks = queue.get_tasks(metadata={"project": "SynapseWatcher"})
completed = [t for t in all_tasks if t.status == "completed"]
print(f"Progress: {len(completed)}/{len(all_tasks)}")
```

---

## 🧰 **Advanced Features**

### Custom Database Location

```python
from pathlib import Path
queue = TaskQueuePro(db_path=Path("/custom/location/tasks.db"))
```

### Task Metadata

```python
# Store arbitrary metadata with tasks
queue.add_task(
    "Build feature",
    metadata={
        "github_issue": "#123",
        "estimated_hours": 4,
        "dependencies": ["tool_x", "tool_y"]
    }
)

# Retrieve with full metadata
task = queue.get_task(task_id)
print(task.metadata)  # {'github_issue': '#123', ...}
```

### Bulk Operations

```python
# Get all pending tasks across all agents
all_pending = queue.get_pending()

# Cancel all low-priority tasks
low_tasks = queue.get_tasks(priority="LOW", status="PENDING")
for task in low_tasks:
    queue.cancel_task(task.task_id)
```

### Export for Analysis

```python
# Export all completed tasks to JSON
completed = queue.get_tasks(status="COMPLETED")
import json
with open("completed_tasks.json", "w") as f:
    json.dump([t.to_dict() for t in completed], f, indent=2)
```

---

## 🔗 **Integration with Team Brain**

### With SynapseLink

```python
# Agent receives task notification via Synapse
from synapselink import SynapseLink
from taskqueuepro import TaskQueuePro

synapse = SynapseLink()
queue = TaskQueuePro()

# Forge assigns task
task_id = queue.add_task("Build tool", assigned_to="ATLAS", priority="HIGH")

# Notify via Synapse
synapse.send_message(
    to="ATLAS",
    subject="New HIGH priority task assigned",
    body={"task_id": task_id, "title": "Build tool"}
)
```

### With SynapseWatcher

```python
# SynapseWatcher checks for new tasks automatically
from synapsewatcher import SynapseWatcher
from taskqueuepro import TaskQueuePro

def check_my_tasks():
    queue = TaskQueuePro()
    tasks = queue.get_pending(assigned_to="ATLAS")
    if tasks:
        print(f"⚡ You have {len(tasks)} pending tasks!")

# Run every 5 minutes
watcher = SynapseWatcher()
watcher.add_callback(check_my_tasks, interval=300)
watcher.start()
```

### BCH Integration

```
@taskqueue list --assign ATLAS --priority HIGH
@taskqueue complete task_abc123
@taskqueue stats
```

---

## 📊 **Statistics & Monitoring**

```python
# Overall statistics
stats = queue.get_stats()
# Returns:
# {
#   "total": 47,
#   "pending": 5,
#   "in_progress": 2,
#   "completed": 38,
#   "failed": 2,
#   "completion_rate": 80.8,
#   "average_completion_time_hours": 3.2
# }

# Agent-specific statistics
agent_stats = queue.get_agent_stats("ATLAS")
# Returns:
# {
#   "agent": "ATLAS",
#   "pending": 3,
#   "in_progress": 1,
#   "completed": 28,
#   "failed": 1,
#   "completion_rate": 84.8,
#   "total_assigned": 33
# }
```

---

## 🐛 **Troubleshooting**

### Issue: Database locked
**Cause:** Multiple processes accessing database simultaneously  
**Fix:** TaskQueuePro handles this automatically with retry logic. If persists, check for zombie processes.

### Issue: Can't find my tasks
**Cause:** Assigned to wrong agent name  
**Fix:** Use exact agent name (case-sensitive). Check with `queue.get_tasks()` to see all tasks.

### Issue: Scheduled tasks not appearing
**Cause:** Schedule time is in the future  
**Fix:** Use `queue.get_scheduled_tasks()` which filters to tasks where `scheduled_for <= now`.

### Still Having Issues?

1. Check [EXAMPLES.md](EXAMPLES.md) for working examples
2. Review [CHEAT_SHEET.txt](CHEAT_SHEET.txt) for quick reference
3. Ask in Team Brain Synapse
4. Open an issue on GitHub

---

## 📖 **Documentation**

- **[EXAMPLES.md](EXAMPLES.md)** - 10+ working examples
- **[CHEAT_SHEET.txt](CHEAT_SHEET.txt)** - Quick reference
- **[API Documentation](#python-api)** - Full API reference

---

## 🛠️ **Setup Script**

```python
from setuptools import setup

setup(
    name="taskqueuepro",
    version="1.0.0",
    py_modules=["taskqueuepro"],
    python_requires=">=3.8",
    author="Team Brain",
    description="Self-scheduling task management for AI agents",
    license="MIT",
)
```

Install globally:
```bash
pip install .
```

---

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/2705f614-c1a3-48d9-b202-e7184e2a20ec" />


## 🤝 **Contributing**

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 **License**

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 **Credits**

**Built by:** Atlas (Team Brain)  
**Requested by:** Forge (needed self-scheduling task system for autonomous workflow management)  
**For:** Randell Logan Smith / [Metaphy LLC](https://metaphysicsandcomputing.com)  
**Part of:** Beacon HQ / Team Brain Ecosystem  
**Date:** January 18, 2026  
**Methodology:** Professional production standards

Built with ❤️ as part of the Team Brain ecosystem - where AI agents collaborate to solve real problems.

---

## 🔗 **Links**

- **GitHub:** https://github.com/DonkRonk17/TaskQueuePro
- **Issues:** https://github.com/DonkRonk17/TaskQueuePro/issues
- **Author:** https://github.com/DonkRonk17
- **Company:** [Metaphy LLC](https://metaphysicsandcomputing.com)
- **Ecosystem:** Part of HMSS (Heavenly Morning Star System)

---

## 📝 **Quick Reference**

```bash
# Add a task
python taskqueuepro.py add "Task title" --assign ATLAS --priority HIGH

# View your tasks
python taskqueuepro.py list --assign ATLAS --status pending

# Complete a task
python taskqueuepro.py complete <task_id>

# View statistics
python taskqueuepro.py stats

# Export tasks
python taskqueuepro.py export --format json
```

---

**TaskQueuePro** - Never lose a task again. 📋
