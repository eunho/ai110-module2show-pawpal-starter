"""
Simplified unit tests for the PawPal+ pet care management system.
Focuses on Task Completion and Task Addition.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import datetime
from pawpal_system import Pet, WalkTask, FeedingTask, Scheduler

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


def test_scheduler_sort_by_time():
    """Verify that Scheduler.sort_by_time sorts tasks by preferred_start_time correctly."""
    pet = Pet(name="Mochi", species="Dog", age=2.0, weight=15.0, energy_level="High")
    t1 = WalkTask("Walk 1", 30, "high", datetime.time(14, 30), pet)
    t2 = WalkTask("Walk 2", 30, "high", datetime.time(8, 15), pet)
    t3 = WalkTask("Walk 3", 30, "high", datetime.time(18, 0), pet)
    
    sorted_tasks = Scheduler.sort_by_time([t1, t2, t3])
    
    assert [t.title for t in sorted_tasks] == ["Walk 2", "Walk 1", "Walk 3"]


def test_scheduler_filter_tasks():
    """Verify that Scheduler.filter_tasks correctly filters by pet name or completion status."""
    pet_mochi = Pet(name="Mochi", species="Dog", age=2.0, weight=15.0, energy_level="High")
    pet_biscuit = Pet(name="Biscuit", species="Cat", age=4.0, weight=10.0, energy_level="Low")
    
    t1 = WalkTask("Walk 1", 30, "high", datetime.time(8, 0), pet_mochi)
    t2 = WalkTask("Walk 2", 30, "high", datetime.time(9, 0), pet_biscuit)
    t3 = WalkTask("Walk 3", 30, "high", datetime.time(10, 0), pet_mochi)
    
    t1.mark_complete() # t1 completed, t2 and t3 not completed
    
    # Filter by pet name
    mochi_tasks = Scheduler.filter_tasks([t1, t2, t3], pet_name="mochi")
    assert len(mochi_tasks) == 2
    assert t1 in mochi_tasks
    assert t3 in mochi_tasks
    
    # Filter by completion status
    completed_tasks = Scheduler.filter_tasks([t1, t2, t3], is_completed=True)
    assert len(completed_tasks) == 1
    assert completed_tasks[0] == t1
    
    incomplete_tasks = Scheduler.filter_tasks([t1, t2, t3], is_completed=False)
    assert len(incomplete_tasks) == 2
    assert t2 in incomplete_tasks
    assert t3 in incomplete_tasks
    
    # Filter by both
    completed_mochi = Scheduler.filter_tasks([t1, t2, t3], pet_name="mochi", is_completed=True)
    assert len(completed_mochi) == 1
    assert completed_mochi[0] == t1


def test_scheduler_conflict_detection():
    """Verify that detect_conflict and detect_time_overlap identify overlapping schedules."""
    # Overlap checking
    assert Scheduler.detect_time_overlap(datetime.time(8, 0), 30, datetime.time(8, 15), 15) is True
    assert Scheduler.detect_time_overlap(datetime.time(8, 0), 30, datetime.time(8, 30), 10) is False
    assert Scheduler.detect_time_overlap(datetime.time(8, 0), 30, datetime.time(7, 45), 30) is True
    
    # Task conflict checking
    pet = Pet(name="Mochi", species="Dog", age=2.0, weight=15.0, energy_level="High")
    t1 = WalkTask("Morning Walk", 30, "high", datetime.time(8, 0), pet)
    t2 = WalkTask("Quick Outing", 15, "medium", datetime.time(8, 15), pet)
    t3 = WalkTask("Afternoon Walk", 30, "low", datetime.time(14, 0), pet)
    
    assert Scheduler.detect_conflict(t1, t2) is True
    assert Scheduler.detect_conflict(t1, t3) is False

    # Verify duplicate times (exact same start time) are flagged
    t_dup1 = WalkTask("Walk A", 30, "high", datetime.time(10, 0), pet)
    t_dup2 = WalkTask("Walk B", 30, "medium", datetime.time(10, 0), pet)
    assert Scheduler.detect_conflict(t_dup1, t_dup2) is True

    # Verify Scheduler.check_conflicts returns warnings for overlapping/duplicate tasks
    warnings = Scheduler.check_conflicts([t_dup1, t_dup2])
    assert len(warnings) == 1
    assert "Conflict detected between 'Walk A'" in warnings[0]
    assert "and 'Walk B'" in warnings[0]


def test_scheduler_get_tasks_for_date():
    """Verify that get_tasks_for_date handles daily, weekly, and one-off task recurrences correctly."""
    pet = Pet(name="Mochi", species="Dog", age=2.0, weight=15.0, energy_level="High")
    
    # Let's say today is a Monday (e.g. 2026-06-22 is a Monday)
    monday = datetime.date(2026, 6, 22)
    tuesday = datetime.date(2026, 6, 23)
    next_monday = datetime.date(2026, 6, 29)
    
    # Daily task
    t_daily = WalkTask("Daily Walk", 30, "high", datetime.time(8, 0), pet, recurrence="daily")
    t_daily.created_date = monday
    
    # Weekly task created on Monday
    t_weekly = WalkTask("Weekly Class", 60, "medium", datetime.time(10, 0), pet, recurrence="weekly")
    t_weekly.created_date = monday
    
    # One-off task created on Monday
    t_oneoff = WalkTask("One-off Vet", 45, "high", datetime.time(14, 0), pet, recurrence="none")
    t_oneoff.created_date = monday
    
    tasks = [t_daily, t_weekly, t_oneoff]
    
    # Check tasks for Monday (same day as created)
    monday_tasks = Scheduler.get_tasks_for_date(tasks, monday)
    assert len(monday_tasks) == 3
    assert t_daily in monday_tasks
    assert t_weekly in monday_tasks
    assert t_oneoff in monday_tasks
    
    # Check tasks for Tuesday (different day, different weekday)
    tuesday_tasks = Scheduler.get_tasks_for_date(tasks, tuesday)
    assert len(tuesday_tasks) == 1
    assert tuesday_tasks[0] == t_daily # Only daily task
    
    # Check tasks for Next Monday (different week, same weekday)
    next_monday_tasks = Scheduler.get_tasks_for_date(tasks, next_monday)
    assert len(next_monday_tasks) == 2
    assert t_daily in next_monday_tasks
    assert t_weekly in next_monday_tasks
    assert t_oneoff not in next_monday_tasks # oneoff was only for original Monday


def test_auto_recurrence_on_completion():
    """Verify that completing a daily or weekly task spawns a new instance for the next occurrence."""
    pet = Pet(name="Mochi", species="Dog", age=2.0, weight=15.0, energy_level="High")
    
    # 1. Test Daily Task auto-recurrence
    t_daily = WalkTask(
        title="Daily Walk",
        duration=30,
        priority="high",
        preferred_start_time=datetime.time(8, 0),
        pet=pet,
        recurrence="daily",
        distance=1.0,
        route="Park"
    )
    t_daily.created_date = datetime.date.today()
    
    assert len(pet.tasks) == 1
    
    t_daily.mark_complete()
    assert t_daily.is_completed is True
    
    # Check that a new task was created and registered with the pet
    assert len(pet.tasks) == 2
    new_daily = [t for t in pet.tasks if t != t_daily][0]
    assert new_daily.title == "Daily Walk"
    assert new_daily.is_completed is False
    assert new_daily.created_date == datetime.date.today() + datetime.timedelta(days=1)
    assert new_daily.distance == 1.0 # Subclass attributes are preserved
    
    # 2. Test Weekly Task auto-recurrence
    t_weekly = WalkTask(
        title="Weekly Agility",
        duration=45,
        priority="medium",
        preferred_start_time=datetime.time(10, 0),
        pet=pet,
        recurrence="weekly",
        distance=0.5,
        route="Training Center"
    )
    t_weekly.created_date = datetime.date.today()
    
    # Pet now has t_daily, new_daily, and t_weekly
    assert len(pet.tasks) == 3
    
    t_weekly.mark_complete()
    assert t_weekly.is_completed is True
    
    # Pet now has t_daily, new_daily, t_weekly, and new_weekly
    assert len(pet.tasks) == 4
    new_weekly = [t for t in pet.tasks if t not in (t_daily, new_daily, t_weekly)][0]
    assert new_weekly.title == "Weekly Agility"
    assert new_weekly.is_completed is False
    assert new_weekly.created_date == datetime.date.today() + datetime.timedelta(weeks=1)
    assert new_weekly.route == "Training Center"
    
    # 3. Test One-off (none) task does NOT auto-recur
    t_none = WalkTask(
        title="One-off Vet Visit",
        duration=60,
        priority="high",
        preferred_start_time=datetime.time(11, 0),
        pet=pet,
        recurrence="none"
    )
    assert len(pet.tasks) == 5
    t_none.mark_complete()
    assert t_none.is_completed is True
    assert len(pet.tasks) == 5 # No new task created
