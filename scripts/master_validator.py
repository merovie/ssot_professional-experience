import os
import json
import frontmatter
from pathlib import Path

class SSoTValidator:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.portfolio_path = self.base_path / "portafolio"
        self.domains_path = self.base_path / "dominios"
        self.verticals_path = self.base_path / "verticales"
        self.empresa_path = self.base_path / "empresa"
        self.json_master = self.base_path / "diccionario_maestro_observer.json"
        self.errors = 0

    def log_error(self, message):
        print(f"❌ {message}")
        self.errors += 1

    def validate_metadata_and_relations(self):
        """Valida que los proyectos tengan metadatos correctos y apacen a dominios/verticales existentes."""
        print("🔍 Validando Portafolio y Relaciones...")
        
        dominios_existentes = {f.stem for f in self.domains_path.glob("*.md")}
        empresas_existentes = {f.stem for f in self.empresa_path.glob("*.md")}
        # Asumiendo que las verticales siguen el patrón V1, V2...
        verticales_existentes = {f.stem.split('_')[0] for f in self.verticals_path.glob("*.md") if "_" in f.name}

        for md_file in self.portfolio_path.rglob("*.md"):
            if md_file.name.lower() == "readme.md": continue
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    
                    # 1. Validar campos obligatorios
                    for field in ["ID", "Empresa", "Verticales", "Dominios"]:
                        if field not in post:
                            self.log_error(f"Metadata faltante [{field}] en {md_file.name}")

                    # 1.1 Validar existencia de la Empresa
                    empresa_ref = post.get("Empresa")
                    if empresa_ref and empresa_ref not in empresas_existentes:
                        self.log_error(f"Empresa '{empresa_ref}' no encontrada en /empresa/ para el proyecto {md_file.name}")

                    # 2. Validar Dominios
                    for dom in post.get("Dominios", []):
                        clean_dom = dom.replace("#", "")
                        if clean_dom not in dominios_existentes:
                            self.log_error(f"Dominio inexistente '{dom}' referenciado en {md_file.name}")

                    # 3. Validar Verticales
                    for vert in post.get("Verticales", []):
                        if vert not in verticales_existentes:
                            self.log_error(f"Vertical inexistente '{vert}' referenciada en {md_file.name}")
                            
            except Exception as e:
                self.log_error(f"Error procesando {md_file.name}: {e}")

    def validate_empresa_links(self):
        """Verifica que los links en /empresa apuntan a proyectos que existen."""
        print("🔍 Validando Conexiones Empresa -> Portafolio...")
        for md_file in self.empresa_path.glob("*.md"):
            if md_file.name.lower() == "readme.md": continue
            
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Buscamos links tipo [Texto](../portafolio/ruta/archivo.md)
                if "../portafolio/" in content:
                    import re
                    links = re.findall(r'(\.\./portafolio/[\w\-/]+\.md)', content)
                    for link in links:
                        target_path = (self.empresa_path / link).resolve()
                        if not target_path.exists():
                            self.log_error(f"Link roto en {md_file.name}: {link}")

    def validate_json_sync(self):
        """Verifica que el JSON maestro refleje los archivos en disco."""
        print("🔍 Validando Sincronización con diccionario_maestro_observer.json...")
        if not self.json_master.exists():
            self.log_error("No se encuentra el archivo diccionario_maestro_observer.json")
            return

        try:
            with open(self.json_master, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            self.log_error("El archivo JSON maestro tiene errores de sintaxis.")
            return
            
        dominios_json = {d['archivo'] for d in data.get('dominios', [])}
        dominios_disco = {f.name for f in self.domains_path.glob("*.md") if f.stem.lower() != "readme"}
        
        verticales_json = {v['archivo'] for v in data.get('verticales', [])}
        verticales_disco = {f.name for f in self.verticals_path.glob("*.md") if f.stem.lower() != "readme"}

        # Validación de Dominios
        
        # Diferencia entre disco y JSON
        missing_in_json = dominios_disco - dominios_json
        if missing_in_json:
            self.log_error(f"Archivos de dominio no registrados en JSON: {missing_in_json}")

        # Validación de Verticales
        missing_verts = verticales_disco - verticales_json
        if missing_verts:
            self.log_error(f"Archivos de verticales no registrados en JSON: {missing_verts}")

    def run_all(self):
        print("="*60)
        print("🚀 INICIANDO SUITE DE VALIDACIÓN SSoT")
        print("="*60)
        
        self.validate_metadata_and_relations()
        self.validate_empresa_links()
        self.validate_json_sync()
        
        print("\n" + "="*60)
        if self.errors == 0:
            print("✅ VALIDACIÓN EXITOSA: El repositorio es íntegro.")
        else:
            print(f"❌ VALIDACIÓN FALLIDA: Se encontraron {self.errors} errores.")
        print("="*60)

if __name__ == "__main__":
    validator = SSoTValidator()
    validator.run_all()