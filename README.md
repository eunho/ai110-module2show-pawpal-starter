# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Here is the terminal output showing a generated daily care plan for Mochi and Biscuit, including conflict resolution and budget warnings:

```
🐾 Running PawPal+ Schedule Generator...

===============================================================================================
📅 TODAY'S PET CARE TIMELINE FOR JORDAN'S HOUSEHOLD
===============================================================================================
TIME SLOT     | PET        | TYPE | TASK TITLE                | PRIORITY | TASK DETAILS
-----------------------------------------------------------------------------------------------
08:00 - 08:30 | Mochi      | 🦮    | Morning Walk              | HIGH     | 1.5 mi, route: Greenlake Loop
08:30 - 08:40 | Biscuit    | 🦴    | Breakfast Feeding         | HIGH     | 0.5 cups of Canned Salmon
09:00 - 09:05 | Mochi      | 💊    | Joint Supplement          | MEDIUM   | Dosage: 1 chewable of Cosequin
14:00 - 14:15 | Biscuit    | 🎾    | Laser Toy Play            | LOW      | Activity: Laser chasing
===============================================================================================

❌ DEFERRED/SKIPPED TASKS:
 • 🎾 Agility Park Training for Mochi (80m) — Reason: Exceeds daily time budget (requires 80m, only 60m remaining of 120m budget).
===============================================================================================
📊 Daily Time Budget: [██████████░░░░░░░░░░] 60/120 mins (50.0%)
===============================================================================================
```

## 🧪 Testing PawPal+

To verify the correctness of the PawPal+ scheduling logic and pet models, run the following command:

```bash
python -m pytest
```

### What the Tests Cover
Our test suite in `tests/test_pawpal.py` validates the core components of the scheduling engine:
- **Task Completion Status**: Asserts that `mark_complete()` successfully changes task completion states.
- **Task Auto-Registration**: Confirms that when a new task is instantiated, it is automatically registered to its associated pet.
- **Chronological Sorting**: Ensures tasks are correctly sorted by preferred start times.
- **Task Filtering**: Verifies filtering tasks case-insensitively by pet name and/or completion status.
- **Conflict & Overlap Detection**: Verifies that overlapping task periods and duplicate times are correctly detected, and warning notifications are generated.
- **Date-Based Task Filtering**: Validates the retrieval of active tasks based on daily, weekly, or one-off recurrence rules for a target date.
- **Auto-Recurrence Spawning**: Asserts that marking recurring tasks (daily/weekly) as complete automatically registers a new task instance for the next occurrence, preserving subclass attributes.

### Successful Test Run Output

```text
============================= test session starts ==============================
platform darwin -- Python 3.13.13, pytest-9.0.3, pluggy-1.6.0
rootdir: /Users/eunho/Documents/codepath/ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 7 items

tests/test_pawpal.py .......                                             [100%]

============================== 7 passed in 0.01s ===============================
```

### Confidence Level
**Confidence Level**: ⭐⭐⭐⭐⭐ (5/5 stars)
- **Rationale**: The core scheduling logic is fully decoupled and mathematically verified by deterministic unit tests covering the edge cases of duplicate preferred start times, daily recurrence, weekly recurrence, and complex filtering.

## 📐 Smarter Scheduling

This system includes algorithmic features to manage the scheduling, validation, and execution of pet care tasks:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| **Task sorting** | `Scheduler.sort_by_time(tasks)` | Sorts task lists chronologically by preferred start time using a lambda function as a key to sort "HH:MM" time strings. |
| **Filtering** | `Scheduler.filter_tasks(tasks, pet_name, is_completed)` | Filters a list of tasks case-insensitively by pet name and/or completion status. |
| **Conflict handling** | `Scheduler.detect_time_overlap(s1, d1, s2, d2)`<br>`Scheduler.detect_conflict(t1, t2)`<br>`Scheduler.check_conflicts(tasks)` | Checks for overlapping time slots, resolves conflicts by shifting tasks forward, and offers a lightweight validation check returning non-crashing warnings. |
| **Recurring tasks** | `Scheduler.get_tasks_for_date(tasks, date)`<br>`Task.mark_complete()` | Filters active tasks based on daily, weekly (weekday-matching), or one-off recurrence rules. Automatically schedules next occurrences on task completion. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
