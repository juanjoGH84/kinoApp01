# user_information.py
import streamlit as st
from data_manager import get_data, update_data, data_access


dbname, collection_name = data_access()

# Set the title of the page
st.title("User Information")
username = st.session_state.get('username')

if username:
    # Retrieve user information from the database
    users = get_data( dbname, collection_name)

    # Find the current user's information
    current_user = next((user for user in users if user.get('user') == username), None)

    # Display current user's information
    if current_user:
        st.write(f"User ID: {current_user.get('_id')}")
        st.write(f"Name: {current_user.get('user')}")
        
        # Editable email field
        new_email = st.text_input("Email", value=current_user.get('email'))
        
        if st.button("Update Email"):
            # Update the email in the database
            update_data(dbname, collection_name, {'_id': current_user['_id']}, {'$set': {'email': new_email}})
            st.success("Email updated successfully.")
        
        # Editable DX Token field
        new_dx_token = st.text_input("DX Token", value=current_user.get('dxToken'))
        
        if st.button("Update DX Token"):
            # Update the DX Token in the database
            update_data(dbname, collection_name, {'_id': current_user['_id']}, {'$set': {'dxToken': new_dx_token}})
            st.success("DX Token updated successfully.")

        new_fb_page = st.text_input("Facebook Page", value=current_user.get('fbPage'))
        
        if st.button("Update Facebook Page"):
            # Update the DX Token in the database
            update_data(dbname, collection_name, {'_id': current_user['_id']}, {'$set': {'fbPage': new_fb_page}})
            st.success("Facebook Token updated successfully.")
        # Editable Facebook Token field
        new_fb_token = st.text_input("Facebook Token", value=current_user.get('fbToken'))
        
        if st.button("Update Facebook Token"):
            # Update the DX Token in the database
            update_data(dbname, collection_name, {'_id': current_user['_id']}, {'$set': {'fbToken': new_fb_token}})
            st.success("Facebook Token updated successfully.")
        
        new_GPT_token = st.text_input("ChatGPT Token", value=current_user.get('GPTtoken'))
        
        if st.button("Update ChatGPT Token"):
            # Update the DX Token in the database
            update_data(dbname, collection_name, {'_id': current_user['_id']}, {'$set': {'GPTtoken': new_GPT_token}})
            st.success("ChatGPT Token updated successfully.")
                    
    else:
        st.write("Current user information not found.")
else:
    st.write("No current user logged in.")