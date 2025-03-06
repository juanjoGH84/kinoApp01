# features.py
import streamlit as st
import pandas as pd
from bson import ObjectId
from data_manager import get_data, userinfo
from fbfeature.commingFilmsList import load_films, display_films

dbname, collection_name = userinfo() 

information = get_data(dbname, collection_name)
if information:
    df_info = pd.DataFrame(information)
    if '_id' in df_info.columns:
        df_info['_id'] = df_info['_id'].apply(lambda x: str(x) if isinstance(x, ObjectId) else x)
else:
    df_info = pd.DataFrame()
films = load_films()

filmList = [
    {"Title": film.get("title", "No Title"), "Booked From": film.get("booked_from", "No Date"),  "ID ": film.get("id", "No  ID"), "ID Parent": film.get("parent_id", "No parent ID")}
    for film in films
]

def display_key_features():
    """Display the key features of the app."""
    
    # Fetch and display user data from the 'users' database
    st.write("### User Information:")
    st.table(df_info)
    
    # Fetch and display films data from the 'comingFilms' collection
    st.write("### Coming Films:")
    st.table(filmList)
    
    display_films(films)
    