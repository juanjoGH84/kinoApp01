# fbfeature/fbfunctions.py
import streamlit as st
import facebook as fb
import requests
from data_manager import get_data

def prepare_facebook_post(film):
    """Prepare the message and image URL for a Facebook post."""
    title = film.get('title', 'No Title')
    body = next((content['body'] for content in film.get('contents', []) if content['language_id'] == 1), "No body available")
    image_url = next((asset['url'] for asset in film.get('assets', []) if asset['type'] == 'poster'), None)
    booked_from = film.get('booked_from', 'Unknown date')

    message = f"{title}\n\n{body}\n booked from {booked_from}\nBestill billetten din på: https://tynsetkulturhus.no/kinoprogram/"
    return message, image_url

def publish_to_facebook(message, image_url):
    """Publish a message and optional image URL to Facebook."""
    # Retrieve the username from session state
    username = st.session_state.get('username')
    
    if not username:
        return "No user logged in."

    # Retrieve user information from the database
    users = get_data("users", "user_accounts")
    current_user = next((user for user in users if user.get('user') == username), None)
    
    if not current_user:
        return "User not found."

    # Get the page access token from the user's information
    page_access_token = current_user.get('fbToken')
    page_id = current_user.get('fbPage')

    if not page_access_token:
        st.error("Page Access Token is not set. Please configure it in User Information Page")
        return

    try:
        graph_api = fb.GraphAPI(page_access_token)
        if image_url:
            # Download the image from the URL
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                with open("temp_image.jpg", "wb") as f:
                    f.write(image_response.content)
                # Upload the image to Facebook
                response = graph_api.put_photo(
                    image=open("temp_image.jpg", 'rb'),
                    message=message,
                    album_path=f"{page_id}/photos"
                )
            else:
                st.error("Failed to download the image.")
                return
        else:
            response = graph_api.put_object(
                parent_object=page_id,
                connection_name='feed',
                message=message
            )

        if 'id' in response:
            st.success(f"Post published successfully! Post ID: {response['id']}")
        else:
            st.error("Failed to publish the post.")
    except fb.GraphAPIError as e:
        st.error(f"An error occurred while posting to Facebook: {e}")
