from datetime import date
from src.scheduler import Owner, Pet, Task, Scheduler

owner = Owner("Kimberly", 90, "Morning tasks preferred")

dog = Pet("Buddy", "Dog", 3)
cat = Pet("Luna", "Cat", 2)

owner.add_pet(dog)
owner.add_pet(cat)

dog.add_task(Task("Feed Buddy", 10, 2, "09:00", "daily", date.today()))
dog.add_task(Task("Morning walk", 30, 1, "08:00", "daily", date.today()))
cat.add_task(Task("Clean litter box", 15, 1, "07:30", "daily", date.today()))
cat.add_task(Task("Brush Luna", 10, 3, "08:00", "weekly", date.today()))

scheduler = Scheduler(owner)

print("Today's Schedule")
print("-" * 40)
for task in scheduler.generate_daily_plan():
    print(f"{task.time} | {task.description} | {task.duration} min | Completed: {task.completed}")

print("\nFiltered Incomplete Tasks")
print("-" * 40)
for task in scheduler.filter_tasks(completed=False):
    print(f"{task.time} | {task.description}")

print("\nConflict Warnings")
print("-" * 40)
conflicts = scheduler.detect_conflicts()
if conflicts:
    for conflict in conflicts:
        print(conflict)
else:
    print("No conflicts found.")

print("\nMarking 'Morning walk' complete for Buddy...")
scheduler.mark_task_complete("Buddy", "Morning walk")

print("\nBuddy's Tasks After Completion")
print("-" * 40)
for task in dog.tasks:
    print(f"{task.description} | {task.time} | {task.due_date} | Completed: {task.completed}")