import streamlit as st
import requests 
import pandas as pd
import base64
from io import BytesIO
import os

if 'loaded_plan' not in st.session_state:
    st.session_state['loaded_plan'] = None

st.session_state['back_to_main_page'] = "Go back to Main Page"
st.session_state['current_folder'] = os.path.dirname(os.path.abspath(__file__))
st.session_state['tmp_save_folder'] = os.path.dirname(os.path.abspath(__file__)) + "/tmp"
st.session_state['loaded_plan_path'] = None

def main_page():
    st.title('Vocabulary Memorization Helper')
    st.write('This app helpes you to memorize TOEFL or GRE vocabulary by the forgetting curve method.')
    st.write('According to the forgetting curve, people should review the vocabulary on the 1st, 2nd, 4th, 7th, and 15th days.')
    # Create buttons for navigation to different plans
    if st.button('New plan'):
        st.session_state.current_page = 'new_plan'
        st.rerun()
    elif st.button('Continue plan'):
        st.session_state.current_page = 'continue_plan'
        st.rerun()

def new_plan():
    st.title('New plan')
    st.write('Select one of the following options to start a new plan.')
    if st.button('TOEFL'):
        st.session_state['loaded_plan'] = 'toefl.db'
        os.path.join(st.session_state['current_folder'], st.session_state['loaded_plan'])
        st.session_state.current_page = 'your_plan'
        st.rerun()
    if st.button('GRE'):
        st.session_state['loaded_plan'] = 'gre.db'
        os.path.join(st.session_state['current_folder'], st.session_state['loaded_plan'])
        st.session_state.current_page = 'your_plan'
        st.rerun()
        # st.markdown('[Click me to download GRE plan](path/to/gre_plan.db)')
    if st.button(f":red[**{st.session_state['back_to_main_page']}**]"):
        st.session_state.current_page = 'main_page'
        st.rerun()

def continue_plan():
    st.title('Continue plan')
    st.write('Upload you plan (database) so you can continue with your existing plan.')
    
    uploaded_file = st.file_uploader("Choose a plan")
    if uploaded_file is not None:
        # # To read file as bytes:
        # bytes_data = uploaded_file.getvalue()
        # st.write(bytes_data)
        file_path = os.path.join(st.session_state['tmp_save_folder'], uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.session_state['loaded_plan'] = str(uploaded_file.name)
        st.session_state['loaded_plan_path'] = file_path
        
        upload_db()

        st.write("Upload backend successful")
            
        if st.button("Go to your Plan"):
            st.session_state.current_page = 'your_plan'
            st.rerun()

    if st.button(f":red[**{st.session_state['back_to_main_page']}**]"):
        st.session_state.current_page = 'main_page'
        st.rerun()

def your_plan():
    st.title('Your plan: ' + st.session_state.loaded_plan)
    st.write('You are now ready to start your plan. Click the button below to see today\'s plan.')

    if st.button("Check Today's vocaulary"):
        st.session_state.current_page = 'display_plan'
        st.rerun()

    if st.button(f":red[**{st.session_state['back_to_main_page']}**]"):
        st.session_state.current_page = 'main_page'
        st.rerun()

def display_plan():
    st.title("Today's plan")
    st.write('These are the words you should review today. Click the button below to download the plan.')

    response = get_today_plan()
    
    # Convert response to DataFrame
    df = pd.DataFrame.from_dict(response, orient='index', columns=['word_id', 'word', 'definition', 'sentence', 'start_date', 'current_memory_index'])
    
    # Display the response in a table
    st.table(df)
    
    punch_in()

    # Create a CSV file from the DataFrame
    csv = df.to_csv(index=False)
    
    # Create a download link for the CSV file
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="plan.csv">Click me to download the table</a>'
    st.markdown(href, unsafe_allow_html=True)

    if st.button('Go back to Your plan'):
        st.session_state.current_page = 'your_plan'
        st.rerun()

    if st.button(f":red[**{st.session_state['back_to_main_page']}**]"):
        st.session_state.current_page = 'main_page'
        st.rerun()

def upload_db():
    file = open(st.session_state['loaded_plan_path'], 'rb')
    response = requests.post('http://localhost:8080/upload', files={'file': file})
    if response.status_code == 200:
        st.write('Upload to frontend successful')

def get_today_plan():
    # example response
    # response = {"1": {"word": "Ephemeral", "definition": "Lasting for a very short time."}}
    response = requests.get('http://localhost:8080/today')
    if response.status_code == 200:
        st.write("Get today's plan successful")
    return response.json()

def punch_in():
    response = requests.post('http://localhost:8080/punch_in', data={'word_ids': [1,2]})
    if response.status_code == 200:
        st.write('Punch in successful')

# Initialize the page state if it doesn't exist
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main_page'
    st.rerun()

# Display pages based on the current state
if st.session_state.current_page == 'main_page':
    main_page()
elif st.session_state.current_page == 'new_plan':
    new_plan()
elif st.session_state.current_page == 'continue_plan':
    continue_plan()
elif st.session_state.current_page == 'your_plan':
    your_plan()
elif st.session_state.current_page == 'display_plan':
    display_plan()
