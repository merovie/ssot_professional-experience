import os
import frontmatter
from pathlib import Path

def buscar_dominios_no_utilizados():
    """
    Identifica dominios definidos que no están asociados a ningún proyecto en el portafolio.
    """
    base_path = Path(__file__).parent.parent
    portfolio_path = base_path / "portafolio"
    domains_path = base_path / "dominios"

    # 1. Obtener el conjunto de todos los dominios definidos (ID limpio sin #)
    # Usamos el nombre del archivo (stem) ya que es la fuente de verdad
    dominios_definidos = {f.stem: f.name for f in domains_path.glob("*.md") if f.stem.lower() != "readme"}
    
    dominios_usados = set()
    archivos_analizados = 0

    print("🔍 Analizando el uso de dominios en el portafolio...\n")

    # 2. Rastrear todos los dominios mencionados en el portafolio
    for archivo_md in portfolio_path.rglob("*.md"):
        if archivo_md.name.lower() == "readme.md":
            continue
            
        archivos_analizados += 1
        try:
            with open(archivo_md, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                refs = post.get("Dominios", [])
                
                if isinstance(refs, list):
                    for ref in refs:
                        # Limpiamos el prefijo '#' para comparar con el nombre del archivo
                        nombre_limpio = ref.replace("#", "")
                        dominios_usados.add(nombre_limpio)
        except Exception as e:
            print(f"💥 Error leyendo {archivo_md.name}: {e}")

    # 3. Calcular la diferencia
    set_definidos = set(dominios_definidos.keys())
    huerfanos = set_definidos - dominios_usados

    # 4. Reporte de resultados
    print("="*50)
    print(f"📊 Resumen de Cobertura:")
    print(f"   - Proyectos revisados: {archivos_analizados}")
    print(f"   - Total dominios definidos: {len(set_definidos)}")
    print(f"   - Dominios en uso: {len(dominios_usados & set_definidos)}")
    print("="*50 + "\n")

    if not huerfanos:
        print("✅ ¡Excelente! Todos tus dominios están indexados en al menos un proyecto.")
    else:
        print(f"⚠️ Se encontraron {len(huerfanos)} dominios sin indexar (no aparecen en el portafolio):")
        for h in sorted(huerfanos):
            print(f"   [-] {h}")
        print("\n💡 Sugerencia: Considera asociarlos a un proyecto o revisar si falta documentación.")
    print("="*50)

if __name__ == "__main__":
    buscar_dominios_no_utilizados()