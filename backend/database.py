import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime
import os

# --- Variable de estado para la conexión ---
# Usamos esto para evitar reconectar en cada rerun de Streamlit.
# Es más eficiente que crear una conexión global al inicio del script.
if "db_client" not in st.session_state:
    st.session_state.db_client = None

def get_db_collection():
    """
    Establece o reutiliza una conexión a MongoDB y devuelve la colección.
    """
    if "db_client" in st.session_state and st.session_state.db_client:
        try:
            st.session_state.db_client.admin.command('ping')
            db = st.session_state.db_client['extractor_db']
            return db['escrituras']
        except ConnectionFailure:
            st.warning("La conexión a MongoDB se perdió. Intentando reconectar...")
            st.session_state.db_client = None

    try:
        # --- CAMBIO CLAVE PARA DOCKER CON AUTENTICACIÓN ---
        # Usamos variables de entorno para la URI, usuario y contraseña de MongoDB.
        # Dentro de Docker Compose, 'mongodb' es el nombre del servicio.
        mongodb_host = os.getenv("MONGODB_HOST", "mongodb") # Por defecto 'mongodb' si es en Docker Compose
        mongodb_port = os.getenv("MONGODB_PORT", "27017")
        mongodb_user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
        mongodb_pass = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
        mongodb_db_name = os.getenv("MONGO_DATABASE", "extractor_db") # Nombre de la DB

        auth_source = "admin" 

        # Construir la URI de conexión
        if mongodb_user and mongodb_pass:
            # Nos aseguramos que pymongo esté usando la autenticación correcta (authSource)
            MONGODB_URI = f"mongodb://{mongodb_user}:{mongodb_pass}@{mongodb_host}:{mongodb_port}/{mongodb_db_name}?authSource={auth_source}"
        else:
            MONGODB_URI = f"mongodb://{mongodb_host}:{mongodb_port}/{mongodb_db_name}"
            st.warning("No se encontraron credenciales de MongoDB. Conectando sin autenticación (no recomendado para producción).")

        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping') # Esto autentica contra la DB 'admin' si authSource está en la URI.

        st.session_state.db_client = client
        st.success(f"Conexión a MongoDB ({mongodb_host}:{mongodb_port}) establecida con éxito.")

        db = client[mongodb_db_name] # Aquí seleccionamos la base de datos de trabajo
        return db['escrituras']
    except Exception as e:
        st.error(f"Error crítico al conectar a la base de datos: {e}. Asegúrate de que MongoDB esté corriendo y las credenciales sean correctas.")
        return None

def save_to_mongodb(data: dict, numero_carpeta: int) -> bool:
    """
    Guarda o actualiza una escritura en MongoDB.

    Returns:
        bool: True si la operación fue exitosa, False en caso de error.
    """
    collection = get_db_collection()
    if collection is None:
        st.error("No se puede guardar: no hay conexión a la base de datos.")
        return False

    if not numero_carpeta:
        st.error("El número de carpeta no puede estar vacío.")
        return False

    update_payload = data.copy()
    update_payload['numero_carpeta'] = numero_carpeta
    # Eliminamos el _id y fecha_creacion para que no cree problemas cuando se hace una modificación a los datos.
    update_payload.pop('_id', None)
    update_payload.pop('fecha_creacion', None)

    now = datetime.now()
    
    update_operations = {
        '$set': {
            **update_payload,
            'ultima_modificacion': now
        },
        '$setOnInsert': {
            'fecha_creacion': now
        }
    }

    try:
        resultado = collection.update_one(
            {'numero_carpeta': numero_carpeta},
            update_operations,
            upsert=True
        )
        # No mostramos el mensaje de éxito aquí, lo hará app.py.
        return True # Devolvemos True en caso de éxito.
    except Exception as e:
        st.error(f"Error al guardar/actualizar el documento en MongoDB: {e}")
        return False # Devolvemos False en caso de error.


def find_escritura_by_carpeta(numero_carpeta: int):
    """
    Busca un documento en MongoDB por su número de carpeta.
    """
    collection = get_db_collection()
    if collection is None:
        st.error("No se puede buscar: sin conexión a la base de datos.")
        return None
    
    try:
        document = collection.find_one({'numero_carpeta': int(numero_carpeta)})
        if document:
            # Limpiamos el _id para evitar problemas al reenviarlo en una actualización.
            document.pop('_id', None)
        return document
    except Exception as e:
        st.error(f"Ocurrió un error durante la búsqueda: {e}")
        return None
