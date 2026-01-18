# TaskQueuePro

Self-scheduling task management with priorities and auto-assignment.

## Quick Start
```python
from taskqueuepro import TaskQueuePro
queue = TaskQueuePro()
task_id = queue.add_task('Build tool', assigned_to='ATLAS', priority='HIGH')
tasks = queue.get_pending(assigned_to='ATLAS')
queue.complete_task(task_id)
```
