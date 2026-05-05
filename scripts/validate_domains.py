import os
import frontmatter
from pathlib import Path

def validar_conexiones_dominios():
    # Configuración de rutas relativas basadas en tu estructura
    base_path = Path(__file__).parent.parent
    portfolio_path = base_path / "portafolio"
    domains_path = base_path / "dominios"

    # 1. Obtener todos los dominios existentes (nombres de archivos .md)
    # Limpiamos el nombre para comparar (ej: "StakeholderManagement.md" -> "StakeholderManagement")
    existentes = {f.stem for f in domains_path.glob("*.md")}
    
    errores_encontrados = 0
    archivos_procesados = 0

    print("🔍 Iniciando validación de dominios en el portafolio...\n")

    # 2. Recorrer archivos del portafolio (recursivo)
    for archivo_md in portfolio_path.rglob("*.md"):
        if archivo_md.name.lower() == "readme.md":
            continue
            
        archivos_procesados += 1
        try:
            with open(archivo_md, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                
                dominios_referenciados = post.get("Dominios", [])
                
                # Si no es una lista (error de formato en YAML), lo manejamos
                if not isinstance(dominios_referenciados, list):
                    print(f"❌ [FORMATO] {archivo_md.relative_to(base_path)}: 'Dominios' debe ser una lista.")
                    errores_encontrados += 1
                    continue

                for dom_ref in dominios_referenciados:
                    # Quitamos el '#' para comparar con el nombre del archivo
                    nombre_limpio = dom_ref.replace("#", "")
                    
                    if nombre_limpio not in existentes:
                        print(f"❌ [MISSING] {archivo_md.relative_to(base_path)}:")
                        print(f"   ⚠️ El dominio '{dom_ref}' no tiene un archivo correspondiente en /dominios/{nombre_limpio}.md")
                        errores_encontrados += 1
                        
        except Exception as e:
            print(f"💥 Error procesando {archivo_md.name}: {e}")

    # 3. Resumen final
    print("\n" + "="*40)
    print(f"📊 Resumen de Validación:")
    print(f"   - Archivos analizados: {archivos_processed}")
    print(f"   - Archivos de dominio en sistema: {len(existentes)}")
    
    if errores_encontrados == 0:
        print(f"✅ ¡Todo perfecto! Todas las conexiones son íntegras.")
    else:
        print(f"❌ Se encontraron {errores_encontrados} inconsistencias.")
    print("="*40)

if __name__ == "__main__":
    validar_conexiones_dominios()
