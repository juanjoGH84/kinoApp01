# main.py
import streamlit as st
from authenticator import authenticate_user, logout
from data_manager import get_data
from features import display_key_features

# Fetch data from the database
#st.title("Kino Manager App")
st.markdown('<h1 style="display: flex; align-items: center;"><i class="fa-solid fa-film" style="margin-right: 10px;"></i> Kino Manager App</h1>', unsafe_allow_html=True)
st.markdown('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">', unsafe_allow_html=True)

# Authenticate the user
if authenticate_user():
    # If authenticated, display the features
    display_key_features()
    logout()  # Show the logout button
else:
    # If not authenticated, only show the authentication forms
    st.write("### Please log in to access the features.")
