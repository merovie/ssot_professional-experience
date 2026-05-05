import os
import frontmatter
import json

def generate_ssot_index(base_path):
    # Estructura ajustada a tu imagen
    index = {
        "verticales": [],
        "dominios": [],
        "empresa": [],
        "portafolio": []
    }

    # Carpetas clave a indexar
    target_folders = ["verticales", "dominios", "empresa", "portafolio"]

    for folder in target_folders:
        folder_path = os.path.join(base_path, folder)
        if not os.path.exists(folder_path):
            continue

        for filename in os.listdir(folder_path):
            if filename.endswith(".md"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    
                    # Metadata mínima para el LLM
                    item = {
                        "id": filename.replace(".md", ""),
                        "path": file_path,
                        "verticales_asociadas": post.get("verticals", []),
                        "dominios_clave": post.get("domains", []),
                        "score": post.get("priority", 0), # Para priorizar proyectos top
                        "snippet": post.content[:150].strip() # Para que el LLM entienda el contexto
                    }
                    index[folder].append(item)

    # Guardar el índice para que el prompt lo use
    with open('ssot_index.json', 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=4, ensure_ascii=False)
    
    return "Índice SSOT actualizado según tu estructura de carpetas."

# Ejecución
# generate_ssot_index('./SSOT_PROFESSIONAL-EXPERIENCE')