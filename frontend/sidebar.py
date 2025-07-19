import streamlit as st

def display_sidebar():
    """
    Muestra la barra lateral con controles para subir un archivo nuevo
    o buscar uno existente.

    Returns:
        tuple: (uploaded_file, assigned_number) para el flujo de carga.
    """
    with st.sidebar:
        st.header("Nueva Escritura")

        # 1. Subida de archivo PDF
        uploaded_file = st.file_uploader(
            "Sube tu archivo PDF aquí",
            type="pdf",
            help="Solo se permiten archivos PDF."
        )

        # 2. Asignar un número de carpeta
        assigned_number = st.number_input(
            "Asigna un número de Carpeta:",
            min_value=0,
            value=1,
            step=1,
            help="Este es el número de Carpeta para la nueva operación."
        )

        # 3. Botón "Iniciar Extracción"
        if st.button("Iniciar Extracción", type="primary"):
            if uploaded_file is not None:
                st.success("¡Análisis iniciado!")
                st.info(f"Archivo: {uploaded_file.name}")
                st.info(f"Número: {assigned_number}")
                # Comunicamos la acción de análisis a app.py
                st.session_state.start_analysis = True
                st.session_state.search_triggered = False # Aseguramos que no se active la búsqueda
            else:
                st.warning("Por favor, sube un archivo PDF antes de iniciar.")
                st.session_state.start_analysis = False
        
        # Separador visual para la nueva funcionalidad
        st.markdown("---")
        
        st.header("Buscar Carpeta Existente")

        # 4. Campo para buscar por número de carpeta
        search_number = st.number_input(
            "Introduce el número de Carpeta a buscar:",
            min_value=0,
            step=1,
            key="search_number_input"
        )

        # 5. Botón para iniciar la búsqueda
        if st.button("Buscar Carpeta"):
            if search_number > 0:
                # Comunicamos la acción de búsqueda a app.py
                st.session_state.search_query = search_number
                st.session_state.search_triggered = True
                st.session_state.start_analysis = False # Aseguramos que no se active el análisis
            else:
                st.warning("Por favor, introduce un número de carpeta válido para buscar.")

        return uploaded_file, assigned_number