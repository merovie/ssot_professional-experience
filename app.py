import streamlit as st
import google.generativeai as genai
from pathlib import Path

# --- CONFIGURACIÓN ACTA ---
st.set_page_config(page_title="Melissa Rodríguez", page_icon="💎")
st.title("💎 Growth | Desarrollo Negocios | Geociencias | Tecnología")

# Configuración SEGURA de la API
# Aquí st.secrets buscará una etiqueta llamada "GEMINI_API_KEY"
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Falta la configuración de la API Key en los secretos de Streamlit.")
    st.stop()

model = genai.GenerativeModel('gemini-1.5-flash')

# --- CARGA DEL REPOSITORIO (SSoT) ---
def cargar_contexto_ssot():
    base_path = Path(__file__).parent
    contexto = "ERES EL ASISTENTE PROFESIONAL DE UNA GEOCIENTÍFICA SENIOR.\n"
    contexto += "USA EXCLUSIVAMENTE ESTA BASE DE DATOS PARA RESPONDER:\n\n"
    
    for folder in ["dominios", "portafolio"]:
        path = base_path / folder
        if path.exists():
            for file in path.rglob("*.md"):
                with open(file, 'r', encoding='utf-8') as f:
                    contexto += f"\n--- ORIGEN: {file.name} ---\n{f.read()}\n"
    return contexto

# --- LÓGICA DEL CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.contexto = cargar_contexto_ssot()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Consulta sobre mi experiencia o dominios técnicos..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Enviamos el contexto completo + la pregunta
        full_prompt = f"{st.session_state.contexto}\n\nPregunta del reclutador: {prompt}"
        response = model.generate_content(full_prompt)
        
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})