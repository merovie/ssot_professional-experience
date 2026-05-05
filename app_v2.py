import streamlit as st
import google.generativeai as genai
import os
from pathlib import Path

# --- 1. CONFIGURACIÓN DE SEGURIDAD Y MODELOS ---
# Usamos los secretos de Streamlit para proteger tu API Key
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("Error: No se encontró la GEMINI_API_KEY en los secretos.")
        st.stop()
except Exception as e:
    st.error(f"Error de configuración: {e}")
    st.stop()

# Definimos los modelos según el diagnóstico realizado
MODEL_TEXTO = 'models/gemini-2.5-flash'
MODEL_AUDIO = 'models/lyria-3'

# --- 2. INTERFAZ DE USUARIO (UI) ---
st.set_page_config(page_title="ACTA - test AUDIO", page_icon="💎")

st.title("💎 ACTA: TEST")
st.markdown("""
Bienvenido al consultor inteligente de **ACTA**. 
Este sistema utiliza un **SSoT** para responder basado en mi trayectoria real en geociencias e innovación.
""")

# Configuración en la barra lateral
with st.sidebar:
    st.header("Preferencias")
    modo_respuesta = st.radio(
        "¿Cómo quieres la respuesta?",
        ["Solo Texto", "Texto + Audio"],
        help="El modo audio utiliza Lyria 3 para una narración profesional."
    )
    st.divider()
    st.caption("Versión 2.0 - Motor Gemini 2.5 Flash")

# --- 3. LÓGICA DEL SSoT (Carga de Contexto) ---
def obtener_contexto_ssot():
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

# --- 4. FLUJO PRINCIPAL DEL CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.contexto = obtener_contexto_ssot()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Consulta sobre mi experiencia..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 4.2. Generar respuesta del asistente
    with st.chat_message("assistant"):
        
        # Construimos el prompt con las correcciones de estilo (articular/alinear)
        full_prompt = f"""{st.session_state.contexto}
        
        Actúa como el consultor profesional de ACTA.
        Reglas de estilo: No uses 'gestionar stakeholders', usa 'articular' o 'alinear'. 
        Tu enfoque debe ser analítico y data-driven.
        
        Pregunta del usuario: {prompt}
        """
        
        try:
            # Generación de Texto
            model = genai.GenerativeModel(MODEL_TEXTO)
            response = model.generate_content(full_prompt)
            texto_respuesta = response.text
            st.markdown(texto_respuesta)
            st.session_state.messages.append({"role": "assistant", "content": texto_respuesta})
            
            # Generación de Audio (si se solicita)
            # Generación de Audio (Sintaxis compatible)
            if modo_respuesta == "Texto + Audio":
                with st.spinner("Sintetizando voz..."):
                    try:
                        # Usamos el modelo para generar el audio de forma compatible
                        audio_response = model.generate_content(
                            f"Lee este texto con voz clara y profesional: {texto_respuesta[:500]}",
                            generation_config={"response_mime_type": "audio/mpeg"}
                        )
                        
                        if audio_response.data:
                            st.audio(audio_response.data, format="audio/mp3")
                    except Exception as audio_err:
                        st.warning("El modelo actual no soporta salida directa de audio. Usando TTS alternativo...")
                        # Opción de respaldo rápida
                        st.tts(texto_respuesta[:500])
                        
        except Exception as e:
            st.error(f"Hubo un problema al procesar la respuesta: {e}")