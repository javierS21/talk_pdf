import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain


load_dotenv()

pc = Pinecone(api_key = os.environ["PINECONE_API_KEY"])
index = pc.Index("taller")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
vector_store = PineconeVectorStore(embedding = embeddings, index = index)

def load_name_files(path):
    """
    Lista de archivos cargados actualmente en pinecone
    """
    archivos = []
    with open(path, 'r') as file:
        for line in file:
            archivos.append(line.strip())
    return archivos

def save_name_files(path, new_files):
    """
    Verifica que cualquier archivo a subir, no se repita 
    """
    old_files = load_name_files(path) # lista con los nombres de archivos cargados actualmente

    with open(path, 'a') as file: # abre el archivo en modo append para agregar cosas al final sin borrar lo que ya hay
        for item in new_files:
            if item not in old_files:
                file.write(item+"\n")
                old_files.append(item)
    return old_files

def clean_files(path):
    with open(path, 'w') as file: # modo escritura que borra todo el contenido 
        pass
    index.delete(delete_all=True)
    return True

def text_to_pinecone(pdf):
    try:
        temp_dir = tempfile.TemporaryDirectory()
        temp_filepath = os.path.join(temp_dir.name, pdf.name)
        with open(temp_filepath, "wb") as f:
            f.write(pdf.getvalue())
        loader = PyPDFLoader(temp_filepath)
        text = loader.load()
        with st.spinner(f"Creando embedding de documento: {pdf.name}"):
            create_embeddings(pdf.name, text)
        return True
    except Exception as e:
        st.error(f"Error al procesar {pdf.name}: {str(e)}")
        return False
    

def create_embeddings(file_name, text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 100,
        length_function = len
    )
    chunks = text_splitter.split_documents(text) 
    vector_store.add_documents(documents=chunks)

def process_question(question):

    llm = ChatOpenAI(model_name = "gpt-4o-mini")
    chain = load_qa_chain(llm, chain_type = "stuff")
    docs = vector_store.similarity_search(question, 2)
    respuesta = chain.run(input_documents = docs, question= question)
    return respuesta
