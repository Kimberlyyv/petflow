from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date, timedelta


@dataclass
class Task:
    description: str
    duration: int
    priority: int
    time: str
    frequency: str
    due_date: date
    completed: bool = False

    def mark_complete(self) -> Optional["Task"]:
        """Mark the task as complete and create the next recurring task if needed."""
        self.completed = True

        if self.frequency.lower() == "daily":
            return Task(
                description=self.description,
                duration=self.duration,
                priority=self.priority,
                time=self.time,
                frequency=self.frequency,
                due_date=self.due_date + timedelta(days=1),
            )
        elif self.frequency.lower() == "weekly":
            return Task(
                description=self.description,
                duration=self.duration,
                priority=self.priority,
                time=self.time,
                frequency=self.frequency,
                due_date=self.due_date + timedelta(weeks=1),
            )

        return None

    def update_task(self, description: str, duration: int, priority: int, time: str, frequency: str) -> None:
        """Update the task details."""
        self.description = description
        self.duration = duration
        self.priority = priority
        self.time = time
        self.frequency = frequency


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the pet."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for the pet."""
        return self.tasks


@dataclass
class Owner:
    name: str
    available_time: int
    preferences: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def sort_by_time(self) -> List[Task]:
        """Return tasks sorted by time."""
        return sorted(self.get_all_tasks(), key=lambda task: task.time)

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filter tasks by completion status or pet name."""
        filtered = []

        for pet in self.owner.pets:
            for task in pet.tasks:
                if completed is not None and task.completed != completed:
                    continue
                if pet_name is not None and pet.name.lower() != pet_name.lower():
                    continue
                filtered.append(task)

        return filtered

    def generate_daily_plan(self) -> List[Task]:
        """Generate a daily plan sorted by time and limited by available time."""
        sorted_tasks = self.sort_by_time()
        selected_tasks = []
        total_time = 0

        for task in sorted_tasks:
            if not task.completed and total_time + task.duration <= self.owner.available_time:
                selected_tasks.append(task)
                total_time += task.duration

        return selected_tasks

    def mark_task_complete(self, pet_name: str, task_description: str) -> None:
        """Mark a task complete and add the next recurring version if needed."""
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                for task in pet.tasks:
                    if task.description.lower() == task_description.lower() and not task.completed:
                        new_task = task.mark_complete()
                        if new_task:
                            pet.add_task(new_task)
                        return

    def detect_conflicts(self) -> List[str]:
        """Detect tasks that are scheduled at the same time and explain the conflict."""
        seen_times = {}
        conflicts = []

        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.time in seen_times:
                    first_task = seen_times[task.time]

                    conflicts.append(
                        f"Schedule conflict at {task.time}: "
                        f"'{first_task['description']}' for {first_task['pet_name']} and "
                        f"'{task.description}' for {pet.name} are planned at the same time. "
                        f"Consider moving one task to a different time."
                    )
                else:
                    seen_times[task.time] = {
                        "description": task.description,
                        "pet_name": pet.name
                    }

        return conflicts