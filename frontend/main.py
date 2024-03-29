from datetime import datetime, timedelta
import json
import streamlit as st
import requests
import os

class PlanManager:
    """A class to manage the user's vocabulary memorization plan."""
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
                review_dates = [
                    current_date + timedelta(days=interval)
                    for interval in forgetting_curve_intervals
                ]
                schedule[f"list:{list_number},unit:{unit_number}"] = {
                    i: date.strftime('%Y-%m-%d')
                    for i, date in enumerate(review_dates)
                }
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
    st.write(f":orange[**Help you to extract the scheduled words to learn today.**]")
    st.write('Enhance your vocabulary memorization with the forgetting curve method, ideal for GRE preparation and more.')
    st.write('According to the forgetting curve, the best time review a word is the 1st, 2nd, 4th, 7th, 15th day after you first learn it.')
    st.write('Click below to start a new plan or continue with an existing one. (NEED TO UPLOAD YOUR EXISTING PLAN.)')
    st.write('You will always have a button to go back to this main page.')

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
        plan = st.session_state['plan_manager'].generate_forgetting_curve_schedule(today)
        st.session_state['plan_manager'].plan = 'gre_default_plan.json'
        st.session_state['plan_manager'].save_schedule_to_json(plan, 'gre_default_plan.json')
        st.session_state.current_page = 'your_plan'
        st.rerun()
        
    if 'confirm_back' not in st.session_state:
        st.session_state['confirm_back'] = False

    # Display the confirmation expander if 'confirm_back' is True
    if st.session_state['confirm_back']:
        with st.expander("Confirmation", expanded=True):
            st.warning("Are you sure you want to go back to the main page?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button('Yes, go back'):
                    # Actions to take if user confirms
                    st.session_state.current_page = 'main_page'
                    st.session_state['confirm_back'] = False  # Reset the flag
                    st.experimental_rerun()
            with col2:
                if st.button('Cancel'):
                    # Reset the flag without rerouting if user cancels
                    st.session_state['confirm_back'] = False
                    st.rerun()

    # Check for a button click to trigger the confirmation message
    if st.button(f":red[**Back to Main Page**]"):  # Using a simplified label for clarity
        st.session_state['confirm_back'] = True
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

        
    if 'confirm_back' not in st.session_state:
        st.session_state['confirm_back'] = False

    # Display the confirmation expander if 'confirm_back' is True
    if st.session_state['confirm_back']:
        with st.expander("Confirmation", expanded=True):
            st.warning("Are you sure you want to go back to the main page?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button('Yes, go back'):
                    # Actions to take if user confirms
                    st.session_state.current_page = 'main_page'
                    st.session_state['confirm_back'] = False  # Reset the flag
                    st.experimental_rerun()
            with col2:
                if st.button('Cancel'):
                    # Reset the flag without rerouting if user cancels
                    st.session_state['confirm_back'] = False
                    st.rerun()

    # Check for a button click to trigger the confirmation message
    if st.button(f":red[**Back to Main Page**]"):  # Using a simplified label for clarity
        st.session_state['confirm_back'] = True
        st.rerun()

def your_plan():
    """Displays the user's current plan and provides options to proceed."""
    st.title(f"Your Plan: {st.session_state.plan_manager.plan}")
    st.write("You're all set to begin your plan. Use the button below to view today's vocabulary.")

    if st.button("Check Today's Vocabulary"):
        st.session_state.current_page = 'check_today_words'
        st.rerun()

    with open(st.session_state.plan_manager.plan, 'rb') as f:
        st.download_button(f":green[**Download Your Plan (List and Unit based)**]", f, file_name=st.session_state.plan_manager.plan)

    converted_plan_path = convert_to_time_based(st.session_state.plan_manager.plan)
    with open(converted_plan_path, 'rb') as f:
        st.download_button(f":green[**Download Your Plan (Date based)**]", f, file_name=converted_plan_path)

    if st.button(f":red[**{st.session_state['back_to_main_page']}**]"):
        st.session_state.current_page = 'main_page'
        st.rerun()

        
    if 'confirm_back' not in st.session_state:
        st.session_state['confirm_back'] = False

    # Display the confirmation expander if 'confirm_back' is True
    if st.session_state['confirm_back']:
        with st.expander("Confirmation", expanded=True):
            st.warning("Are you sure you want to go back to the main page?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button('Yes, go back'):
                    # Actions to take if user confirms
                    st.session_state.current_page = 'main_page'
                    st.session_state['confirm_back'] = False  # Reset the flag
                    st.experimental_rerun()
            with col2:
                if st.button('Cancel'):
                    # Reset the flag without rerouting if user cancels
                    st.session_state['confirm_back'] = False
                    st.rerun()

    # Check for a button click to trigger the confirmation message
    if st.button(f":red[**Back to Main Page**]"):  # Using a simplified label for clarity
        st.session_state['confirm_back'] = True
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
                
                attribute = ["word_id", "meaning_US", "sentence", "word"]

                result = requests.post('http://127.0.0.1:5000/db/acquire_unit', json={'list': list_number, 'unit': unit_number, 'attribute': attribute})

                if result.status_code == 200:
                    data = result.json()
                    data_dict = json.loads(data)
                    new_dict = {f"list:{list_number},unit:{unit_number}": data_dict}
                    display[key] = new_dict

            st.download_button(f":green[**Download today's words**]", json.dumps(display, indent=4), f"today_words.json")
            st.write(display)

    if st.button(f":red[**{st.session_state['back_to_main_page']}**]"):
        st.session_state.current_page = 'main_page'
        st.rerun()

        
    if 'confirm_back' not in st.session_state:
        st.session_state['confirm_back'] = False

    # Display the confirmation expander if 'confirm_back' is True
    if st.session_state['confirm_back']:
        with st.expander("Confirmation", expanded=True):
            st.warning("Are you sure you want to go back to the main page?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button('Yes, go back'):
                    # Actions to take if user confirms
                    st.session_state.current_page = 'main_page'
                    st.session_state['confirm_back'] = False  # Reset the flag
                    st.experimental_rerun()
            with col2:
                if st.button('Cancel'):
                    # Reset the flag without rerouting if user cancels
                    st.session_state['confirm_back'] = False
                    st.rerun()

    # Check for a button click to trigger the confirmation message
    if st.button(f":red[**Back to Main Page**]"):  # Using a simplified label for clarity
        st.session_state['confirm_back'] = True
        st.rerun()

def convert_to_time_based(file_path):
    # Load the JSON file content
    with open(file_path, 'r') as file:
        study_plan = json.load(file)

    # Convert the nested dictionary into a list of tuples for sorting
    date_plan = []
    for list_unit, dates in study_plan.items():
        for index, date in dates.items():
            date_plan.append((date, list_unit, index))

    # Sort the list based on dates
    date_plan_sorted = sorted(date_plan, key=lambda x: x[0])

    # Re-arrange based on dates into a new dictionary
    sorted_study_plan = {}
    for date, list_unit, index in date_plan_sorted:
        if date not in sorted_study_plan:
            sorted_study_plan[date] = []
        sorted_study_plan[date].append((list_unit, index))

    # Save sorted_study_plan to a JSON file
    output_file_path = file_path.split('.json')[0] + '_sorted.json'  # Path to the output JSON file
    with open(output_file_path, 'w') as output_file:
        json.dump(sorted_study_plan, output_file, indent=4)

    return output_file_path

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
