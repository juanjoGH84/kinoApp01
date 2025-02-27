#pages/filmDisplay.py
import streamlit as st
from fbfeature.commingFilmsList import load_films, display_films
from authenticator import authenticate_user

# Check if the user is authenticated
if "username" in st.session_state and st.session_state.username:
    st.title("Film Display")
    films = load_films()  # Fetch the films data
    display_films(films)  # Display the films
else:
    st.write("### Please log in to access this page.")