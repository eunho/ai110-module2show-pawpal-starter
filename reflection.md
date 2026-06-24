# PawPal+ Project Reflection

## 1. System Design

**Core User Actions:**
1. **Manage Pet Profiles**: A user can add a pet with characteristics (name, species, age, weight, energy level) to keep track of individualized care needs.
2. **Define and Customize Pet Care Tasks**: A user can add or edit care tasks (e.g., feeding, walk, medication, enrichment, appointment) with specialized parameters (e.g., dosage, amount, location), duration, and priority.
3. **Generate and View an Optimized Daily Schedule**: A user can trigger the scheduler to produce a daily plan that respects availability windows and time budgets, with explanations of why tasks were scheduled, deferred, or skipped.

**a. Initial design**

- **UML Design Overview**: The design models real-world pet care concepts through clean, decoupled Python classes. It separates data representation (`Owner`, `Pet`, `Task`) from scheduling execution logic (`Scheduler`, `ScheduleResult`).
- **Classes and Responsibilities**:
  - `Owner`: Holds owner-specific configurations (daily time budget, available windows) and maintains a registry of owned `Pet` profiles.
  - `Pet`: Holds specific pet attributes (species, weight, energy level) and customized care preferences.
  - `Task` (Base Class): Models a generic care action with core scheduling constraints (duration, priority level, preferred start time, target pet, recurrence).
  - Specialized Task Subclasses (`FeedingTask`, `WalkTask`, `MedicationTask`, `EnrichmentTask`, `AppointmentTask`): Extend the base `Task` class to store specialized parameters (e.g., dosage, amount, routes, location) required for concrete activities.
  - `Scheduler`: Implements a stateless engine that sorts tasks by priority/duration, maps them onto availability windows, shifts overlapping tasks to resolve conflicts, and enforces the owner's daily time budget.
  - `ScheduleResult`: Synthesizes the output of a scheduler run, containing chronological scheduled tasks, skipped tasks with detailed reason explanations, and a step-by-step reasoning log.

**b. Design changes**

- **Did your design change during implementation?** Yes.
- **Change and Rationale**: We modified the association between `Task` and `Pet`. In the initial draft skeleton, tasks held a string key `pet_name: str`. During implementation, we replaced this with a direct object reference `pet: Pet`. This change was made to adhere to strict Object-Oriented Programming (OOP) principles, preventing scheduling bugs or data mix-ups if multiple pets share the same name. Additionally, a direct object reference allows the scheduling engine or task logs to query pet-specific metadata (like weight, age, or species) dynamically if needed for future rule enhancements.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- **What constraints does your scheduler consider?** The scheduler enforces a strict daily time budget (in minutes), respects the owner's availability time blocks, ensures tasks do not overlap, and prioritizes critical needs based on priority level (High > Medium > Low).
- **How did you decide which constraints mattered most?** Task priority level is treated as the primary constraint (High-priority tasks are scheduled first) because critical pet needs (such as medication or feeding times) cannot be skipped, whereas low-priority tasks (such as training or extra grooming) can be deferred if time is limited.

**b. Tradeoffs**

- **Describe one tradeoff your scheduler makes.** The scheduler implements a **greedy, sequential conflict resolution** strategy. It schedules tasks one-by-one in sorted priority order. When a task overlaps with a previously scheduled task, it shifts that task forward in time until a free slot is found.
- **Why is that tradeoff reasonable for this scenario?** A greedy approach is computationally efficient ($O(N \log N)$ sorting + $O(N)$ scheduling steps) and ensures instantaneous execution in the browser or terminal. While a globally optimized backtracking solver could potentially squeeze in more low-priority tasks by rearranging high-priority tasks, a greedy solver guarantees that critical high-priority items are booked at or as close to their preferred times as possible, which is the safest design for animal health.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
