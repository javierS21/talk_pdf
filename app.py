import streamlit as st
import os 
from utils import *

# Ruta donde se guarda la lista de archivos almacenados 
FILE_LIST = "archivos.txt"

# Configuracion de la pagina
st.set_page_config(page_title = 'preguntaDOC', layout= "centered")
st.title("Pregunta a tu PDF")

archivos = load_name_files(FILE_LIST)

with st.sidebar:
    st.header("Subir archivos PDF")

    files_uploaded = st.file_uploader(
        label = "Carga tu(s) archivo PDF",
        type='pdf',
        accept_multiple_files = True
    )

    if st.button('Procesar'):
        nuevos_archivos = []
        for pdf in files_uploaded:
            if pdf is not None and pdf.name not in archivos:
                st.info(f"Procesando {pdf.name}")
                if text_to_pinecone(pdf):
                    nuevos_archivos.append(pdf.name)
        if nuevos_archivos:
            archivos = save_name_files(FILE_LIST, nuevos_archivos)
            st.success("Documentos procesados correctamente.")

    if archivos:
        
        lista_documentos = st.empty() # Crea un hueco dinámico para poner o quitar información en la app
        with lista_documentos.container():  # abre el contenedor creado arriba. Todo lo que este dentro del bloque serpa insertado en ese hueco creado. 
            for arch in archivos: 
                st.write(arch)
            if st.button("Borrar Todos los Archivos"):
                archivos = []
                clean_files(FILE_LIST) 
                lista_documentos.empty() # vacía el contenedor lista_documentos
                


if archivos:
    st.markdown("### Haz una pregunta sobre los documentos: ")
    user_question = st.text_input("Pregunta: ")

    if user_question:
        with st.spinner("Pensando..."):
            respuesta = process_question(user_question)
        st.markdown("### Respuesta: ")
        st.write(respuesta)