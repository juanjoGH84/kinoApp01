# commingfilmsRequest.py
import os
import requests
from dotenv import load_dotenv
from data_manager import insert_data

# Load environment variables from .env
load_dotenv()

# API details
url = "https://public.dx.no/v1/partners/145/productions/comingFilms"
auth_token = os.getenv('DX_TOKEN')

# Set up the authorization header
headers = {
    "Authorization": f"Bearer {auth_token}"
}

try:
    # Make the GET request to the API
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
    data = response.json()  # Parse the response JSON
    
    # Insert data into MongoDB using data_manager.py
    insert_data("users", "commingFilms", data)
    
    print("Data successfully inserted into MongoDB.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")
except Exception as e:
    print(f"Error inserting data into MongoDB: {e}")
