#fbfeature/ChatGPTfunctions.py

from openai import OpenAI
import streamlit as st
from data_manager import get_data
from fbfeature.fbfunctions import prepare_facebook_post
from dotenv import load_dotenv

load_dotenv()

def generate_facebook_post(message, film):
    """Generate a Facebook post using OpenAI."""
    # Retrieve the username from session state
    username = st.session_state.get('username')
    
    if not username:
        return "No user logged in."

    # Retrieve user information from the database
    users = get_data("users", "user_accounts")
    current_user = next((user for user in users if user.get('user') == username), None)
    
    if not current_user:
        return "User not found."

    # Get the GPT token from the user's information
    gpt_token = current_user.get('GPTtoken')
    
    if not gpt_token:
        return "GPT token not found for the user."

    client = OpenAI(api_key=gpt_token)
    
    # Prepare the message using the prepare_facebook_post function
    message, _ = prepare_facebook_post(film)
    print(message)
    try:
        # Make a request to the OpenAI ChatCompletion API
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": message}
            ],
            model="gpt-4o",  # Use a valid model name, like "gpt-3.5-turbo"
            temperature=0.7
        )

        # Extract and return the response content
        generated_text = chat_completion.choices[0].message.content
        print(generated_text)
        return generated_text
    
        

    except Exception as e:
        return f"An error occurred while generating the text: {e}"