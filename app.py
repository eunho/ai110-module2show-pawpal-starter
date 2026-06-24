import streamlit as st
import datetime
from pawpal_system import (
    Owner,
    Pet,
    Task,
    FeedingTask,
    WalkTask,
    MedicationTask,
    EnrichmentTask,
    AppointmentTask,
    Scheduler,
    ScheduleResult
)

# 1. Page Configuration & Premium Theme Styling
st.set_page_config(
    page_title="PawPal+ | Smart Pet Care Planner",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Styling for glassmorphism and clean design
st.markdown(
    """
    <style>
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }
    .timeline-item {
        background: rgba(255, 255, 255, 0.03);
        border-left: 4px solid #4CAF50;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 8px 8px 0;
    }
    .timeline-item.high {
        border-left-color: #FF5252;
    }
    .timeline-item.medium {
        border-left-color: #FFD740;
    }
    .timeline-item.low {
        border-left-color: #40C4FF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. State Initialization
if "owner" not in st.session_state:
    # Initialize Jordan as default owner
    st.session_state.owner = Owner(name="Jordan", daily_time_budget=120)
    
    # Initialize some default pets to make the experience smooth
    mochi = Pet(name="Mochi", species="dog", age=2.5, weight=15.0, energy_level="high")
    biscuit = Pet(name="Biscuit", species="cat", age=4.0, weight=10.0, energy_level="low")
    st.session_state.owner.add_pet(mochi)
    st.session_state.owner.add_pet(biscuit)
    
    # Initialize default tasks
    WalkTask(
        title="Morning Walk",
        duration=30,
        priority="high",
        preferred_start_time=datetime.time(8, 0),
        pet=mochi,
        distance=1.5,
        route="Greenlake Loop"
    )
    FeedingTask(
        title="Breakfast Feeding",
        duration=10,
        priority="high",
        preferred_start_time=datetime.time(8, 30),
        pet=biscuit,
        food_type="Canned Salmon",
        amount_cups=0.5
    )

if "schedule_result" not in st.session_state:
    st.session_state.schedule_result = None

owner = st.session_state.owner

# 3. Sidebar Configuration (Owner Settings & Pet Registry)
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/dog-heart.png", width=80)
    st.title("🐾 PawPal+ Control Panel")
    st.markdown("Manage your household settings and pet profiles.")
    
    st.divider()
    
    # Section A: Owner Configuration
    st.subheader("👤 Owner Profile")
    new_owner_name = st.text_input("Owner Name", value=owner.name)
    new_budget = st.number_input(
        "Daily Care Budget (mins)",
        min_value=10,
        max_value=1440,
        value=owner.daily_time_budget,
        step=10
    )
    owner.name = new_owner_name
    owner.daily_time_budget = int(new_budget)
    
    # Availability Windows
    st.markdown("**Availability Windows**")
    if st.button("Set Default (07:00 - 22:00)"):
        owner.clear_availability_windows()
        owner.add_availability_window(datetime.time(7, 0), datetime.time(22, 0))
        st.success("Set default window!")
        
    st.divider()
    
    # Section B: Pet Registry
    st.subheader("🐕 Register a Pet")
    with st.form("add_pet_form", clear_on_submit=True):
        pet_name = st.text_input("Pet Name")
        species = st.selectbox("Species", ["dog", "cat", "other"])
        age = st.number_input("Age (years)", min_value=0.1, max_value=30.0, value=2.0, step=0.5)
        weight = st.number_input("Weight (lbs)", min_value=0.5, max_value=250.0, value=15.0, step=1.0)
        energy_level = st.select_slider("Energy Level", options=["low", "medium", "high"], value="medium")
        
        submitted_pet = st.form_submit_button("Add Pet Profile")
        if submitted_pet:
            if pet_name.strip():
                new_pet = Pet(
                    name=pet_name.strip(),
                    species=species,
                    age=float(age),
                    weight=float(weight),
                    energy_level=energy_level
                )
                owner.add_pet(new_pet)
                st.success(f"Added {new_pet.name} successfully!")
                st.rerun()
            else:
                st.error("Pet Name cannot be empty.")

# 4. Main Panel Interface Layout
st.title("🐾 PawPal+ care planner")
st.caption(f"Helping **{owner.name}** keep pets happy, healthy, and on schedule.")

# Section A: Registered Pets Dashboard
st.subheader("🐾 Registered Pets")
if not owner.pets:
    st.info("No pets registered yet. Add one in the sidebar panel.")
else:
    cols = st.columns(len(owner.pets))
    for i, pet in enumerate(owner.pets):
        with cols[i]:
            with st.container(border=True):
                col_p1, col_p2 = st.columns([3, 1])
                with col_p1:
                    icon = "🐶" if pet.species == "dog" else "🐱" if pet.species == "cat" else "🐾"
                    st.markdown(f"### {icon} {pet.name}")
                    st.markdown(f"**Species:** {pet.species.capitalize()}")
                    st.markdown(f"**Age:** {pet.age} yrs | **Weight:** {pet.weight} lbs")
                    st.markdown(f"**Energy:** {pet.energy_level.upper()}")
                with col_p2:
                    if st.button("🗑️", key=f"del_pet_{pet.name}"):
                        owner.remove_pet(pet.name)
                        st.warning(f"Removed {pet.name}.")
                        st.rerun()

st.divider()

# Section B: Add a Task & Tasks List
st.subheader("📅 Schedule a Care Task")
if not owner.pets:
    st.warning("Please register a pet in the sidebar before scheduling a task.")
else:
    task_col1, task_col2 = st.columns([1, 1])
    
    with task_col1:
        with st.form("add_task_form", clear_on_submit=True):
            st.markdown("### Create New Activity")
            task_title = st.text_input("Task Title", placeholder="e.g. Walk, Evening Kibble, Heartworm pill")
            target_pet_name = st.selectbox("Assign to Pet", options=[p.name for p in owner.pets])
            target_pet = next(p for p in owner.pets if p.name == target_pet_name)
            
            task_category = st.selectbox("Task Category", options=["Walk", "Feeding", "Medication", "Enrichment", "Appointment"])
            
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, step=5)
            priority = st.selectbox("Scheduling Priority", options=["high", "medium", "low"], index=1)
            
            preferred_time = st.time_input("Preferred Start Time", value=datetime.time(8, 0))
            recurrence = st.selectbox("Recurrence", options=["daily", "weekly", "none"])
            start_date = st.date_input("Start / Creation Date", value=datetime.date.today())
            
            # Dynamic attributes based on category selection
            st.markdown("---")
            st.markdown("**Category Specific Details**")
            
            if task_category == "Walk":
                walk_distance = st.number_input("Walk Distance (miles)", min_value=0.1, max_value=15.0, value=1.0, step=0.5)
                walk_route = st.text_input("Route Name", value="Neighborhood Loop")
            elif task_category == "Feeding":
                food_type = st.text_input("Food Type/Brand", value="Kibble")
                food_amt = st.number_input("Amount (cups)", min_value=0.1, max_value=10.0, value=1.0, step=0.25)
            elif task_category == "Medication":
                med_name = st.text_input("Medication Name")
                med_dosage = st.text_input("Dosage Instructions", placeholder="e.g. 1 pill, 5ml")
            elif task_category == "Enrichment":
                activity_type = st.text_input("Enrichment Activity", value="Puzzle Toy")
            elif task_category == "Appointment":
                app_location = st.text_input("Location", value="Vet Clinic")
                app_notes = st.text_area("Appointment Notes")
                
            submitted_task = st.form_submit_button("Add Activity to Care List")
            
            if submitted_task:
                if not task_title.strip():
                    st.error("Task Title cannot be empty.")
                else:
                    # Instantiate specialized subclasses (auto-registers with pet via __post_init__)
                    if task_category == "Walk":
                        WalkTask(
                            title=task_title.strip(),
                            duration=int(duration),
                            priority=priority,
                            preferred_start_time=preferred_time,
                            pet=target_pet,
                            recurrence=recurrence,
                            created_date=start_date,
                            distance=float(walk_distance),
                            route=walk_route.strip()
                        )
                    elif task_category == "Feeding":
                        FeedingTask(
                            title=task_title.strip(),
                            duration=int(duration),
                            priority=priority,
                            preferred_start_time=preferred_time,
                            pet=target_pet,
                            recurrence=recurrence,
                            created_date=start_date,
                            food_type=food_type.strip(),
                            amount_cups=float(food_amt)
                        )
                    elif task_category == "Medication":
                        if not med_name.strip():
                            st.error("Medication Name is required.")
                        else:
                            MedicationTask(
                                title=task_title.strip(),
                                duration=int(duration),
                                priority=priority,
                                preferred_start_time=preferred_time,
                                pet=target_pet,
                                recurrence=recurrence,
                                created_date=start_date,
                                med_name=med_name.strip(),
                                dosage=med_dosage.strip()
                            )
                    elif task_category == "Enrichment":
                        EnrichmentTask(
                            title=task_title.strip(),
                            duration=int(duration),
                            priority=priority,
                            preferred_start_time=preferred_time,
                            pet=target_pet,
                            recurrence=recurrence,
                            created_date=start_date,
                            activity_type=activity_type.strip()
                        )
                    elif task_category == "Appointment":
                        AppointmentTask(
                            title=task_title.strip(),
                            duration=int(duration),
                            priority=priority,
                            preferred_start_time=preferred_time,
                            pet=target_pet,
                            recurrence=recurrence,
                            created_date=start_date,
                            location=app_location.strip(),
                            notes=app_notes.strip()
                        )
                    st.success(f"Added task '{task_title.strip()}' for {target_pet.name}!")
                    st.rerun()
                    
    with task_col2:
        st.markdown("### 📋 Scheduled Care Activities List")
        all_tasks = owner.get_all_tasks()
        
        # Add sorting & filtering expander
        with st.expander("🔍 Filter & Sort Activities List", expanded=False):
            filter_pet = st.selectbox("Filter by Pet", options=["All Pets"] + [p.name for p in owner.pets], index=0)
            filter_status = st.selectbox("Filter by Status", options=["All", "Completed", "Incomplete"], index=0)
            sort_by = st.selectbox("Sort by", options=["Preferred Start Time", "Priority", "Duration", "Task Title"], index=0)

        # Apply filtering
        filtered_tasks = all_tasks
        if filter_pet != "All Pets":
            filtered_tasks = Scheduler.filter_tasks(filtered_tasks, pet_name=filter_pet)
        if filter_status == "Completed":
            filtered_tasks = Scheduler.filter_tasks(filtered_tasks, is_completed=True)
        elif filter_status == "Incomplete":
            filtered_tasks = Scheduler.filter_tasks(filtered_tasks, is_completed=False)

        # Apply sorting
        if sort_by == "Preferred Start Time":
            filtered_tasks = Scheduler.sort_by_time(filtered_tasks)
        elif sort_by == "Priority":
            priority_map = {"high": 3, "medium": 2, "low": 1}
            filtered_tasks = sorted(filtered_tasks, key=lambda t: priority_map.get(t.priority, 0), reverse=True)
        elif sort_by == "Duration":
            filtered_tasks = sorted(filtered_tasks, key=lambda t: t.duration, reverse=True)
        elif sort_by == "Task Title":
            filtered_tasks = sorted(filtered_tasks, key=lambda t: t.title.lower())

        if not filtered_tasks:
            st.info("No matching activities found.")
        else:
            for task in filtered_tasks:
                emoji = "🦮" if task.get_category() == "walk" else "🦴" if task.get_category() == "feeding" else "💊" if task.get_category() == "medication" else "🎾" if task.get_category() == "enrichment" else "🏥"
                status_color = "🟢" if task.is_completed else "🟡"
                
                with st.container(border=True):
                    col_t1, col_t2 = st.columns([4, 1])
                    with col_t1:
                        st.markdown(f"**{emoji} {task.title}** for **{task.pet.name}**")
                        st.caption(f"Priority: {task.priority.upper()} | Duration: {task.duration}m | Time: {task.preferred_start_time.strftime('%H:%M')}")
                        
                        # Subclass details displaying
                        if isinstance(task, WalkTask):
                            st.caption(f"Details: {task.distance} miles along {task.route}")
                        elif isinstance(task, FeedingTask):
                            st.caption(f"Details: {task.amount_cups} cups of {task.food_type}")
                        elif isinstance(task, MedicationTask):
                            st.caption(f"Details: Dosage: {task.dosage} of {task.med_name}")
                        elif isinstance(task, EnrichmentTask):
                            st.caption(f"Details: {task.activity_type}")
                        elif isinstance(task, AppointmentTask):
                            st.caption(f"Details: at {task.location}. Notes: {task.notes}")
                            
                    with col_t2:
                        # Complete toggle
                        if not task.is_completed:
                            if st.button("✔️", key=f"comp_{task.task_id}", help="Mark complete"):
                                task.mark_complete()
                                st.rerun()
                        else:
                            st.markdown("✅ *Done*")
                            
                        # Delete button
                        if st.button("🗑️", key=f"del_{task.task_id}", help="Delete activity"):
                            task.pet.remove_task(task.task_id)
                            st.warning("Deleted task.")
                            st.rerun()

st.divider()

# Section C: Generate Daily Schedule
st.subheader("🧠 Algorithmic Scheduler Engine")
st.markdown("Generate a daily care timeline that fits availability windows and daily budget without overlapping.")

# Date picker for scheduling
selected_date = st.date_input("Select Date for Schedule", value=datetime.date.today())

# Button to reset completions and generate schedule
btn_col1, btn_col2 = st.columns([3, 1])
with btn_col1:
    gen_button = st.button("⚡ Generate Schedule & Resolve Conflicts", type="primary")
with btn_col2:
    if st.button("🔄 Reset Completions"):
        Scheduler.reset_completions(owner.get_all_tasks())
        st.success("All task completion statuses reset!")
        st.rerun()

if gen_button:
    all_tasks = owner.get_all_tasks()
    # Filter tasks active for the selected date based on recurrence rules
    date_active_tasks = Scheduler.get_tasks_for_date(all_tasks, selected_date)
    
    if not date_active_tasks:
        st.error(f"No active activities to schedule for {selected_date.strftime('%A, %b %d, %Y')}.")
    else:
        scheduler = Scheduler()
        st.session_state.schedule_result = scheduler.generate_daily_schedule(owner, tasks=date_active_tasks)
        st.success(f"Daily care schedule for {selected_date.strftime('%A, %b %d, %Y')} generated successfully!")

# Display generated results if they exist
result: ScheduleResult = st.session_state.schedule_result
if result:
    st.divider()
    
    # 1. Metrics dashboard
    dash_col1, dash_col2, dash_col3 = st.columns(3)
    
    with dash_col1:
        # Time budget stats
        budget = owner.daily_time_budget
        used = result.total_time_used
        st.metric(
            label="Total Time Scheduled", 
            value=f"{used} mins", 
            delta=f"{budget - used} mins remaining" if used <= budget else f"{used - budget} mins over!",
            delta_color="normal" if used <= budget else "inverse"
        )
        # Visual progress bar
        pct = min(used / budget if budget > 0 else 0, 1.0)
        st.progress(pct)
        
    with dash_col2:
        num_scheduled = len(result.scheduled_tasks)
        st.metric(label="Tasks Scheduled", value=num_scheduled)
        
    with dash_col3:
        num_skipped = len(result.skipped_tasks)
        st.metric(
            label="Tasks Skipped/Deferred", 
            value=num_skipped,
            delta=f"-{num_skipped} items" if num_skipped > 0 else "All Clear",
            delta_color="off" if num_skipped == 0 else "inverse"
        )
        
    # 2. Timeline rendering
    st.markdown("### 🕒 Optimal Care Timeline")
    if not result.scheduled_tasks:
        st.info("No tasks could be scheduled.")
    else:
        for item in result.scheduled_tasks:
            start_str = item["start_time"].strftime("%H:%M")
            end_str = item["end_time"].strftime("%H:%M")
            task = item["task"]
            priority_class = task.priority.lower()
            
            # Specific icon
            emoji = "🦮" if task.get_category() == "walk" else "🦴" if task.get_category() == "feeding" else "💊" if task.get_category() == "medication" else "🎾" if task.get_category() == "enrichment" else "🏥"
            
            # Additional details rendering
            extra_details = ""
            if isinstance(task, WalkTask):
                extra_details = f"— Walk {task.distance} miles along {task.route}"
            elif isinstance(task, FeedingTask):
                extra_details = f"— Feed {task.amount_cups} cups of {task.food_type}"
            elif isinstance(task, MedicationTask):
                extra_details = f"— Give {task.dosage} of {task.med_name}"
            
            st.markdown(
                f"""
                <div class="timeline-item {priority_class}">
                    <strong>🕒 {start_str} - {end_str}</strong> | {emoji} {task.title} for <strong>{task.pet.name}</strong> 
                    <span style="font-size: 0.8em; margin-left: 15px; padding: 2px 6px; border-radius: 4px; background: rgba(255,255,255,0.1);">
                        {task.priority.upper()}
                    </span>
                    <div style="font-size: 0.9em; opacity: 0.8; margin-top: 5px;">
                        {extra_details} (Duration: {task.duration} mins)
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    # 3. Skipped Tasks
    if result.skipped_tasks:
        st.markdown("### ⚠️ Skipped / Deferred Tasks")
        for task, reason in result.skipped_tasks:
            st.warning(f"**{task.title}** for **{task.pet.name}** ({task.duration}m) — **Reason:** {reason}")
            
    # 4. Assistant reasoning log
    with st.expander("🤖 Assistant Reasoning Log & Scheduling Explanations", expanded=False):
        for line in result.explanation:
            st.markdown(line)
