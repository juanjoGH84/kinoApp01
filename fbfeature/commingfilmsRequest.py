# commingfilmsRequest.py
import os
import sys
import requests
# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_manager import get_data, insert_data, userinfo

#Database 
dbname, collection_name = userinfo()


# Retrieve the dxToken from the database
users = get_data(dbname, collection_name)
dx_token = None

for user in users:
    if 'dxToken' in user:
        dx_token = user['dxToken']
        break

if not dx_token:
    raise ValueError("DX Token not found in the database.")

# API details
url = "https://public.dx.no/v1/partners/145/productions/comingFilms"

# Set up the authorization header
headers = {
    "Authorization": f"Bearer {dx_token}"
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
