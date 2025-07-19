import streamlit as st
import pandas as pd
from backend.database import save_to_mongodb

def display_data_view(data, carpeta):
    """
    Muestra la vista principal con los datos extraídos y los botones
    para editar y guardar.

    Args:
        data (dict): Los datos extraídos del PDF para mostrar.
    """
    st.header("Visualización y Edición de Datos Extraídos")

    # --- Controles de Edición y Guardado ---
    col1, col2 = st.columns(2)
    with col1:
        # Botón para alternar el modo de edición
        if st.session_state.get('editing', False):
            if st.button("Guardar Cambios en Interfaz"):
                st.session_state.editing = False
                st.success("Cambios guardados en la interfaz. Recuerda guardarlos en la base de datos.")
                st.rerun()
        else:
            if st.button("Habilitar Edición"):
                st.session_state.editing = True
                st.rerun()

    with col2:
        if st.button("Guardar en Base de Datos", type="primary"):
            # Llamamos a la función y capturamos el resultado.
            save_success = save_to_mongodb(data, carpeta)
            
            # Si el guardado fue exitoso, establecemos la bandera.
            if save_success:
                st.session_state.data_saved_successfully = True
                # Forzamos un rerun para que app.py pueda detectar la bandera inmediatamente.
                st.rerun()

    # Mensaje informativo sobre el modo actual
    if st.session_state.get('editing', False):
        st.info("Modo Edición: Puedes modificar los campos. Haz clic en 'Guardar Cambios en Interfaz' para aplicar.")
    else:
        st.info("Modo Visualización: Para modificar, haz clic en 'Habilitar Edición'.")

    st.markdown("---")

    # --- Visualización Estructurada de Datos ---
    display_structured_data(data, carpeta)


