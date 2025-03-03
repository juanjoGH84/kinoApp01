#/fbfeature/commingFilmsList.py
from datetime import datetime
import streamlit as st
import subprocess
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_manager import get_data, update_data  # Import the database query function
from fbfeature.fbfunctions import prepare_facebook_post, publish_to_facebook
from fbfeature.ChatGPTfunctions import generate_facebook_post

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
    all_films = films_data[0].get("data", [])
    
    unique_films = {}

    for film in all_films:
        parent_id = film.get('parent_id')
        # Use parent_id as key; if already present, skip adding duplicate
        if parent_id is not None and parent_id not in unique_films:
            unique_films[parent_id] = film
    
    films = list(unique_films.values())

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
    # Button to run commingfilmsRequest.py
    if st.button("Update Coming Films"):
        result = subprocess.run(["python3", "fbfeature/commingfilmsRequest.py"], capture_output=True, text=True)
        if result.returncode == 0:
            st.success("Coming films updated successfully.")
        else:
            st.error(f"Error updating coming films: {result.stderr}")

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

            # Get the generated text
            generated_text = film.get('generated_text', '')

            # Choose the column based on the index
            col = [col1, col2, col3][index % 3]

            # Display the film's details in the selected column
            with col:
                st.subheader(title)
                st.write(f"**Booked From:** {booked_from}")
                st.write(body)
                if poster_url:
                    st.image(poster_url, caption=title, width=150)
                st.write(f"Generated Text: {generated_text}")
                st.markdown("---")  # Add a separator within the column

                if st.button(f"Generate Facebook Post for {title}"):
                    message, _ = prepare_facebook_post(film)
                    generated_text = generate_facebook_post(message, film)
                    update_data("users", "commingFilms", {'parent_id': film['parent_id']}, {'$set': {'generated_text': generated_text}})
                    st.success("Generated text updated successfully.")
                    st.write(generated_text)

                if st.button(f"Publish Facebook Post for {title}"):
                    message, image_url = prepare_facebook_post(film)
                    publish_to_facebook(message, image_url)
                    print(message)
    
    else:
        st.write("No films available.")
