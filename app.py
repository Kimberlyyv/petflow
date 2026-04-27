import streamlit as st
from datetime import date
from src.scheduler import Owner, Pet, Task, Scheduler
from src.retrieval import get_guideline

st.set_page_config(page_title="PetFlow+", page_icon="🐾", layout="centered")

st.title("🐾 PetFlow+")

st.markdown(
    """
Welcome to PetFlow+.

This app helps a pet owner keep track of pet care tasks and generate a daily schedule.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PetFlow+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan", 120, "Morning tasks preferred")

scheduler = Scheduler(st.session_state.owner)

st.divider()

st.subheader("Owner and Pet Info")

owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
st.session_state.owner.name = owner_name

pet_name = st.text_input("Pet name")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Pet age", min_value=0, step=1)

if st.button("Add Pet"):
    new_pet = Pet(pet_name, species, pet_age)
    st.session_state.owner.add_pet(new_pet)
    st.success(f"{pet_name} was added successfully.")

if st.session_state.owner.pets:
    st.write("Current pets:")
    for pet in st.session_state.owner.pets:
        st.write(f"- {pet.name} ({pet.species}, age {pet.age})")
else:
    st.info("No pets added yet.")

st.divider()

st.subheader("Add a Task")

if st.session_state.owner.pets:
    pet_names = [pet.name for pet in st.session_state.owner.pets]

    selected_pet_name = st.selectbox("Choose a pet", pet_names)
    task_title = st.text_input("Task title", value="Morning walk")
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    priority_number = st.number_input("Priority (1 = highest)", min_value=1, max_value=5, value=1)
    task_time = st.text_input("Task time (HH:MM)", value="08:00")
    frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])

    if st.button("Add Task"):
        if not task_title.strip():
            st.error("Task title cannot be empty.")

        elif ":" not in task_time:
            st.error("Time must be in HH:MM format.")

        else:
            selected_pet = None
            for pet in st.session_state.owner.pets:
                if pet.name == selected_pet_name:
                    selected_pet = pet
                    break

            if selected_pet:
                new_task = Task(
                    task_title,
                    int(duration),
                    int(priority_number),
                    task_time,
                    frequency,
                    date.today()
                )
                selected_pet.add_task(new_task)

                st.success(f"Task added for {selected_pet.name}.")

                guideline = get_guideline(selected_pet.species, task_title)
                st.info(f"Care tip: {guideline}")
else:
    st.info("Add a pet first before creating tasks.")

st.divider()

st.subheader("Current Tasks")

all_tasks = scheduler.get_all_tasks()

if all_tasks:
    task_rows = []
    for task in scheduler.generate_daily_plan():
        task_rows.append(
            {
                "Time": task.time,
                "Task": task.description,
                "Duration": task.duration,
                "Priority": task.priority,
                "Frequency": task.frequency,
                "Completed": task.completed,
            }
        )
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate Schedule"):
    daily_plan = scheduler.generate_daily_plan()

    if daily_plan:
        st.success("Daily schedule generated!")

        table_data = []
        for task in daily_plan:
            table_data.append(
                {
                    "Time": task.time,
                    "Task": task.description,
                    "Duration": task.duration,
                    "Priority": task.priority,
                    "Completed": task.completed,
                }
            )

        st.table(table_data)

        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for conflict in conflicts:
                st.warning(conflict)
    else:
        st.warning("No tasks available to schedule.")