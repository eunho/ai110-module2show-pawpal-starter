"""
PawPal+ CLI Testing Ground
Instantiates Owner, two Pets, adds tasks at different times, 
and prints an optimized, beautiful ASCII schedule to the terminal.
"""

import datetime
from pawpal_system import Owner, Pet, WalkTask, FeedingTask, MedicationTask, EnrichmentTask, Scheduler

def get_category_emoji(category: str) -> str:
    """Helper to return an emoji icon representing the task category."""
    emojis = {
        "feeding": "🦴",
        "walk": "🦮",
        "medication": "💊",
        "enrichment": "🎾",
        "appointment": "🏥",
        "general": "📋"
    }
    return emojis.get(category, "📋")

def print_styled_schedule(owner: Owner, result) -> None:
    """Prints a highly readable, aligned ASCII schedule with a budget indicator."""
    print("=" * 95)
    print(f"📅 TODAY'S PET CARE TIMELINE FOR {owner.name.upper()}'S HOUSEHOLD")
    print("=" * 95)
    
    # Header format
    header_fmt = "{:<13} | {:<10} | {:<4} | {:<25} | {:<8} | {}"
    print(header_fmt.format("TIME SLOT", "PET", "TYPE", "TASK TITLE", "PRIORITY", "TASK DETAILS"))
    print("-" * 95)
    
    # List scheduled tasks
    if not result.scheduled_tasks:
        print("No tasks scheduled for today.")
    else:
        for item in result.scheduled_tasks:
            start_str = item["start_time"].strftime("%H:%M")
            end_str = item["end_time"].strftime("%H:%M")
            time_slot = f"{start_str} - {end_str}"
            
            task = item["task"]
            pet_name = task.pet.name
            category = task.get_category()
            emoji = get_category_emoji(category)
            
            # Extract category-specific details via polymorphism / type check
            details = ""
            if isinstance(task, WalkTask):
                details = f"{task.distance} mi, route: {task.route}"
            elif isinstance(task, FeedingTask):
                details = f"{task.amount_cups} cups of {task.food_type}"
            elif isinstance(task, MedicationTask):
                details = f"Dosage: {task.dosage} of {task.med_name}"
            elif isinstance(task, EnrichmentTask):
                details = f"Activity: {task.activity_type}"
            
            print(header_fmt.format(
                time_slot, 
                pet_name, 
                emoji, 
                task.title, 
                task.priority.upper(), 
                details
            ))
            
    print("=" * 95)
    
    # Skipped Tasks section
    if result.skipped_tasks:
        print("\n❌ DEFERRED/SKIPPED TASKS:")
        for task, reason in result.skipped_tasks:
            emoji = get_category_emoji(task.get_category())
            print(f" • {emoji} {task.title} for {task.pet.name} ({task.duration}m) — Reason: {reason}")
        print("=" * 95)

    # Budget progress bar visualization
    budget = owner.daily_time_budget
    used = result.total_time_used
    pct = min(used / budget if budget > 0 else 0.0, 1.0)
    bar_len = 20
    filled_len = int(round(bar_len * pct))
    bar = "█" * filled_len + "░" * (bar_len - filled_len)
    
    print(f"📊 Daily Time Budget: [{bar}] {used}/{budget} mins ({pct*100:.1f}%)")
    print("=" * 95)


