import streamlit as st
import pymongo

@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data():
    db = client.users
    items = db.user_accounts.find()
    items = list(items)  # make hashable for st.cache_data
    return items

items = get_data()

st.table(items) 

for item in items:
    st.write(f" The user {item['user']} password is : {item['pwd']}:")