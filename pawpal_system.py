"""
PawPal+ Core System Logic Layer - Skeleton
Contains OOP classes representing Owners, Pets, Tasks (with inheritance), 
and the Scheduler engine. Uses Python Dataclasses where appropriate to keep data structures clean.
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
        pass


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
        self.availability_windows: List[Tuple[datetime.time, datetime.time]] = availability_windows or [
            (datetime.time(7, 0), datetime.time(22, 0))
        ]
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """
        Associates a new pet with the owner.
        """
        pass

    def remove_pet(self, pet_name: str) -> None:
        """
        Removes a pet from the owner's list by name.
        """
        pass

    def set_time_budget(self, minutes: int) -> None:
        """
        Updates the daily time budget.
        """
        pass

    def add_availability_window(self, start: datetime.time, end: datetime.time) -> None:
        """
        Adds a care availability window.
        """
        pass

    def clear_availability_windows(self) -> None:
        """
        Clears all availability windows so new ones can be set.
        """
        pass


@dataclass
class Task:
    """
    Base class representing a generic care task with scheduling constraints.
    """
    title: str
    duration: int  # in minutes
    priority: str  # "high", "medium", "low"
    preferred_start_time: datetime.time
    pet_name: str
    recurrence: str = "daily"
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def get_category(self) -> str:
        """
        Returns the category/type of the task. Subclasses override this.
        """
        return "general"


@dataclass
class FeedingTask(Task):
    """
    Specialized task for pet feeding.
    """
    food_type: str = "Kibble"
    amount_cups: float = 1.0

    def get_category(self) -> str:
        return "feeding"


@dataclass
class WalkTask(Task):
    """
    Specialized task for dog walks.
    """
    distance: float = 1.0
    route: str = "Neighborhood Route"

    def get_category(self) -> str:
        return "walk"


@dataclass
class MedicationTask(Task):
    """
    Specialized task for administering meds.
    """
    med_name: str = ""
    dosage: str = ""

    def get_category(self) -> str:
        return "medication"


@dataclass
class EnrichmentTask(Task):
    """
    Specialized task for mental stimulation or training.
    """
    activity_type: str = "Puzzle Toy"

    def get_category(self) -> str:
        return "enrichment"


@dataclass
class AppointmentTask(Task):
    """
    Specialized task for vet or groomer appointments.
    """
    location: str = "Vet Clinic"
    notes: str = ""

    def get_category(self) -> str:
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
        return 0

    @staticmethod
    def minutes_to_time(m: int) -> datetime.time:
        """Helper to convert minutes since midnight to datetime.time."""
        return datetime.time(0, 0)

    def generate_daily_schedule(self, owner: Owner, tasks: List[Task]) -> ScheduleResult:
        """
        Generates an optimized non-overlapping daily schedule based on priority,
        availability, and time budget.
        """
        return ScheduleResult()
