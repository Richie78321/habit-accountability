# Habit Accountability

A simple script to broadcast to a Discord server when you have failed to complete a task on time.

## Setup
1. Fork this repository.
2. In the [GitHub Actions config file](.github/workflows/habit-accountability.yaml), edit the following values:
   * Under the `schedule` value, choose when and how often this should run. This should run infrequently enough to give you time to reschedule overdue tasks, as this program will continue to count overdue tasks until they are rescheduled. My recommendation is once per day at midnight.
   * Under the `IMPLICIT_TIMEZONE` value, enter your local timezone (the full list of options is available [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)).
3. Add two secrets to your repository: your Todoist API key under `TODOIST_APIKEY`, and the URL for your [Discord webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) under `DISCORD_WEBHOOK`.

## Configuration
Create a file `habits.yaml` in the root directory that defines the IDs of the Todoist tasks and the messages to send if they are overdue.
``` yaml
habits:
  - task_id: 1234
    task_failure_message: Message 1
  - task_id: 5678
    task_failure_message: Message 2
```