def display_structured_data(data, carpeta):
    """
    Muestra o permite editar datos JSON de forma estructurada con separadores y tablas.

    Args:
        data (dict): Los datos JSON a mostrar/editar. Estos datos se modificarán directamente.
        carpeta (int): El número de carpeta asignada a la operación.
    """
    if data is None or not data: # Verifica si los datos son None o están vacíos
        st.info("No hay datos extraídos del PDF para mostrar o editar. Por favor, procesa un documento primero.")
        return # Sale de la función si no hay datos
    st.success("Análisis completado con éxito.")
    st.header("Datos de la Escritura")

    # ---
    ## Datos de la Operación
    st.subheader("Número de Carpeta")
    # Muestra el número de carpeta asignada previamente cuando se busca un documento o el nuevo número de carpeta asignado al iniciar una nueva operación.
    carpeta_mostrada = data.get("numero_carpeta", carpeta)
    st.markdown(f"**Carpeta Asignada:** {carpeta_mostrada}")

    st.subheader("Datos de la Operación")
    col1_op, col2_op = st.columns(2)
    with col1_op:
        data["fecha_otorgamiento"] = st.text_input("Fecha Otorgamiento", value=data.get("fecha_otorgamiento", ""), disabled=not st.session_state.editing, key="fecha_otorgamiento")
        data["numero_escritura"] = st.text_input("Número Escritura", value=data.get("numero_escritura", ""), disabled=not st.session_state.editing, key="numero_escritura")
        data["escribano"] = st.text_input("Escribano", value=data.get("escribano", ""), disabled=not st.session_state.editing, key="escribano")
    with col2_op:
        data["lugar_escritura"] = st.text_input("Lugar Escritura", value=data.get("lugar_escritura", ""), disabled=not st.session_state.editing, key="lugar_escritura")
        data["folio_escritura"] = st.text_input("Folio Escritura", value=data.get("folio_escritura", ""), disabled=not st.session_state.editing, key="folio_escritura")
        data["registro_escribano"] = st.text_input("Registro Escribano", value=data.get("registro_escribano", ""), disabled=not st.session_state.editing, key="registro_escribano")

    # ---
    ## Partes Intervinientes
    st.subheader("Partes Intervinientes")
    if "partes_intervinientes" in data and data["partes_intervinientes"]:
        for i, parte in enumerate(data["partes_intervinientes"]):
            st.markdown(f"### Parte {i+1}: {parte.get('rol', 'Desconocido')}")
            with st.expander(f"Detalles de {parte.get('rol', 'Parte')}"):
                col1_p, col2_p = st.columns(2)
                with col1_p:
                    parte["nombre"] = st.text_input(f"Nombre", value=parte.get("nombre", ""), disabled=not st.session_state.editing, key=f"nombre_{parte.get('rol', 'parte')}_{i}")
                    parte["nacionalidad"] = st.text_input(f"Nacionalidad", value=parte.get("nacionalidad", ""), disabled=not st.session_state.editing, key=f"nacionalidad_{parte.get('rol', 'parte')}_{i}")
                    parte["tipo_documento"] = st.text_input(f"Tipo Documento", value=parte.get("tipo_documento", ""), disabled=not st.session_state.editing, key=f"tipo_doc_{parte.get('rol', 'parte')}_{i}")
                    parte["tipo_CUIL"] = st.text_input(f"Tipo CUIL", value=parte.get("tipo_CUIL", ""), disabled=not st.session_state.editing, key=f"tipo_cuil_{parte.get('rol', 'parte')}_{i}")
                    parte["estado_civil"] = st.text_input(f"Estado Civil", value=parte.get("estado_civil", ""), disabled=not st.session_state.editing, key=f"estado_civil_{parte.get('rol', 'parte')}_{i}")
                    parte["domicilio"] = st.text_input(f"Domicilio", value=parte.get("domicilio", ""), disabled=not st.session_state.editing, key=f"domicilio_{parte.get('rol', 'parte')}_{i}")
                with col2_p:
                    parte["apellido"] = st.text_input(f"Apellido", value=parte.get("apellido", ""), disabled=not st.session_state.editing, key=f"apellido_{parte.get('rol', 'parte')}_{i}")
                    parte["fecha_nacimiento"] = st.text_input(f"Fecha Nacimiento", value=parte.get("fecha_nacimiento", ""), disabled=not st.session_state.editing, key=f"fecha_nacimiento_{parte.get('rol', 'parte')}_{i}")
                    parte["numero_documento"] = st.text_input(f"Número Documento", value=parte.get("numero_documento", ""), disabled=not st.session_state.editing, key=f"numero_doc_{parte.get('rol', 'parte')}_{i}")
                    parte["numero_CUIL"] = st.text_input(f"Número CUIL", value=parte.get("numero_CUIL", ""), disabled=not st.session_state.editing, key=f"numero_cuil_{parte.get('rol', 'parte')}_{i}")
                    parte["nombre_apellido_conyuge"] = st.text_input(f"Cónyuge", value=parte.get("nombre_apellido_conyuge", ""), disabled=not st.session_state.editing, key=f"conyuge_{parte.get('rol', 'parte')}_{i}")
                    parte["representacion"] = st.text_input(f"Representación", value=parte.get("representacion", ""), disabled=not st.session_state.editing, key=f"representacion_{parte.get('rol', 'parte')}_{i}")
    else:
        st.info("No hay partes intervinientes para mostrar.")

    # ---
    ## Descripción de la Propiedad
    st.subheader("Datos de la Propiedad")
    if "descripcion_propiedad" in data and data["descripcion_propiedad"]:
        propiedad = data["descripcion_propiedad"]
        propiedad["direccion"] = st.text_area("Dirección", value=propiedad.get("direccion", ""), disabled=not st.session_state.editing, key="direccion_propiedad")
        col1_prop, col2_prop = st.columns(2)
        with col1_prop:
            propiedad["Partida"] = st.text_input("Partida", value=propiedad.get("Partida", ""), disabled=not st.session_state.editing, key="partida_propiedad")
            propiedad["superficie"] = st.text_input("Superficie", value=propiedad.get("superficie", ""), disabled=not st.session_state.editing, key="superficie_propiedad")
        with col2_prop:
            propiedad["matricula"] = st.text_input("Matrícula", value=propiedad.get("matricula", ""), disabled=not st.session_state.editing, key="matricula_propiedad")
            propiedad["medidas"] = st.text_input("Medidas", value=propiedad.get("medidas", ""), disabled=not st.session_state.editing, key="medidas_propiedad")

        st.markdown("**Nomenclatura Catastral:**")
        if "nomenclatura_catastral" in propiedad and propiedad["nomenclatura_catastral"]:
            df_nomenclatura = pd.DataFrame(propiedad["nomenclatura_catastral"])
            if st.session_state.editing:
                edited_df = st.data_editor(df_nomenclatura, num_rows="dynamic", key="nomenclatura_catastral_editor")
                propiedad["nomenclatura_catastral"] = edited_df.to_dict('records')
            else:
                st.dataframe(df_nomenclatura, hide_index=True)
        else:
            st.info("No hay datos de nomenclatura catastral para mostrar.")
    else:
        st.info("No hay descripción de propiedad para mostrar.")

    # ---
    ## Valor de Transacción y Observaciones
    st.subheader("Información Adicional")
    data["valor_transaccion"] = st.text_input("Valor de Transacción", value=data.get("valor_transaccion", ""), disabled=not st.session_state.editing, key="valor_transaccion")
    data["observaciones"] = st.text_area("Observaciones", value=data.get("observaciones", ""), disabled=not st.session_state.editing, key="observaciones")
