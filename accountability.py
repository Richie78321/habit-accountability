import os
import yaml
import requests
import pytz
from datetime import datetime, timedelta
from dateutil.parser import isoparse
from todoist.api import TodoistAPI

if not os.getenv('GITHUB_ACTIONS'):
  # Not running in GitHub Actions. Use python-dotenv to load env variables.
  from dotenv import load_dotenv
  load_dotenv()

implicit_timezone = pytz.timezone(os.getenv('IMPLICIT_TIMEZONE'))
todoist_token = os.getenv('TODOIST_APIKEY')
if todoist_token is None:
  raise Exception('Please set TODOIST_APIKEY as an environment variable.')
discord_webhook = os.getenv('DISCORD_WEBHOOK')
if discord_webhook is None:
  raise Exception('Please set DISCORD_WEBHOOK as an environment variable.')

class Habit(object):
  def __init__(self, todoist_api, habit):
    self.habit = habit
    
    response = todoist_api.items.get(item_id=habit['task_id'])
    if response is not None:
      self.todoist_item = response['item']

  def is_valid_habit(self):
    if self.todoist_item is None:
      return False

    conditions = [
      self.todoist_item['due'].get('date') if self.todoist_item['due'] else None, # Task must have a due date.
      not self.todoist_item['in_history'], # Task should not be archived.
      not self.todoist_item['is_deleted'], # Task should not be deleted.
      self.habit['task_failure_message'], # Habit must have a failure message.
    ]

    return all(conditions)

  def due_date(self):
    date_iso_string = self.todoist_item['due'].get('date')
    parsed_date = isoparse(date_iso_string)

    due_date_timezone = self.todoist_item['due'].get('timezone')
    if due_date_timezone is None:
      # No timezone, need to use implicit timezone (otherwise it would always be implicitly UTC)
      parsed_date = implicit_timezone.localize(parsed_date)

    if 'T' in date_iso_string:
      # There is a time component of the due date. Interpret literally.
      return parsed_date
    else:
      # There is no time component of this due date. Interpret as beginning of next day.
      return parsed_date + timedelta(days=1)

  def is_overdue(self):
    return self.due_date() <= pytz.utc.localize(datetime.utcnow())

  def broadcast_failure_message(self):
    if self.habit['task_failure_message'] is None:
      return

    requests.post(discord_webhook, json={
      'content': '**Habit Accountability**: {}'.format(self.habit['task_failure_message'])
    })
    print("Broadcasted failure message for uncompleted task with ID {}.".format(self.habit['task_id']))

def broadcast_overdue_habits(habit_configs):
  api = TodoistAPI(todoist_token)
  api.sync()

  for habit_config in habit_configs:
    habit = Habit(api, habit_config)
    if habit.is_valid_habit():
      if habit.is_overdue():
        habit.broadcast_failure_message()
    else:
      print("Task with ID {} is not a valid task. Continuing...".format(task_id))

def main():
  with open("habits.yaml", 'r') as stream:
    habit_configs = yaml.safe_load(stream)['habits']

  broadcast_overdue_habits(habit_configs)
  print("Check completed.")

if __name__ == '__main__':
  main()