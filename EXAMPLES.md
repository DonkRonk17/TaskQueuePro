# TaskQueuePro Examples

**10 Real-World Examples for Team Brain Workflow**

---

## Example 1: Add a Basic Task

```python
from taskqueuepro import TaskQueuePro

queue = TaskQueuePro()
task_id = queue.add_task(
    title="Review SynapseWatcher code",
    assigned_to="ATLAS"
)
print(f"Created task: {task_id}")
```

**Output:**
```
Created task: task_a7f3c2d1
```

**Use case:** Quick task assignment without priority or scheduling.

---

## Example 2: Add High-Priority Task

```python
from taskqueuepro import TaskQueuePro

queue = TaskQueuePro()
task_id = queue.add_task(
    title="Fix critical security bug",
    description="CVE-2026-1234 needs immediate patch",
    assigned_to="ATLAS",
    priority="CRITICAL"
)
```

**Output:**
```
Created task: task_b4e8f9a2
```

**Use case:** Urgent tasks that need immediate attention.

---

## Example 3: Schedule a Task

```python
from taskqueuepro import TaskQueuePro
from datetime import datetime, timedelta

queue = TaskQueuePro()

# Schedule for tomorrow morning
tomorrow_9am = (datetime.now() + timedelta(days=1)).replace(hour=9, minute=0, second=0)

task_id = queue.add_task(
    title="Generate daily report",
    assigned_to="CLIO",
    priority="NORMAL",
    schedule_at=tomorrow_9am
)
print(f"Task scheduled for: {tomorrow_9am}")
```

**Output:**
```
Task scheduled for: 2026-01-19 09:00:00
```

**Use case:** Recurring tasks, scheduled reviews, time-specific operations.

---

## Example 4: Get Your Pending Tasks

```python
from taskqueuepro import TaskQueuePro

queue = TaskQueuePro()

# Get all my pending tasks
my_tasks = queue.get_pending(assigned_to="ATLAS")

print(f"You have {len(my_tasks)} pending tasks:")
for task in my_tasks:
    print(f"  [{task.priority}] {task.title}")
```

**Output:**
```
You have 3 pending tasks:
  [4] Fix critical security bug
  [3] Review SynapseWatcher code
  [2] Update documentation
```

**Use case:** Morning standup - see what's on your plate.

---

## Example 5: Work Through Tasks

```python
from taskqueuepro import TaskQueuePro

queue = TaskQueuePro()

# Get high priority tasks
urgent_tasks = queue.get_tasks(priority="HIGH", status="PENDING")

for task in urgent_tasks:
    print(f"Starting: {task.title}")
    queue.start_task(task.task_id)
    
    # Do the work...
    # ...
    
    # Mark complete
    queue.complete_task(task.task_id)
    print(f"✅ Completed: {task.title}")
```

**Output:**
```
Starting: Review SynapseWatcher code
✅ Completed: Review SynapseWatcher code
Starting: Test MemoryBridge integration
✅ Completed: Test MemoryBridge integration
```

**Use case:** Automated task processing workflow.

---

## Example 6: Task with Metadata

```python
from taskqueuepro import TaskQueuePro

queue = TaskQueuePro()

task_id = queue.add_task(
    title="Build ContextCompressor v2",
    assigned_to="ATLAS",
    priority="HIGH",
    metadata={
        "github_issue": "#45",
        "estimated_hours": 8,
        "dependencies": ["compression_lib", "test_suite"],
        "project": "Q-Mode"
    }
)

# Later, retrieve with metadata
task = queue.get_task(task_id)
print(f"GitHub Issue: {task.metadata['github_issue']}")
print(f"Estimated: {task.metadata['estimated_hours']} hours")
```

**Output:**
```
GitHub Issue: #45
Estimated: 8 hours
```

**Use case:** Rich task context, project tracking, dependency management.

---

## Example 7: Team Workload View

```python
from taskqueuepro import TaskQueuePro

queue = TaskQueuePro()

agents = ["ATLAS", "FORGE", "BOLT", "CLIO", "NEXUS"]

print("Team Workload:")
for agent in agents:
    stats = queue.get_agent_stats(agent)
    print(f"{agent:10} | Pending: {stats['pending']:2} | In Progress: {stats['in_progress']:2} | Completed: {stats['completed']:3}")
```

**Output:**
```
Team Workload:
ATLAS      | Pending:  3 | In Progress:  1 | Completed:  28
FORGE      | Pending:  0 | In Progress:  0 | Completed:  12
BOLT       | Pending:  5 | In Progress:  2 | Completed:  45
CLIO       | Pending:  2 | In Progress:  1 | Completed:  15
NEXUS      | Pending:  1 | In Progress:  0 | Completed:   8
```

