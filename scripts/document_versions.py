import os
import re
from pathlib import Path
from datetime import datetime

def format_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def generar_documentacion_automatica():
    """
    Escanea archivos app*.py para documentar la evolución del consultor ACTA.
    """
    base_path = Path(__file__).parent.parent
    output_file = base_path / "DOCUMENTACION_VERSIONS.md"
    
    # Buscar todos los archivos que coincidan con el patrón app*.py
    apps = sorted(list(base_path.glob("app*.py")), key=lambda x: x.name)
    
    last_metadata = {}
    
    with open(output_file, "w", encoding="utf-8") as doc:
        doc.write("# 📑 Registro Evolutivo de Versiones - ACTA\n\n")
        doc.write(f"*Generado automáticamente el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*\n\n")
        doc.write("Su objetivo es trazar la evolución de los modelos, motores de voz y reglas de negocio.\n\n")
        
        for app in apps:
            # Identificar versión por nombre de archivo
            version_match = re.search(r"v(\d+)", app.name)
            v_label = f"Iteración {version_match.group(1)}" if version_match else "Versión 1 (Lanzamiento)"
            
            stats = app.stat()
            fecha_creacion = format_time(stats.st_ctime)
            fecha_modificacion = format_time(stats.st_mtime)

            with open(app, "r", encoding="utf-8") as f:
                content = f.read()
                
                # Extracción de metadatos mediante Regex
                # Corregido regex para capturar el valor entre comillas
                modelo = re.search(r"MODEL_TEXTO\s*=\s*['\"]([^'\"]+)['\"]", content)
                modelo_str = modelo.group(1) if modelo else "Gemini Flash (Legacy)"
                
                # Detección de motor de audio
                if "texttospeech.TextToSpeechClient" in content:
                    audio = "Google Cloud TTS (Voz Neuronal HD)"
                elif "gTTS" in content:
                    audio = "gTTS (Standard Web)"
                elif "lyria" in content.lower():
                    audio = "Google Lyria (Experimental)"
                else:
                    audio = "Sin Audio / Solo Texto"
                
                # Extracción del bloque de contexto SSoT
                contexto_match = re.search(r"contexto = (?:\"\"\"|''')(.*?)(?:\"\"\"|''')", content, re.DOTALL)
                contexto_txt = contexto_match.group(1).strip() if contexto_match else "Carga dinámica / Externa"

                # Extracción de objetivo (opcional, busca línea "# Objetivo: ...")
                objetivo_match = re.search(r"# Objetivo:\s*(.*)", content)
                objetivo_txt = objetivo_match.group(1).strip() if objetivo_match else "No especificado en el código."

                doc.write(f"## 💎 {v_label} (`{app.name}`)\n")
                doc.write(f"- **📅 Creado:** `{fecha_creacion}`\n")
                doc.write(f"- **📝 Última Modif:** `{fecha_modificacion}`\n")
                doc.write(f"- **🎯 Objetivo:** {objetivo_txt}\n")
                doc.write(f"- **Cerebro (LLM):** `{modelo_str}`\n")
                doc.write(f"- **Interfaz Vocal:** `{audio}`\n")
                
                # Análisis de cambios respecto a la versión anterior
                if last_metadata:
                    cambios = []
                    if last_metadata.get('modelo') != modelo_str:
                        cambios.append(f"Actualización de modelo: {last_metadata['modelo']} ➔ {modelo_str}")
                    if last_metadata.get('audio') != audio:
                        cambios.append(f"Cambio de motor de voz: {last_metadata['audio']} ➔ {audio}")
                    if last_metadata.get('contexto') != contexto_txt:
                        cambios.append("Modificación en la definición de perfil (SSoT Interno)")
                    
                    if cambios:
                        doc.write("- **🔄 Cambios detectados:**\n")
                        for c in cambios: doc.write(f"  - {c}\n")

                doc.write(f"- **📜 Contexto Detectado:**\n")
                doc.write(f"```text\n{contexto_txt}\n```\n\n")
                doc.write("---\n")

                # Guardar estado para la siguiente comparación
                last_metadata = {
                    'modelo': modelo_str,
                    'audio': audio,
                    'contexto': contexto_txt
                }

    print(f"✅ Documentación actualizada con {len(apps)} versiones en: {output_file}")

if __name__ == "__main__":
    generar_documentacion_automatica()