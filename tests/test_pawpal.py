"""
Simplified unit tests for the PawPal+ pet care management system.
Focuses on Task Completion and Task Addition.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import datetime
from pawpal_system import Pet, WalkTask, FeedingTask

def test_task_completion():
    """Verify that calling mark_complete() actually changes the task's status."""
    pet = Pet(name="Mochi", species="Dog", age=2.0, weight=15.0, energy_level="High")
    task = WalkTask(
        title="Morning Walk",
        duration=30,
        priority="high",
        preferred_start_time=datetime.time(8, 0),
        pet=pet,
        distance=1.0,
        route="Park"
    )
    
    # Assert initial state
    assert task.is_completed is False
    
    # Mark complete and assert status changed
    task.mark_complete()
    assert task.is_completed is True


def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Biscuit", species="Cat", age=4.0, weight=10.0, energy_level="Low")
    
    # Pet should start with 0 tasks
    assert len(pet.tasks) == 0
    
    # Adding one task (instantiation with auto-registration)
    task1 = FeedingTask(
        title="Breakfast",
        duration=10,
        priority="high",
        preferred_start_time=datetime.time(8, 0),
        pet=pet,
        food_type="Salmon",
        amount_cups=0.5
    )
    assert len(pet.tasks) == 1
    assert pet.tasks[0] == task1
    
    # Adding a second task
    task2 = FeedingTask(
        title="Dinner",
        duration=10,
        priority="high",
        preferred_start_time=datetime.time(18, 0),
        pet=pet,
        food_type="Kibble",
        amount_cups=0.5
    )
    assert len(pet.tasks) == 2
    assert task2 in pet.tasks
