"""
PawPal+ Core System Logic Layer
Contains OOP classes representing Owners, Pets, Tasks (with inheritance), 
and the Scheduler engine for conflict detection, sorting, and budgeting.
"""

from dataclasses import dataclass, field
import datetime
from typing import List, Tuple, Dict, Any, Optional
import uuid

@dataclass
class Pet:
    """
    Represents a pet and their individual profile information.
    """
    name: str
    species: str
    age: float
    weight: float
    energy_level: str
    preferences: Dict[str, Any] = field(default_factory=dict)
    # List of tasks associated with this pet.
    # We set repr=False and compare=False to avoid infinite recursion.
    tasks: List['Task'] = field(default_factory=list, init=False, repr=False, compare=False)

    def add_task(self, task: 'Task') -> None:
        """
        Adds a task to the pet's task list.
        """
        if not any(t.task_id == task.task_id for t in self.tasks):
            self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """
        Removes a task from the pet's task list by ID.
        """
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

    def update_profile(
        self,
        species: Optional[str] = None,
        age: Optional[float] = None,
        weight: Optional[float] = None,
        energy_level: Optional[str] = None,
        preferences: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Updates pet profile attributes.
        """
        if species:
            self.species = species.lower()
        if age is not None:
            self.age = age
        if weight is not None:
            self.weight = weight
        if energy_level:
            self.energy_level = energy_level.lower()
        if preferences is not None:
            self.preferences.update(preferences)

    def __repr__(self) -> str:
        """Returns a string representation of the Pet."""
        return f"Pet(name={self.name}, species={self.species}, age={self.age}, energy={self.energy_level})"


class Owner:
    """
    Represents the owner, holding their daily budget constraints,
    availability windows, and their registered pets.
    """
    def __init__(
        self,
        name: str,
        daily_time_budget: int = 120,
        availability_windows: Optional[List[Tuple[datetime.time, datetime.time]]] = None
    ) -> None:
        self.name: str = name
        self.daily_time_budget: int = daily_time_budget  # in minutes
        # Default availability: 07:00 to 22:00
        self.availability_windows: List[Tuple[datetime.time, datetime.time]] = availability_windows or [
            (datetime.time(7, 0), datetime.time(22, 0))
        ]
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """
        Associates a new pet with the owner.
        """
        if not any(p.name == pet.name for p in self.pets):
            self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """
        Removes a pet from the owner's list by name.
        """
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_all_tasks(self) -> List['Task']:
        """
        Retrieves all tasks across all pets owned by this owner.
        """
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def set_time_budget(self, minutes: int) -> None:
        """
        Updates the daily time budget.
        """
        self.daily_time_budget = minutes

    def add_availability_window(self, start: datetime.time, end: datetime.time) -> None:
        """
        Adds a care availability window.
        """
        if start < end:
            self.availability_windows.append((start, end))
            # Sort windows by start time
            self.availability_windows.sort(key=lambda x: x[0])

    def clear_availability_windows(self) -> None:
        """
        Clears all availability windows so new ones can be set.
        """
        self.availability_windows = []

    def __repr__(self) -> str:
        """Returns a string representation of the Owner."""
        return f"Owner(name={self.name}, budget={self.daily_time_budget}m, pets={[p.name for p in self.pets]})"


@dataclass
class Task:
    """
    Base class representing a generic care task with scheduling constraints.
    """
    title: str
    duration: int  # in minutes
    priority: str  # "high", "medium", "low"
    preferred_start_time: datetime.time
    pet: Pet  # Direct association to a Pet object
    recurrence: str = "daily"
    is_completed: bool = False
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_date: datetime.date = field(default_factory=datetime.date.today)

    def __post_init__(self) -> None:
        """
        Automatically register this task with the associated Pet.
        """
        if self.pet:
            self.pet.add_task(self)

    def get_category(self) -> str:
        """
        Returns the category/type of the task. Subclasses override this.
        """
        return "general"

    def mark_complete(self) -> None:
        """
        Marks the task as completed.
        If the task is daily or weekly, automatically schedules the next occurrence relative to today.
        """
        if not self.is_completed:
            self.is_completed = True
            if self.recurrence in ("daily", "weekly"):
                from dataclasses import replace
                today_date = datetime.date.today()
                if self.recurrence == "daily":
                    next_date = today_date + datetime.timedelta(days=1)
                else:  # weekly
                    next_date = today_date + datetime.timedelta(weeks=1)
                
                # Create new instance for the next occurrence
                replace(
                    self,
                    is_completed=False,
                    created_date=next_date,
                    task_id=str(uuid.uuid4())
                )
                
                # Stop this completed task instance from continuing to recur
                self.recurrence = "none"

    def __repr__(self) -> str:
        """Returns a string representation of the Task."""
        return f"Task(title={self.title}, pet={self.pet.name}, duration={self.duration}m, priority={self.priority})"


@dataclass
class FeedingTask(Task):
    """
    Specialized task for pet feeding.
    """
    food_type: str = "Kibble"
    amount_cups: float = 1.0

    def get_category(self) -> str:
        """Returns the feeding category."""
        return "feeding"


@dataclass
class WalkTask(Task):
    """
    Specialized task for dog walks.
    """
    distance: float = 1.0
    route: str = "Neighborhood Route"

    def get_category(self) -> str:
        """Returns the walk category."""
        return "walk"


@dataclass
class MedicationTask(Task):
    """
    Specialized task for administering meds.
    """
    med_name: str = ""
    dosage: str = ""

    def get_category(self) -> str:
        """Returns the medication category."""
        return "medication"


@dataclass
class EnrichmentTask(Task):
    """
    Specialized task for mental stimulation or training.
    """
    activity_type: str = "Puzzle Toy"

    def get_category(self) -> str:
        """Returns the enrichment category."""
        return "enrichment"


@dataclass
class AppointmentTask(Task):
    """
    Specialized task for vet or groomer appointments.
    """
    location: str = "Vet Clinic"
    notes: str = ""

    def get_category(self) -> str:
        """Returns the appointment category."""
        return "appointment"


class ScheduleResult:
    """
    Holds the output of a scheduling run, including scheduled events,
    skipped tasks, total time spent, and explanations.
    """
    def __init__(self) -> None:
        # List of dicts: {"start_time": datetime.time, "end_time": datetime.time, "task": Task}
        self.scheduled_tasks: List[Dict[str, Any]] = []
        # List of tuples: (Task, reason_for_skipping)
        self.skipped_tasks: List[Tuple[Task, str]] = []
        self.total_time_used: int = 0
        self.explanation: List[str] = []


class Scheduler:
    """
    State-free scheduling engine that builds daily care plans
    respecting priorities, time budgets, availability windows, and overlaps.
    """

    @staticmethod
    def time_to_minutes(t: datetime.time) -> int:
        """Helper to convert datetime.time to minutes since midnight."""
        return t.hour * 60 + t.minute

    @staticmethod
    def minutes_to_time(m: int) -> datetime.time:
        """Helper to convert minutes since midnight to datetime.time."""
        m = m % 1440
        return datetime.time(hour=m // 60, minute=m % 60)

    @staticmethod
    def sort_by_time(tasks: List[Task]) -> List[Task]:
        """
        Sorts a list of Task objects by their preferred start time.
        Uses a lambda function as a key to sort strings in "HH:MM" format.

        Args:
            tasks (List[Task]): The list of Task objects to be sorted.

        Returns:
            List[Task]: A new list containing the sorted Task objects.
        """
        return sorted(tasks, key=lambda t: t.preferred_start_time.strftime("%H:%M"))

    @staticmethod
    def filter_tasks(
        tasks: List[Task],
        pet_name: Optional[str] = None,
        is_completed: Optional[bool] = None
    ) -> List[Task]:
        """
        Filters tasks by completion status or pet name.

        Args:
            tasks (List[Task]): The list of tasks to filter.
            pet_name (Optional[str], optional): The pet's name to filter by. Defaults to None.
            is_completed (Optional[bool], optional): The completion status to filter by. Defaults to None.

        Returns:
            List[Task]: A filtered list containing only matching tasks.
        """
        filtered = tasks
        if pet_name is not None:
            filtered = [t for t in filtered if t.pet.name.lower() == pet_name.lower()]
        if is_completed is not None:
            filtered = [t for t in filtered if t.is_completed == is_completed]
        return filtered

    @staticmethod
    def detect_time_overlap(start1: datetime.time, duration1: int, start2: datetime.time, duration2: int) -> bool:
        """
        Checks if two time periods overlap.

        Args:
            start1 (datetime.time): The preferred start time of the first period.
            duration1 (int): The duration of the first period in minutes.
            start2 (datetime.time): The preferred start time of the second period.
            duration2 (int): The duration of the second period in minutes.

        Returns:
            bool: True if the periods overlap, False otherwise.
        """
        s1 = Scheduler.time_to_minutes(start1)
        e1 = s1 + duration1
        s2 = Scheduler.time_to_minutes(start2)
        e2 = s2 + duration2
        return max(s1, s2) < min(e1, e2)

    @staticmethod
    def detect_conflict(task1: Task, task2: Task) -> bool:
        """
        Checks if two tasks have overlapping times based on their preferred start times and durations.

        Args:
            task1 (Task): The first Task object.
            task2 (Task): The second Task object.

        Returns:
            bool: True if the tasks overlap in time, False otherwise.
        """
        return Scheduler.detect_time_overlap(
            task1.preferred_start_time, task1.duration,
            task2.preferred_start_time, task2.duration
        )

    @staticmethod
    def get_tasks_for_date(tasks: List[Task], date: datetime.date) -> List[Task]:
        """
        Filters and returns the tasks that are active on a specific date.
        - 'daily': Active every day.
        - 'weekly': Active on the same day of the week as they were created.
        - 'none': Active only on the exact created_date.

        Args:
            tasks (List[Task]): The full list of tasks.
            date (datetime.date): The target date to filter tasks for.

        Returns:
            List[Task]: A list containing only tasks active on the target date.
        """
        active_tasks = []
        for task in tasks:
            created = getattr(task, "created_date", date)
            # If the task starts in the future, it is not active on this date
            if created > date:
                continue
            if task.recurrence == "daily":
                active_tasks.append(task)
            elif task.recurrence == "weekly":
                if created.weekday() == date.weekday():
                    active_tasks.append(task)
            elif task.recurrence == "none":
                if created == date:
                    active_tasks.append(task)
        return active_tasks

    @staticmethod
    def reset_completions(tasks: List[Task]) -> None:
        """
        Resets the completion status of all tasks to False.
        Useful when starting a new day's schedule.

        Args:
            tasks (List[Task]): The list of tasks to reset.
        """
        for task in tasks:
            task.is_completed = False

    @staticmethod
    def check_conflicts(tasks: List[Task]) -> List[str]:
        """
        Performs a lightweight conflict check on a list of tasks based on their preferred start times and durations.
        Returns a list of warning messages for any overlapping tasks.

        Args:
            tasks (List[Task]): The list of tasks to check.

        Returns:
            List[str]: A list of warning message strings for each detected conflict.
        """
        warnings = []
        sorted_tasks = Scheduler.sort_by_time(tasks)
        for i in range(len(sorted_tasks)):
            for j in range(i + 1, len(sorted_tasks)):
                t1 = sorted_tasks[i]
                t2 = sorted_tasks[j]
                if Scheduler.detect_conflict(t1, t2):
                    warnings.append(
                        f"⚠️ WARNING: Conflict detected between '{t1.title}' for {t1.pet.name} "
                        f"and '{t2.title}' for {t2.pet.name} around {t1.preferred_start_time.strftime('%H:%M')}."
                    )
        return warnings

    def generate_daily_schedule(self, owner: Owner, tasks: Optional[List[Task]] = None) -> ScheduleResult:
        """
        Generates an optimized non-overlapping daily schedule based on priority,
        availability, and time budget.
        """
        result = ScheduleResult()
        
        # If tasks is not explicitly provided, retrieve tasks active for today
        if tasks is None:
            tasks = self.get_tasks_for_date(owner.get_all_tasks(), datetime.date.today())
        
        if not tasks:
            result.explanation.append("No tasks provided or found for scheduling.")
            return result

        # Map priorities to numeric values for sorting
        priority_map = {"high": 3, "medium": 2, "low": 1}

        # Sort tasks:
        # 1. Priority (High -> Low)
        # 2. Preferred start time (Earlier -> Later)
        # 3. Duration (Shorter -> Longer)
        sorted_tasks = sorted(
            tasks,
            key=lambda t: (
                -priority_map.get(t.priority, 0),
                self.time_to_minutes(t.preferred_start_time),
                t.duration
            )
        )

        # Convert owner availability windows to minutes since midnight
        avail_mins: List[Tuple[int, int]] = [
            (self.time_to_minutes(start), self.time_to_minutes(end))
            for start, end in owner.availability_windows
        ]

        # Scheduled task intervals: list of tuples (start_min, end_min, task)
        scheduled_intervals: List[Tuple[int, int, Task]] = []
        total_time: int = 0

        for task in sorted_tasks:
            # Check Daily Budget Limit
            if total_time + task.duration > owner.daily_time_budget:
                remaining = owner.daily_time_budget - total_time
                reason = f"Exceeds daily time budget (requires {task.duration}m, only {remaining}m remaining of {owner.daily_time_budget}m budget)."
                result.skipped_tasks.append((task, reason))
                result.explanation.append(f"❌ Skipped '{task.title}' for {task.pet.name}: {reason}")
                continue

            preferred_start_min = self.time_to_minutes(task.preferred_start_time)
            scheduled_start_min: Optional[int] = None

            # Conflict Resolution: search for a valid slot starting from preferred_start_min forward
            # Search window extends from the preferred time up to the end of the day (1440m)
            # We increment by 5-minute steps
            for start_candidate in range(preferred_start_min, 1440, 5):
                end_candidate = start_candidate + task.duration

                # 1. Verify candidate is within owner's availability windows
                within_availability = False
                for w_start, w_end in avail_mins:
                    if w_start <= start_candidate and end_candidate <= w_end:
                        within_availability = True
                        break

                if not within_availability:
                    continue

                # 2. Verify candidate does not overlap with already scheduled tasks
                overlap = False
                for s_start, s_end, s_task in scheduled_intervals:
                    s_start_time = self.minutes_to_time(s_start)
                    candidate_time = self.minutes_to_time(start_candidate)
                    if self.detect_time_overlap(candidate_time, task.duration, s_start_time, s_task.duration):
                        overlap = True
                        break

                if not overlap:
                    scheduled_start_min = start_candidate
                    break

            if scheduled_start_min is not None:
                # Successfully scheduled!
                scheduled_end_min = scheduled_start_min + task.duration
                scheduled_intervals.append((scheduled_start_min, scheduled_end_min, task))
                total_time += task.duration

                start_time = self.minutes_to_time(scheduled_start_min)
                end_time = self.minutes_to_time(scheduled_end_min)

                result.scheduled_tasks.append({
                    "start_time": start_time,
                    "end_time": end_time,
                    "task": task
                })

                # Determine if it was shifted
                if scheduled_start_min == preferred_start_min:
                    result.explanation.append(
                        f"✅ Scheduled '{task.title}' for {task.pet.name} at {start_time.strftime('%H:%M')} "
                        f"(Duration: {task.duration}m, Priority: {task.priority.upper()})."
                    )
                else:
                    orig_time = task.preferred_start_time.strftime('%H:%M')
                    result.explanation.append(
                        f"🔄 Scheduled '{task.title}' for {task.pet.name} at {start_time.strftime('%H:%M')} "
                        f"(originally preferred {orig_time}, shifted due to scheduling conflict. "
                        f"Duration: {task.duration}m, Priority: {task.priority.upper()})."
                    )
            else:
                # Could not find a slot
                reason = "Could not find a conflict-free slot within owner availability windows."
                result.skipped_tasks.append((task, reason))
                result.explanation.append(f"❌ Skipped '{task.title}' for {task.pet.name}: {reason}")

        # Store total time used
        result.total_time_used = total_time

        # Finally, sort scheduled tasks by their start time for display
        result.scheduled_tasks.sort(key=lambda x: x["start_time"])

        return result
