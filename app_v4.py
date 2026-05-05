import streamlit as st
import google.generativeai as genai
from google.cloud import texttospeech
from google.oauth2 import service_account
import io

# --- 1. CONFIGURACIÓN DE SEGURIDAD (SSoT) ---
# Articulamos la infraestructura de seguridad desde los secretos de Streamlit
try:
    # Configuración de Gemini
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("Error: GEMINI_API_KEY no encontrada en secrets.")
        st.stop()
    
    # Configuración de Google Cloud TTS (v4 - Sin archivos físicos)
    gcp_info = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(gcp_info)
    client_tts = texttospeech.TextToSpeechClient(credentials=credentials)
    
except Exception as e:
    st.error(f"Falla en la infraestructura de seguridad de la v4: {e}")
    st.stop()

# Motores de IA
MODEL_TEXTO = 'models/gemini-2.5-flash'

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="REPO v4 - AUDIO GOOGLE", page_icon="💎", layout="wide")

st.title("💎 AUDIO GOOGLE CLOUD")
st.markdown("""
Bienvenido al ecosistema **MRV**. Esta interfaz articula mi trayectoria en geociencias 
e innovación mediante un repositorio de **Single Source of Truth (SSoT)**.
""")

# Barra lateral para preferencias
with st.sidebar:
    st.header("Preferencias")
    modo_respuesta = st.radio(
        "¿Cómo quieres recibir la información?",
        ["Solo Texto", "Texto + Audio", "Solo Audio"],
        help="El modo 'Solo Audio' utiliza voces neuronales de alta fidelidad."
    )
    st.divider()
    st.caption("v4.0 | Enfoque Analítico & Data-Driven")

# --- 3. LÓGICA DEL SSoT ---
def obtener_contexto_ssot():
    # Base de conocimiento alineada con tu trayectoria real
    contexto = """
    Perfil: Geocientífica Senior con enfoque comercial y +10 años en minería técnica.
    Especialidad: Venta consultiva, geostadística analítica e innovación R&D.
    Habilidades: Articular soluciones de negocio y alinear stakeholders estratégicos.
    Enfoque: Generación de valor económico, mitigación de incertidumbre y optimización de EBITDA.
    """
    return contexto

# --- 4. FUNCIÓN DE VOZ NEURONAL MEXICANA ---
def generar_audio_v4(texto):
    try:
        synthesis_input = texttospeech.SynthesisInput(text=texto[:800])
        
        # Identidad vocal: Mexicana, profesional y líder
        voice = texttospeech.VoiceSelectionParams(
            language_code="es-US",
            name="en-US-Chirp3-HD-Aoede"
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0
        )

        response = client_tts.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        return response.audio_content
    except Exception as e:
        st.error(f"Error en la síntesis de voz: {e}")
        return None

# --- 5. FLUJO PRINCIPAL ---
if prompt := st.chat_input("Consulta sobre mi portafolio o innovación..."):
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        contexto = obtener_contexto_ssot()
        
        # Prompt maestro con reglas de estilo de marca
        full_prompt = f"""
        Actúa como el consultor experto de ACTA. 
        Contexto de la experta: {contexto}
        
        REGLAS:
        - No uses 'gestionar stakeholders', usa 'articular' o 'alinear'.
        - Tu enfoque es analítico y data-driven.
        - Responde de forma ejecutiva y profesional.
        
        Pregunta: {prompt}
        """
        
        try:
            model = genai.GenerativeModel(MODEL_TEXTO)
            response = model.generate_content(full_prompt)
            texto_respuesta = response.text
            
            # Visualización adaptativa
            if modo_respuesta != "Solo Audio":
                st.markdown(texto_respuesta)
            else:
                st.info("🔊 Articulando respuesta por audio...")

            # Ejecución de audio multimodal
            if modo_respuesta in ["Texto + Audio", "Solo Audio"]:
                audio_content = generar_audio_v4(texto_respuesta)
                if audio_content:
                    st.audio(
                        audio_content, 
                        format="audio/mp3", 
                        autoplay=(modo_respuesta == "Solo Audio")
                    )
                        
        except Exception as e:
            st.error(f"Error en el procesamiento: {e}")