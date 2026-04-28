import time
import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import frontmatter
import re
from pathlib import Path

class BibliotecarioCompleto(FileSystemEventHandler):
    def __init__(self, ruta_dominios, ruta_verticales, archivo_salida):
        self.ruta_dominios = Path(ruta_dominios)
        self.ruta_verticales = Path(ruta_verticales)s
        self.archivo_salida = archivo_salida
        self.actualizar_todo()

    def procesar_archivo(self, archivo):
        """Extrae la información de un archivo Markdown."""
        try:
            nota = frontmatter.load(archivo)
            # Buscamos el primer párrafo o la sección de Valor Estratégico para el resumen
            contenido = nota.content
            resumen = "Sin descripción"
            if "## 💎 Valor Estratégico" in contenido:
                resumen = contenido.split("## 💎 Valor Estratégico")[1].split("##")[0].strip()
            
            return {
                "id": nota.get("ID", archivo.stem),
                "nombre": nota.get("Nombre", archivo.stem),
                "verticales": nota.get("Verticales", []), # Solo para dominios
                "resumen": resumen,
                "archivo": archivo.name
            }
        except:
            return None

    def actualizar_todo(self):
        """Reconstruye el diccionario con información de ambas carpetas."""
        datos_finales = {
            "verticales": [],
            "dominios": []
        }

        # 1. Procesar Verticales
        for f in self.ruta_verticales.glob("*.md"):
            if f.stem.lower() == "readme": continue
            info = self.procesar_archivo(f)
            if info: datos_finales["verticales"].append(info)

        # 2. Procesar Dominios
        for f in self.ruta_dominios.glob("*.md"):
            if f.stem.lower() == "readme": continue
            info = self.procesar_archivo(f)
            if info: datos_finales["dominios"].append(info)
            
        # Validación de consistencia (opcional: imprimir alertas de verticales huérfanas)
        ids_verticales = {v["id"] for v in datos_finales["verticales"]}
        for d in datos_finales["dominios"]:
            for v_id in d["verticales"]:
                if v_id not in ids_verticales:
                    print(f"⚠️ Alerta: Dominio {d['id']} usa vertical {v_id} no definida.")

        # 3. Guardar el Libro Maestro
        with open(self.archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(datos_finales, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Diccionario sincronizado: {len(datos_finales['verticales'])} Verticales y {len(datos_finales['dominios'])} Dominios.")

    def on_modified(self, event):
        if event.src_path.endswith(".md"):
            self.actualizar_todo()

if __name__ == "__main__":
    # Configuramos las rutas (asegúrate de que estas carpetas existan)
    manejador = BibliotecarioCompleto("./dominios", "./verticales", "./diccionario_maestro_observer.json")
    observador = Observer()
    # Le decimos al observador que mire AMBAS carpetas
    observador.schedule(manejador, "./dominios", recursive=False)
    observador.schedule(manejador, "./verticales", recursive=False)
    observador.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observador.stop()
    observador.join()