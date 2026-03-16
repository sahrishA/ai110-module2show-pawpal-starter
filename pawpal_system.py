
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional

class Owner:
    def __init__(self, name: str, preferences: Optional[Dict] = None):
        self.name = name
        self.preferences = preferences or {}
        self.pets: List['Pet'] = []

    def add_pet(self, pet: 'Pet'):
        if pet not in self.pets:
            self.pets.append(pet)
            pet.owner = self

    def get_pets(self) -> List['Pet']:
        return self.pets

class Pet:
    def __init__(self, name: str, species: str, owner: Optional['Owner'] = None):
        self.name = name
        self.species = species
        self.owner = owner
        self.tasks: List['Task'] = []

    def add_task(self, task: 'Task'):
        if task not in self.tasks:
            self.tasks.append(task)
            task.pet = self

    def get_tasks(self) -> List['Task']:
        return self.tasks

class Task:
    def __init__(self, title: str, duration_minutes: int, priority: str, pet: Optional['Pet'] = None):
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.pet = pet

class ScheduledTask:
    def __init__(self, task: Task, start_time: datetime, end_time: datetime):
        self.task = task
        self.start_time = start_time
        self.end_time = end_time

class Schedule:
    def __init__(self, date: date):
        self.date = date
        self.scheduled_tasks: List[ScheduledTask] = []

    def add_scheduled_task(self, scheduled_task: ScheduledTask):
        self.scheduled_tasks.append(scheduled_task)

    def get_total_duration(self) -> int:
        return sum(st.task.duration_minutes for st in self.scheduled_tasks)

class Scheduler:
    @staticmethod
    def schedule_day(owner: Owner, pet: Pet, tasks: List[Task]) -> Schedule:
        # Implement Sorting: Sort tasks by priority (high > medium > low)
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        sorted_tasks = sorted(tasks, key=lambda t: priority_order.get(t.priority, 3))

        # Get available hours from owner preferences, default to 8 AM - 6 PM
        available_hours = owner.preferences.get('available_hours', [8, 18])
        start_hour, end_hour = available_hours[0], available_hours[1]

        schedule = Schedule(date.today())
        current_time = datetime.combine(schedule.date, datetime.min.time().replace(hour=start_hour))
        end_datetime = datetime.combine(schedule.date, datetime.min.time().replace(hour=end_hour))

        # Implement Filtering: Only schedule tasks that fit within available time
        for task in sorted_tasks:
            proposed_end_time = current_time + timedelta(minutes=task.duration_minutes)
            if proposed_end_time <= end_datetime:
                # No conflict with time limits, schedule it
                scheduled_task = ScheduledTask(task, current_time, proposed_end_time)
                schedule.add_scheduled_task(scheduled_task)
                current_time = proposed_end_time
            # Else, filter out (skip) the task as it doesn't fit

        # Debug Edge Case: If no tasks were scheduled (e.g., all tasks too long or available time too short)
        if not schedule.scheduled_tasks:
            # For debugging, we could log or raise, but for now, the schedule remains empty
            # This handles edge cases like insufficient time or oversized tasks
            pass

        return schedule
        