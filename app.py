import streamlit as st
from frontend.sidebar import display_sidebar
from frontend.data_display import display_data_view
from backend.process import process_escritura_publica
from backend.database import find_escritura_by_carpeta
import os
import tempfile


# --- Configuración de la Página ---
st.set_page_config(
    page_title="Herramienta de Análisis de Escrituras Públicas",
    layout="wide"
)

# --- Inicialización del Estado de la Sesión ---
# Estos estados persistirán entre interacciones.
if 'editing' not in st.session_state:
    st.session_state.editing = False
if 'resultado_analisis' not in st.session_state:
    st.session_state.resultado_analisis = None
if 'current_folder_number' not in st.session_state:
    st.session_state.current_folder_number = None
# Nueva bandera para controlar el flujo post-guardado.
if 'data_saved_successfully' not in st.session_state:
    st.session_state.data_saved_successfully = False


def main():
    """
    Función principal que organiza la aplicación Streamlit.
    """
    st.title("Herramienta de Análisis de Escrituras Públicas")
    st.markdown("Sube un PDF para analizar o busca una carpeta existente en la barra lateral.")

    # --- Barra Lateral (Sidebar) ---
    uploaded_file, new_folder_number = display_sidebar()

    # --- NUEVA LÓGICA: Limpiar la vista después de guardar ---
    # Este bloque se activa cuando data_display.py establece la bandera.
    if st.session_state.get('data_saved_successfully', False):
        st.session_state.resultado_analisis = None
        st.session_state.current_folder_number = None
        # Reseteamos la bandera para evitar que se ejecute en un bucle.
        st.session_state.data_saved_successfully = False
        # Mostramos un mensaje de éxito claro aquí.
        st.success("Datos guardados correctamente. La vista ha sido limpiada.")
        # No se necesita un rerun aquí, el flujo natural del script mostrará la vista vacía.

    # --- Lógica de Procesamiento de PDF (NUEVA ESCRITURA) ---
    if 'start_analysis' in st.session_state and st.session_state.start_analysis:
        if uploaded_file and new_folder_number:
            st.session_state.current_folder_number = new_folder_number
            with st.spinner(f"Procesando PDF para la nueva carpeta {new_folder_number}..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        temp_pdf_path = tmp_file.name
                    st.session_state.resultado_analisis = process_escritura_publica(temp_pdf_path)
                except Exception as e:
                    st.error(f"Ocurrió un error durante el procesamiento del PDF: {e}")
                finally:
                    if 'temp_pdf_path' in locals() and os.path.exists(temp_pdf_path):
                        os.remove(temp_pdf_path)
        st.session_state.start_analysis = False
        st.rerun()

    # --- Lógica de Búsqueda (CARPETA EXISTENTE) ---
    if 'search_triggered' in st.session_state and st.session_state.search_triggered:
        search_number = st.session_state.search_query
        with st.spinner(f"Buscando carpeta número {search_number}..."):
            found_data = find_escritura_by_carpeta(search_number)
        if found_data:
            st.success(f"Carpeta {search_number} encontrada y cargada.")
            st.session_state.resultado_analisis = found_data
            st.session_state.current_folder_number = search_number
        else:
            st.warning(f"No se encontró ninguna carpeta con el número {search_number}.")
            st.session_state.resultado_analisis = None
            st.session_state.current_folder_number = None
        st.session_state.search_triggered = False
        st.rerun()

    # --- Vista Principal de Datos ---
    if st.session_state.resultado_analisis:
        display_data_view(st.session_state.resultado_analisis, st.session_state.current_folder_number)

    # --- Información Adicional ---
    st.markdown("---")
    with st.expander("Cómo funciona esta herramienta"):
        st.markdown(
            """
            * **Analizar Nueva Escritura:** Sube un PDF, asigna un número de carpeta y haz clic en 'Iniciar Extracción'.
            * **Buscar y Editar:** Introduce un número de carpeta existente y haz clic en 'Buscar Carpeta' para cargar, ver y editar sus datos.
            """
        )

if __name__ == "__main__":
    main()