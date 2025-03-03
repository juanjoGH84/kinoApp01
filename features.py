# features.py
import streamlit as st
from data_manager import get_data
from fbfeature.commingFilmsList import load_films, display_films

information = get_data("KinoDev", "user_accounts")

films = load_films()

filmList = [
            {"Title": film.get("title", "No Title"), "Booked From": film.get("booked_from", "No Date")}
            for film in films
        ]

def display_key_features():
    """Display the key features of the app."""
    
    # Fetch and display user data from the 'users' database
    st.write("### User Information:")
    st.table(information)
# Fetch and display films data from the 'comingFilms' collection
    st.write("### Coming Films:")
    st.table(filmList)

    
    display_films(films)