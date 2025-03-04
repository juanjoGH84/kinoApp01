#data_manager.py
import pymongo
import streamlit as st

@st.cache_resource
def connect_db(db_name, collection_name):
    """
    Connects to a MongoDB database and returns a specific collection.
    :param db_name: Name of the database
    :param collection_name: Name of the collection
    :return: MongoDB collection object
    """
    client = pymongo.MongoClient(**st.secrets["mongo"])
    db = client.get_database(db_name)  # Connect to the specified database
    return db[collection_name]  # Return the specified collection

def get_data(db_name, collection_name):
    """
    Retrieves all documents from the specified collection.
    :param db_name: Name of the database
    :param collection_name: Name of the collection
    :return: List of documents from the collection
    """
    collection = connect_db(db_name, collection_name)
    items = collection.find()
    return list(items)

def insert_data(db_name, collection_name, data):
    """
    Inserts data into the specified collection.
    :param db_name: Name of the database
    :param collection_name: Name of the collection
    :param data: Data to insert (list or dict)
    """
    collection = connect_db(db_name, collection_name)
    if isinstance(data, list):
        collection.insert_many(data)  # Insert multiple documents
    elif isinstance(data, dict):
        collection.insert_one(data)  # Insert a single document


def update_data(db_name, collection_name, query, update):
    """
    Updates data in the specified collection.
    :param db_name: Name of the database
    :param collection_name: Name of the collection
    :param query: Query to match documents
    :param update: Update to apply
    """
    collection = connect_db(db_name, collection_name)
    collection.update_one(query, update)

def data_access():
 #user_db = connect_db("KinoDev", "user_accounts")
 db_name = st.secrets["database"]["dbname"]
 collection_name =  st.secrets["database"]["coll_usrs"]
 return db_name, collection_name
