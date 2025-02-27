import streamlit as st
from pymongo import MongoClient

# Leer secretos desde el archivo secrets.toml
MONGO_URI = st.secrets["mongodb"]["uri"]

# Conectar a MongoDB
client = MongoClient(MONGO_URI)
db = client["KinoDev"]  # Nombre de tu base de datos
collection = db["commingFilms"]  # Nombre de tu colección

# Función para agregar un documento a la colección
def agregar_documento(data):
    collection.insert_one(data)

# Función para obtener todos los documentos de la colección
def obtener_documentos():
    return list(collection.find())

# Interfaz de Streamlit
st.title("Aplicación con Streamlit y MongoDB")

# Formulario para agregar un documento
with st.form(key="formulario"):
    nombre = st.text_input("Nombre")
    edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
    submit_button = st.form_submit_button(label="Agregar")

    if submit_button:
        documento = {"nombre": nombre, "edad": edad}
        agregar_documento(documento)
        st.success("Documento agregado con éxito")

# Mostrar documentos en la colección
if st.button("Mostrar documentos"):
    documentos = obtener_documentos()
    for doc in documentos:
        st.write(doc)