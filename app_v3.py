import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# --- 1. CONFIGURACIÓN DE SEGURIDAD Y MODELOS ---
# Acceso centralizado a la Single Source of Truth de configuración
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("Error: Configura 'GEMINI_API_KEY' en .streamlit/secrets.toml")
        st.stop()
except Exception as e:
    st.error(f"Falla en la infraestructura: {e}")
    st.stop()

# Motores de IA actualizados a 2026
MODEL_TEXTO = 'models/gemini-2.5-flash'

# --- 2. CONFIGURACIÓN DE PÁGINA E INTERFAZ ---
st.set_page_config(page_title="ACTA - Consultor de Experiencia", page_icon="💎", layout="wide")

st.title("💎 ACTA: Consultor de Experiencia")
st.markdown("""
Bienvenido al ecosistema de **ACTA**. Este consultor articula mi trayectoria profesional 
utilizando un repositorio **SSoT** para garantizar respuestas precisas y basadas en evidencia.
""")

# Barra lateral para personalización de la experiencia del usuario
with st.sidebar:
    st.header("Preferencias de Salida")
    modo_respuesta = st.radio(
        "¿Cómo prefieres recibir la información?",
        ["Solo Texto", "Texto + Audio", "Solo Audio"],
        help="Elige 'Solo Audio' para una narración automática."
    )
    st.divider()
    st.caption("ACTA v2.1 | Geociencias & Innovación")
    st.caption("Motor: Gemini 2.5 Flash + gTTS")

# --- 3. LÓGICA DEL SSoT (Contexto Profesional) ---
def obtener_contexto_ssot():
    """
    Representa el núcleo analítico del consultor. 
    Basado en el enfoque de geociencias analíticas y liderazgo innovador.
    """
    # En futuras versiones, aquí se integra la lectura de tus archivos .md
    contexto = """
    Perfil: Geocientífica Senior y Arquitecta de Valor con +10 años de experiencia.
    Especialidad: Geostadística, analítica de datos y gestión de portafolios R&D.
    Estilo de Liderazgo: Articulación y alineación estratégica de stakeholders.
    Proyectos Clave: Innovación minera, fondos CORFO/ANID, transformación digital.
    """
    return contexto

# --- 4. FLUJO DE CHAT Y GENERACIÓN ---
if prompt := st.chat_input("Consulta sobre mi portafolio, liderazgo o formación..."):
    
    # Registro visual de la consulta
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        contexto = obtener_contexto_ssot()
        
        # Prompt maestro con restricciones de marca ACTA
        full_prompt = f"""
        Actúa como el consultor oficial de la marca ACTA. 
        Tu objetivo es articular la experiencia de la profesional basándote en este SSoT: {contexto}
        
        REGLAS CRÍTICAS:
        1. No uses 'gestionar stakeholders', usa 'articular' o 'alinear'.
        2. Mantén un tono analítico, basado en evidencia y orientado a la innovación.
        3. Sé conciso y directo.
        
        Pregunta del usuario: {prompt}
        """
        
        try:
            # 4.1. Generación del pensamiento analítico (Texto)
            model = genai.GenerativeModel(MODEL_TEXTO)
            response = model.generate_content(full_prompt)
            texto_respuesta = response.text
            
            # 4.2. Control de visualización según preferencia
            if modo_respuesta != "Solo Audio":
                st.markdown(texto_respuesta)
            else:
                st.info("🔊 Generando narración profesional de ACTA...")

            # 4.3. Articulación de Audio (Multimodalidad)
            if modo_respuesta in ["Texto + Audio", "Solo Audio"]:
                with st.spinner("Sintetizando audio..."):
                    # gTTS proporciona una salida de audio estable y clara
                    tts = gTTS(text=texto_respuesta[:600], lang='es', tld='com.mx')
                    audio_fp = io.BytesIO()
                    tts.write_to_fp(audio_fp)
                    
                    # Autoplay activo solo si el usuario eligió 'Solo Audio'
                    st.audio(
                        audio_fp.getvalue(), 
                        format="audio/mp3", 
                        autoplay=(modo_respuesta == "Solo Audio")
                    )
                        
        except Exception as e:
            st.error(f"Error en la articulación de la respuesta: {e}")