**Use case:** Team coordination, load balancing, status meetings.

---

## Example 8: Check Scheduled Tasks

```python
from taskqueuepro import TaskQueuePro

queue = TaskQueuePro()

# Get tasks that are ready to run (scheduled_for <= now)
ready_tasks = queue.get_scheduled_tasks()

print(f"Tasks ready to execute: {len(ready_tasks)}")
for task in ready_tasks:
    print(f"  {task.title} (scheduled for {task.scheduled_for})")
    queue.start_task(task.task_id)
```

**Output:**
```
Tasks ready to execute: 2
  Generate daily report (scheduled for 2026-01-18T09:00:00)
  Run backup script (scheduled for 2026-01-18T10:30:00)
```

**Use case:** Automated task execution, cron-like scheduling.

---

## Example 9: Fail a Task with Reason

```python
from taskqueuepro import TaskQueuePro

queue = TaskQueuePro()

task_id = "task_abc123"

# Task failed - record why
queue.fail_task(
    task_id,
    reason="Missing dependency: compression_lib not installed"
)

# Later, review failed tasks
failed = queue.get_tasks(status="FAILED")
for task in failed:
    print(f"❌ {task.title}")
    print(f"   Reason: {task.metadata.get('failure_reason', 'Unknown')}")
```

**Output:**
```
❌ Build ContextCompressor v2
   Reason: Missing dependency: compression_lib not installed
```

**Use case:** Error tracking, debugging, task retrospectives.

---

## Example 10: Project Management Dashboard

```python
from taskqueuepro import TaskQueuePro

queue = TaskQueuePro()
project_name = "Q-Mode Tools"

# Get all tasks for project
all_tasks = queue.get_pending() + queue.get_tasks(status="COMPLETED")
project_tasks = [t for t in all_tasks if t.metadata.get("project") == project_name]

# Calculate metrics
total = len(project_tasks)
completed = len([t for t in project_tasks if t.status == "completed"])
in_progress = len([t for t in project_tasks if t.status == "in_progress"])
pending = len([t for t in project_tasks if t.status == "pending"])

print(f"📊 Project: {project_name}")
print(f"Total Tasks: {total}")
print(f"Completed: {completed} ({completed/total*100:.1f}%)")
print(f"In Progress: {in_progress}")
print(f"Pending: {pending}")
print(f"\nNext up:")
for task in [t for t in project_tasks if t.status == "pending"][:3]:
    print(f"  • [{task.priority}] {task.title}")
```

**Output:**
```
📊 Project: Q-Mode Tools
Total Tasks: 18
Completed: 12 (66.7%)
In Progress: 2
Pending: 4

Next up:
  • [3] Build TaskRouter
  • [3] Integrate SynapseWatcher
  • [2] Write documentation
```

**Use case:** Project tracking, progress reports, sprint planning.

---

## Command Line Examples

```bash
# Add a task
python taskqueuepro.py add "Review code" --assign ATLAS --priority HIGH

# List all pending tasks
python taskqueuepro.py list --status pending

# List tasks for specific agent
python taskqueuepro.py list --assign BOLT --status pending

# Complete a task
python taskqueuepro.py complete task_abc123

# View overall statistics
python taskqueuepro.py stats

# View agent statistics
python taskqueuepro.py stats --agent ATLAS

# Export all tasks to JSON
python taskqueuepro.py export --format json --output tasks.json

# Export completed tasks only
python taskqueuepro.py export --status completed --format csv --output completed.csv
```

---

## Integration Examples

### With SynapseLink

```python
from synapselink import SynapseLink
from taskqueuepro import TaskQueuePro

# Forge assigns task and notifies via Synapse
synapse = SynapseLink()
queue = TaskQueuePro()

task_id = queue.add_task(
    title="Build MemoryBridge v2",
    assigned_to="ATLAS",
    priority="HIGH"
)

synapse.send_message(
    to="ATLAS",
    subject="New HIGH priority task",
    body={"task_id": task_id, "action": "check_queue"}
)
```

### With SynapseWatcher

```python
from synapsewatcher import SynapseWatcher
from taskqueuepro import TaskQueuePro

def auto_check_tasks():
    """Automatically check for new tasks every 5 minutes."""
    queue = TaskQueuePro()
    tasks = queue.get_pending(assigned_to="ATLAS")
    
    if tasks:
        urgent = [t for t in tasks if t.priority >= 3]
        if urgent:
            print(f"⚡ URGENT: {len(urgent)} high-priority tasks waiting!")

watcher = SynapseWatcher()
watcher.add_callback(auto_check_tasks, interval=300)
watcher.start()
```

---

**Need more examples?** Check the main [README.md](README.md) for detailed API documentation.
