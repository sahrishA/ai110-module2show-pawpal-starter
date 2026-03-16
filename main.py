from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date

# Create an Owner
owner = Owner(name="Jordan", preferences={"available_hours": [8, 18]})
print(f"Created Owner: {owner.name}")

# Create two Pets for the Owner
pet1 = Pet(name="Mochi", species="dog")
pet2 = Pet(name="Whiskers", species="cat")

# Add pets to owner (this sets the owner on pets)
owner.add_pet(pet1)
owner.add_pet(pet2)
print(f"Owner {owner.name} has pets: {[p.name for p in owner.get_pets()]}")

# Create Tasks for the pets
task1 = Task(title="Morning walk", duration_minutes=30, priority="high")
task2 = Task(title="Feeding", duration_minutes=10, priority="medium")
task3 = Task(title="Playtime", duration_minutes=20, priority="low")

# Add tasks to pets (this sets the pet on tasks)
pet1.add_task(task1)
pet1.add_task(task2)
pet2.add_task(task3)

print(f"Pet {pet1.name} has tasks: {[t.title for t in pet1.get_tasks()]}")
print(f"Pet {pet2.name} has tasks: {[t.title for t in pet2.get_tasks()]}")

# Test Scheduler for one pet (e.g., Mochi)
tasks_for_pet1 = pet1.get_tasks()
schedule = Scheduler.schedule_day(owner, pet1, tasks_for_pet1)

print("\nToday's Schedule for", pet1.name)
print(f"Date: {schedule.date}")
total_duration = schedule.get_total_duration()
print(f"Total scheduled time: {total_duration} minutes")
for st in schedule.scheduled_tasks:
    print(f"- {st.task.title} ({st.task.priority}): {st.start_time.strftime('%H:%M')} - {st.end_time.strftime('%H:%M')}")

# Trace data flow: Show how tasks are linked
print("\nData Flow Trace:")
for task in tasks_for_pet1:
    print(f"Task '{task.title}' belongs to Pet '{task.pet.name}' owned by '{task.pet.owner.name}'")

# Inspect Scheduler.schedule_day method (by showing its logic in action)
print("\nScheduler Method Inspection:")
print("Scheduler.schedule_day sorts tasks by priority (high > medium > low) and schedules sequentially from 8 AM.")
print("Sorted tasks order:", [t.title for t in sorted(tasks_for_pet1, key=lambda t: {'high': 0, 'medium': 1, 'low': 2}.get(t.priority, 3))])