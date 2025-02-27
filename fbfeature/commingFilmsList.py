#/fbfeature/commingFilmsList.py
import os
import json
from datetime import datetime
from data_manager import get_data  # Import the database query function
import streamlit as st

def load_films():
    """
    Load the film data from the MongoDB collection and sort them by the 'booked_from' date.
    :return: Sorted list of films
    """
    # Fetch data from the MongoDB collection
    films_data = get_data("users", "commingFilms")

    if not films_data:
        return []

    # Extract the `data` list from the MongoDB document
    films = films_data[0].get("data", [])

    # Sort the films by 'booked_from' date
    try:
        films.sort(key=lambda film: datetime.strptime(film['booked_from'], '%Y-%m-%d'))
    except KeyError as e:
        print(f"Key error: {e}. Ensure all documents have a 'booked_from' field.")
    except ValueError as e:
        print(f"Date format error: {e}. Ensure 'booked_from' dates are in the 'YYYY-MM-DD' format.")

    return films

def display_films(films):
    """
    Display films in a three-column layout.
    :param films: List of film dictionaries
    """
    if films:
        # Create three columns
        col1, col2, col3 = st.columns(3)

        # Iterate over each film and display its details in columns
        for index, film in enumerate(films):
            # Get the film title
            title = film.get('title', 'No Title')

            # Get the body for language_id: 1
            body = next(
                (content['body'] for content in film.get('contents', []) if content['language_id'] == 1),
                "No description available"
            )

            # Get the booked_from date
            booked_from = film.get('booked_from', 'No booked date')

            # Get the poster URL
            poster_url = next(
                (asset['url'] for asset in film.get('assets', []) if asset['type'] == 'poster'),
                None
            )

            # Choose the column based on the index
            col = [col1, col2, col3][index % 3]

            # Display the film's details in the selected column
            with col:
                st.subheader(title)
                st.write(f"**Booked From:** {booked_from}")
                st.write(f"**Description:** {body}")
                if poster_url:
                    st.image(poster_url, caption=title, width=150)
                st.markdown("---")  # Add a separator within the column
    else:
        st.write("No films available.")