def main():
    print("🐾 Running PawPal+ Schedule Generator...\n")

    # 1. Create an Owner
    owner = Owner(name="Jordan", daily_time_budget=120)

    # 2. Create two Pets and register them to Owner
    mochi = Pet(name="Mochi", species="Dog", age=2.5, weight=15.0, energy_level="High")
    biscuit = Pet(name="Biscuit", species="Cat", age=4.0, weight=10.0, energy_level="Low")
    
    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    # 3. Create multiple Tasks completely out of order
    # Low Priority - 16:00
    t5 = EnrichmentTask(
        title="Agility Park Training",
        duration=80,
        priority="low",
        preferred_start_time=datetime.time(16, 0),
        pet=mochi,
        activity_type="Obstacle run"
    )

    # Low Priority - 14:00
    t4 = EnrichmentTask(
        title="Laser Toy Play",
        duration=15,
        priority="low",
        preferred_start_time=datetime.time(14, 0),
        pet=biscuit,
        activity_type="Laser chasing"
    )

    # Medium Priority - 09:00 (Marked completed to demonstrate status filter)
    t3 = MedicationTask(
        title="Joint Supplement",
        duration=5,
        priority="medium",
        preferred_start_time=datetime.time(9, 0),
        pet=mochi,
        med_name="Cosequin",
        dosage="1 chewable"
    )
    t3.mark_complete()

    # Conflicting Low Priority task - also at 09:00
    t3_conflict = FeedingTask(
        title="Morning Snack",
        duration=15,
        priority="low",
        preferred_start_time=datetime.time(9, 0),
        pet=biscuit,
        food_type="Tuna Treat",
        amount_cups=0.25
    )

    # High Priority - 08:00
    t1 = WalkTask(
        title="Morning Walk",
        duration=30,
        priority="high",
        preferred_start_time=datetime.time(8, 0),
        pet=mochi,
        distance=1.5,
        route="Greenlake Loop"
    )
    
    # High Priority - 08:30
    t2 = FeedingTask(
        title="Breakfast Feeding",
        duration=10,
        priority="high",
        preferred_start_time=datetime.time(8, 30),
        pet=biscuit,
        food_type="Canned Salmon",
        amount_cups=0.5
    )

    # 4. Generate and print schedule
    scheduler = Scheduler()
    result = scheduler.generate_daily_schedule(owner)
    
    print_styled_schedule(owner, result)

    print("\n" + "=" * 95)
    print("🧪 DEMONSTRATING NEW SMART ALGORITHMS:")
    print("=" * 95)

    # A. Sorting tasks by time using Scheduler.sort_by_time()
    all_raw_tasks = owner.get_all_tasks()
    sorted_by_time = Scheduler.sort_by_time(all_raw_tasks)
    print("\n⏰ 1. Tasks sorted chronologically via Scheduler.sort_by_time():")
    for t in sorted_by_time:
        print(f"  • [{t.preferred_start_time.strftime('%H:%M')}] {t.title} for {t.pet.name}")

    # B. Filtering tasks by pet using Scheduler.filter_tasks()
    mochi_tasks = Scheduler.filter_tasks(all_raw_tasks, pet_name="Mochi")
    print(f"\n🐕 2. Mochi's tasks only via Scheduler.filter_tasks(pet_name='Mochi'):")
    for t in mochi_tasks:
        print(f"  • {t.title}")

    # C. Basic Conflict Detection check & Lightweight warnings
    print("\n⚠️ 3. Conflict Detection & Lightweight Warnings:")
    overlap_exists = Scheduler.detect_conflict(t1, t2)
    print(f"  • Overlap check between '{t1.title}' and '{t2.title}': {overlap_exists}")
    
    # Lightweight warnings run (only on tasks active for today!)
    today = datetime.date.today()
    today_tasks = Scheduler.get_tasks_for_date(all_raw_tasks, today)
    warnings = Scheduler.check_conflicts(today_tasks)
    print(f"  • Lightweight warning check for Today (found {len(warnings)} conflicts):")
    for warn in warnings:
        print(f"    {warn}")
    
    # D. Handling Recurring Tasks by date
    tomorrow = today + datetime.timedelta(days=1)
    
    # Let's change t4 (Laser Toy Play) to recurrence="weekly" and set t5 to recurrence="none"
    t4.recurrence = "weekly"
    t5.recurrence = "none"
    
    print("\n🔄 4. Recurring Task Filtering for Tomorrow:")
    tomorrow_tasks = Scheduler.get_tasks_for_date(all_raw_tasks, tomorrow)
    print(f"  • Tomorrow's active tasks (recurrent daily/weekly matching weekday):")
    for t in tomorrow_tasks:
        print(f"    - {t.title} ({t.recurrence})")
    print("=" * 95)

if __name__ == "__main__":
    main()
