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

    # 3. Create multiple Tasks with different start times, categories, and priorities
    # High Priority Walk
    t1 = WalkTask(
        title="Morning Walk",
        duration=30,
        priority="high",
        preferred_start_time=datetime.time(8, 0),
        pet=mochi,
        distance=1.5,
        route="Greenlake Loop"
    )
    
    # High Priority Breakfast (Biscuit)
    t2 = FeedingTask(
        title="Breakfast Feeding",
        duration=10,
        priority="high",
        preferred_start_time=datetime.time(8, 30),
        pet=biscuit,
        food_type="Canned Salmon",
        amount_cups=0.5
    )
    
    # Medium Priority Medication
    t3 = MedicationTask(
        title="Joint Supplement",
        duration=5,
        priority="medium",
        preferred_start_time=datetime.time(9, 0),
        pet=mochi,
        med_name="Cosequin",
        dosage="1 chewable"
    )

    # Low Priority Grooming / Play session
    t4 = EnrichmentTask(
        title="Laser Toy Play",
        duration=15,
        priority="low",
        preferred_start_time=datetime.time(14, 0),
        pet=biscuit,
        activity_type="Laser chasing"
    )

    # Let's add a large Enrichment task that exceeds the remaining budget to verify the bar and skipped list
    t5 = EnrichmentTask(
        title="Agility Park Training",
        duration=80,
        priority="low",
        preferred_start_time=datetime.time(16, 0),
        pet=mochi,
        activity_type="Obstacle run"
    )

    # 4. Generate and print schedule
    scheduler = Scheduler()
    result = scheduler.generate_daily_schedule(owner)
    
    print_styled_schedule(owner, result)

if __name__ == "__main__":
    main()
