# PawPal+ Project Rules

## Backend Architecture Rules
1. **Strict OOP Principles**: Use classes to model real-world concepts (`Owner`, `Pet`, `Task`, `Scheduler`). Avoid unstructured dictionaries for internal data structures where a class could represent them.
2. **Task Hierarchy**: Use inheritance for different task types (e.g., `FeedingTask`, `WalkTask`, `MedicationTask`) to encapsulate specialized parameters (e.g., dosage, amount, location).
3. **Type Annotation**: Annotate all python functions and methods with appropriate type hints (using the `typing` module if necessary).
4. **Docstrings & Comments**: Add standard docstrings to all classes and methods. Do not delete existing comments unless requested.

## Scheduling Algorithmic Constraints
1. **Time Slot Constraints**: Tasks must not overlap. Write a robust conflict detection algorithm.
2. **Daily Time Budget**: The owner can set a daily time budget (e.g., in minutes). The scheduler must prioritize high-priority tasks and omit lower-priority ones if they exceed the budget.
3. **Priority Order**: High priority > Medium priority > Low priority.
4. **Availability Windows**: Support scheduling tasks within designated availability time blocks.

## CLI & Streamlit Integration
1. **CLI First**: Develop and verify the system using a CLI demo script `demo.py` and unit tests before writing/updating the Streamlit UI.
2. **Beautiful Streamlit UI**: Streamlit UI should follow high-quality design principles (using clear visual cues, icons, interactive expanders, and reasoning displays).
3. **Reasoning Explanation**: The scheduling engine must generate explanations for why tasks were scheduled, deferred, or skipped.

## Testing Guidelines
1. **Pytest Setup**: Create test suite covering scheduling, sorting, conflict detection, and edge cases.
2. **Coverage**: Ensure tests achieve high coverage of logic.
