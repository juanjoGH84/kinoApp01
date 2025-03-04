import streamlit as st
from data_manager import get_data, connect_db, data_access

# Initialize the database connection

dbname, collection_name = data_access()


#"KinoDev","user_accounts" dbname, collection_name
user_db = connect_db( dbname, collection_name)


def user_update(name):
    """Update the session state with the logged-in username."""
    st.session_state.username = name


def select_signup():
    """Switch to the sign-up form."""
    st.session_state.form = 'signup_form'

def login_form():
        login_form = st.sidebar.form(key='login_form', clear_on_submit=True)
        username = login_form.text_input(label='Enter Username')
        user_pas = login_form.text_input(label='Enter Password', type='password')
        login = login_form.form_submit_button(label='Sign In')
        
        if login:
            user = user_db.find_one({'user': username, 'pwd': user_pas})
            if user:
                user_update(username)
                st.sidebar.success(f"Welcome back, {username.upper()}!")
                st.rerun()
            else:
                st.sidebar.error('Invalid username or password.')

def signup_form():
    # Sign-Up Form
        signup_form = st.sidebar.form(key='signup_form', clear_on_submit=True)
        new_username = signup_form.text_input(label='Enter Username*')
        new_user_email = signup_form.text_input(label='Enter Email Address*')
        new_user_pas = signup_form.text_input(label='Enter Password*', type='password')
        user_pas_conf = signup_form.text_input(label='Confirm Password*', type='password')
        signup = signup_form.form_submit_button(label='Sign Up')
        
        if signup:
            if '' in [new_username, new_user_email, new_user_pas, user_pas_conf]:
                st.sidebar.error('All fields are required.')
            elif user_db.find_one({'user': new_username}):
                st.sidebar.error('Username already exists.')
            elif user_db.find_one({'email': new_user_email}):
                st.sidebar.error('Email is already registered.')
            elif new_user_pas != user_pas_conf:
                st.sidebar.error('Passwords do not match.')
            else:
                user_db.insert_one({'user': new_username, 'email': new_user_email, 'pwd': new_user_pas})
                user_update(new_username)
                st.sidebar.success(f"Welcome, {new_username.upper()}!")
                st.rerun()
        
        login_form()

def authenticate_user():
    """
    Handles user authentication.
    Returns True if the user is authenticated, False otherwise.
    """
    # Initialize Session State for Username and Form
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'form' not in st.session_state:
        st.session_state.form = ''

    # If the user is already authenticated, return True
    if st.session_state.username != '':
        st.sidebar.success(f"You are logged in as {st.session_state.username.upper()}")
        return True

    # If not authenticated, show login or sign-up forms
    st.sidebar.write("### Authentication")
    
    if st.session_state.form == 'signup_form':
        signup_form()

    else:
        # Login Form
        login_form()
        
    # Create Account Button
    if st.session_state.form != 'signup_form':
        st.sidebar.button("Create Account", on_click=select_signup)

    return False

def logout():
    """Log the user out."""
    if st.sidebar.button("Log Out"):
        st.session_state.username = ''
        st.rerun()
