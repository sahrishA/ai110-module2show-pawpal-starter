import pytest
from datetime import date, datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler, Schedule, ScheduledTask

def test_owner_creation():
    owner = Owner("Alice")
    assert owner.name == "Alice"
    assert owner.pets == []
    assert owner.preferences == {}

def test_owner_with_preferences():
    owner = Owner("Bob", {"available_hours": [9, 17]})
    assert owner.name == "Bob"
    assert owner.preferences["available_hours"] == [9, 17]

def test_add_pet_to_owner():
    owner = Owner("Alice")
    pet = Pet("Fluffy", "cat")
    owner.add_pet(pet)
    assert pet in owner.pets
    assert pet.owner == owner
    assert len(owner.pets) == 1

def test_pet_creation():
    pet = Pet("Whiskers", "dog")
    assert pet.name == "Whiskers"
    assert pet.species == "dog"
    assert pet.tasks == []
    assert pet.owner is None

def test_add_task_to_pet():
    pet = Pet("Fluffy", "cat")
    task = Task("Feed", 15, "high")
    pet.add_task(task)
    assert task in pet.tasks
    assert task.pet == pet
    assert len(pet.tasks) == 1

def test_task_creation():
    task = Task("Walk", 30, "medium")
    assert task.title == "Walk"
    assert task.duration_minutes == 30
    assert task.priority == "medium"
    assert task.pet is None

def test_scheduler_sorting_by_priority():
    owner = Owner("Alice", {"available_hours": [8, 18]})
    pet = Pet("Fluffy", "cat")
    owner.add_pet(pet)
    task_low = Task("Low task", 10, "low")
    task_high = Task("High task", 10, "high")
    task_med = Task("Med task", 10, "medium")
    pet.add_task(task_low)
    pet.add_task(task_high)
    pet.add_task(task_med)
    schedule = Scheduler.schedule_day(owner, pet, [task_low, task_high, task_med])
    # Should be scheduled high, med, low
    assert schedule.scheduled_tasks[0].task.priority == "high"
    assert schedule.scheduled_tasks[1].task.priority == "medium"
    assert schedule.scheduled_tasks[2].task.priority == "low"

def test_scheduler_filtering_time_constraints():
    owner = Owner("Alice", {"available_hours": [8, 9]})  # Only 1 hour available
    pet = Pet("Fluffy", "cat")
    owner.add_pet(pet)
    task_long = Task("Long task", 120, "high")  # 2 hours, too long
    task_short = Task("Short task", 30, "high")  # Fits
    pet.add_task(task_long)
    pet.add_task(task_short)
    schedule = Scheduler.schedule_day(owner, pet, [task_long, task_short])
    # Only short task should be scheduled
    assert len(schedule.scheduled_tasks) == 1
    assert schedule.scheduled_tasks[0].task.title == "Short task"

def test_scheduler_edge_case_no_tasks_fit():
    owner = Owner("Alice", {"available_hours": [8, 8]})  # 0 hours available
    pet = Pet("Fluffy", "cat")
    owner.add_pet(pet)
    task = Task("Any task", 10, "high")
    pet.add_task(task)
    schedule = Scheduler.schedule_day(owner, pet, [task])
    # No tasks should fit
    assert len(schedule.scheduled_tasks) == 0

def test_schedule_creation():
    schedule = Schedule(date(2023, 10, 1))
    assert schedule.date == date(2023, 10, 1)
    assert schedule.scheduled_tasks == []

def test_schedule_add_task():
    schedule = Schedule(date.today())
    task = Task("Test", 20, "low")
    start = datetime.combine(schedule.date, datetime.min.time().replace(hour=8))
    end = start + timedelta(minutes=20)
    stask = ScheduledTask(task, start, end)
    schedule.add_scheduled_task(stask)
    assert len(schedule.scheduled_tasks) == 1
    assert schedule.get_total_duration() == 20

def test_scheduled_task_creation():
    task = Task("Test", 15, "high")
    start = datetime(2023, 10, 1, 9, 0)
    end = datetime(2023, 10, 1, 9, 15)
    stask = ScheduledTask(task, start, end)
    assert stask.task == task
    assert stask.start_time == start
    assert stask.end_time == end