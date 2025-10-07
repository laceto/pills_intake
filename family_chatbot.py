import streamlit as st
import json
import os
from datetime import datetime, date

# File to store pill intake data
DATA_FILE = "pill_intake.json"

# Load existing data from JSON file

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # File is empty or corrupted, return empty list
                return []
    return []


# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Main Streamlit app
def main():
    st.title("Pill Intake Tracker")

    # Load existing data
    intake_data = load_data()

    # Get today's date for pre-filling
    today = date.today()

    # Form for daily intake
    with st.form(key='intake_form'):
        st.write("Track your 3 pills")

        # Date input pre-filled with today
        selected_date = st.date_input("Date", value=today, format="YYYY/MM/DD")
        date_str = selected_date.strftime("%Y-%m-%d")

        # 3 checkboxes for the pills
        pill1 = st.checkbox("Pill 1 Taken")
        pill2 = st.checkbox("Pill 2 Taken")
        pill3 = st.checkbox("Pill 3 Taken")

        submit_button = st.form_submit_button(label="Submit Intake")

        if submit_button:
            pills_taken = [pill1, pill2, pill3]
            num_taken = sum(pills_taken)

            # Check if there's already an entry for the selected date
            existing_entry = next((entry for entry in intake_data if entry['date'] == date_str), None)

            if existing_entry:
                # Update existing entry
                existing_entry['pills_taken'] = pills_taken
                st.success(f"Updated intake for {date_str}: {num_taken}/3 pills taken!")
            else:
                # Add new entry
                new_entry = {
                    'date': date_str,
                    'pills_taken': pills_taken
                }
                intake_data.append(new_entry)
                st.success(f"Recorded intake for {date_str}: {num_taken}/3 pills taken!")

            # Save updated data
            save_data(intake_data)

    # Display intake history
    st.write("### Intake History")
    if intake_data:
        for entry in sorted(intake_data, key=lambda x: x['date'], reverse=True):
            taken = sum(entry['pills_taken'])
            details = ", ".join([f"Pill {i+1}: {'Taken' if taken else 'Not Taken'}" for i, taken in enumerate(entry['pills_taken'])])
            st.write(f"{entry['date']}: {taken}/3 pills taken ({details})")
    else:
        st.write("No intake history yet.")

if __name__ == "__main__":
    main()
