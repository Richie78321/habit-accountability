# Habit Accountability

A simple script to broadcast to a Discord server when you have failed to complete a task on time.

## Configuration
Create a file `habits.yaml` in the root directory that defines the IDs of the Todoist tasks and the message to send if they are overdue.
``` yaml
habits:
  - task_id: 1234
    task_failure_message: Message 1
  - task_id: 5678
    task_failure_message: Message 2
```