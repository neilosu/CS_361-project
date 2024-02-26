import streamlit as st
import requests
import pandas as pd
import base64
from io import BytesIO
import os
from datetime import datetime, timedelta
import json

class PlanManager:
    def __init__(self, plan=None):
        """Initializes the PlanManager with an optional path to a plan file."""
        self.plan = plan
        self.today = datetime.today().strftime('%Y-%m-%d')

    def generate_forgetting_curve_schedule(self, starting_date_str):
        """
        Generates a review schedule based on the forgetting curve methodology.

        Args:
            starting_date_str (str): The starting date in YYYY-MM-DD format.

        Returns:
            dict: A dictionary with numeric keys and values as review dates.
        """
        starting_date = datetime.strptime(starting_date_str, '%Y-%m-%d')
        forgetting_curve_intervals = [0, 1, 2, 4, 7, 15]
        schedule = {}

        total_lists = 34
        units_per_list = 10

        current_date = starting_date

        for list_number in range(1, total_lists + 1):
            total_units = 2 if list_number == 34 else units_per_list

            for unit_number in range(1, total_units + 1):
                review_dates = [current_date + timedelta(days=interval) for interval in forgetting_curve_intervals]
                schedule[f"list:{list_number},unit:{unit_number}"] = {i: date.strftime('%Y-%m-%d') for i, date in enumerate(review_dates)}
                current_date += timedelta(days=1)

        return schedule
    
    
    def save_schedule_to_json(self, schedule, filename):
        """
        Saves the given schedule to a JSON file.

        Args:
            schedule (dict): The schedule to save.
            filename (str): The name of the file to save the schedule to.
        """
        with open(filename, 'w') as f:
            json.dump(schedule, f, indent=4)

# Initialize Streamlit session state with defaults
st.session_state.setdefault('back_to_main_page', "Go back to Main Page")
st.session_state.setdefault('current_folder', os.path.dirname(os.path.abspath(__file__)))
st.session_state.setdefault('tmp_save_folder', os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp"))
st.session_state.setdefault('loaded_plan', None)
st.session_state.setdefault('plan_manager', PlanManager())

def main_page():
    """Displays the main page of the Vocabulary Memorization Helper."""
    st.title('Vocabulary Memorization Helper')
    st.write('Enhance your vocabulary memorization with the forgetting curve method, ideal for GRE preparation and more.')
    st.write('Click below to start a new plan or continue with an existing one.')

    if st.button('New plan'):
        st.session_state.current_page = 'new_plan'
        st.rerun()
    elif st.button('Continue plan'):
        st.session_state.current_page = 'continue_plan'
        st.rerun()

def new_plan():
    """Displays options to start a new memorization plan."""
    st.title('Start a New Plan')
    st.write('Choose an option below to initiate a new vocabulary learning plan starting today.')

    if st.button('GRE Vocabulary'):
        today = st.session_state.plan_manager.today
        plan = st.session_state['plan_manager'].generate_forgetting_curve_schedule('2024-01-01')
        st.session_state['plan_manager'].plan = 'gre_default_plan.json'
        st.session_state['plan_manager'].save_schedule_to_json(plan, 'gre_default_plan.json')
        st.session_state.current_page = 'your_plan'
        st.rerun()

    if st.button(st.session_state['back_to_main_page']):
        st.session_state.current_page = 'main_page'
        st.rerun()

def continue_plan():
    """Provides an option to upload and continue with an existing plan."""
    st.title('Continue Your Plan')
    st.write('Upload your existing plan to resume your learning journey.')

    uploaded_file = st.file_uploader("Choose a file", type=['json'])
    if uploaded_file is not None:
        file_contents = uploaded_file.read()
        with open(uploaded_file.name, 'wb') as f:
            f.write(file_contents)

        st.write('Succeeded !')
        if st.button("Go check your plan"):
            st.session_state['plan_manager'].plan = uploaded_file.name
            st.session_state.current_page = 'your_plan'
            st.rerun()

def your_plan():
    """Displays the user's current plan and provides options to proceed."""
    st.title(f"Your Plan: {st.session_state.plan_manager.plan}")
    st.write("You're all set to begin your plan. Use the button below to view today's vocabulary.")

    if st.button("Check Today's Vocabulary"):
        st.session_state.current_page = 'check_today_words'
        st.rerun()

    if st.button(st.session_state['back_to_main_page']):
        st.session_state.current_page = 'main_page'
        st.rerun()

def check_today_words():
    """Displays the user's vocabulary for the day."""
    st.title("Today's Vocabulary")
    st.write("Here are the words you need to learn today.")

    if st.session_state.plan_manager.plan is not None:
        with open(st.session_state.plan_manager.plan, 'r') as f:
            plan = json.load(f)
            # st.write(todays_vocabulary)

            today = st.session_state.plan_manager.today
            keys_with_date = {}
            for main_key, value in plan.items():
                if today in value.values():
                    for key, date in value.items():
                        if date == today:
                            keys_with_date[key + 'th'] = main_key
            st.write("Explanation: '5th':'list:5,unit:2' means this is the 5th time you memorize this unit (list 5 unit 2)")

            display = {}
            for key, value in keys_with_date.items():
                list_number, unit_number = value.split(',')[0].split(':')[1], value.split(',')[1].split(':')[1]
                
                # attribute = ["word_id", "meaning_US", "sentence"]
                # result = requests.post('http://localhost:5000/word', json={'list': list_number, 'unit': unit_number, 'attribute': attribute})
                result = requests.Response()
                result.status_code = 200
                result._content = b'{"happy": {"word_id": "qe234jhwe3", "meaning_US": "delightful", "sentence": "I am happy."}, "sad" : {"word_id": "435bkj3o", "meaning_US": "unhappy", "sentence": "I am sad."}}'
                
                if result.status_code == 200:
                    data = result.json()
                    new_dict = {"list:5,unit:2": data}
                    display[key] = new_dict

            st.write(display)

    if st.button(st.session_state['back_to_main_page']):
        st.session_state.current_page = 'main_page'
        st.rerun()

# Routing logic to display the appropriate page based on the current state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main_page'
    st.rerun()

if st.session_state.current_page == 'main_page':
    main_page()
elif st.session_state.current_page == 'new_plan':
    new_plan()
elif st.session_state.current_page == 'continue_plan':
    continue_plan()
elif st.session_state.current_page == 'your_plan':
    your_plan()
elif st.session_state.current_page == 'check_today_words':
    check_today_words()
