📄 Pregunta a tu PDF
Una aplicación web creada con Streamlit, LangChain, Pinecone y OpenAI, que permite cargar documentos PDF y hacerles preguntas en lenguaje natural usando inteligencia artificial.

🚀 ¿Qué hace esta app?
Carga y procesa archivos PDF.

Genera embeddings del contenido usando modelos de HuggingFace.

Almacena vectores en Pinecone para búsqueda semántica.

Responde preguntas usando GPT-4o de OpenAI.

Muestra una interfaz amigable y accesible vía Streamlit.

🛠️ Tecnologías utilizadas
Streamlit – interfaz web

LangChain – framework para agentes con LLMs

OpenAI – modelo de lenguaje para generar respuestas

Pinecone – vector store para búsquedas semánticas

sentence-transformers – generación local de embeddings

PyPDF – extracción de texto desde archivos PDF

📁 Estructura del proyecto
app.py → Interfaz principal con Streamlit

utils.py → Funciones para procesamiento y consultas

archivos.txt → Lista de archivos procesados

requirements.txt → Lista de dependencias

.env.example → Archivo de ejemplo con variables de entorno

README.md → Este documento