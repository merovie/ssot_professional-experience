---
ID: "estimacion_cp"
Macro_Asociado: "mina_cmp"
Verticales: ["V1", "V3"]
Dominios: ["EstimacionRecursos", "TechnicalTranslation", "MVP"]
---

# Estimación de Recursos de Corto Plazo

## 🚩 Situación y Tarea (S-T)
**Contexto:** El modelo de largo plazo carecía de la resolución necesaria para capturar la complejidad estructural requerida para el diseño de disparos semanales.
**El Desafío:** Construir modelos de bloques locales de alta resolución que integraran la información de los pozos de tronadura y el mapeo de bancos para la toma de decisiones inmediata.

## 🛠️ Acción (A)
* **Modelamiento de Dominios Geológicos:** Actualicé los wireframes de litología y alteración basándome en la evidencia de los frentes de carguío activos.
* **Interpolación Local:** Utilicé Kriging Ordinario con parámetros optimizados para mallas densas de datos para estimar las leyes en bloques de 5x5x5 metros.
* **Validación Cruzada:** Realicé comparaciones visuales y estadísticas (swath plots) entre los datos de muestra y los valores estimados para asegurar la consistencia del modelo.

## 📈 Resultado (R)
* **Precisión en el Plan Semanal:** El modelo de corto plazo permitió predecir la ley de alimentación con un error inferior al 3% respecto a lo real.
* **Soporte al Diseño de Minado:** Facilitó la definición precisa de las líneas de "dig-lines", minimizando la pérdida de mineral en los bordes de los cuerpos.

---
ID: "estimacion-cp-kriging-01"
Macro_Asociado: "cmp-operaciones"
Verticales: ["V2", "V4"]
Dominios: [
  "EstimacionRecursos",
  "Geoestadistica",
  "AnalisisDeDatos",
  "OreControl"
]
---

# 📊 Proyecto: OEstimación de Corto Plazo y Caracterización Textural

| Atributo | Detalle |
| :--- | :--- |
| **Compañía** | Compañía Minera del Pacífico (CMP) |
| **Software** | Vulcan, Isatis.neo |
| **Metodología** | Kriging Ordinario vs. Inverso a la Distancia (IDW) |
| **Datos** | Análisis químicos de Pozos de Tronadura (Blast holes) |

## Situación y Tarea (S-T)
En la operación de CMP, la estimación de corto plazo se basaba tradicionalmente en la metodología de Inverso a la Distancia (IDW). Mi objetivo fue evaluar y migrar hacia una estimación por **Kriging**, buscando mejorar la representatividad de las leyes y reducir el error en la discriminación de mineral/estéril. La tarea consistió en realizar un flujo completo de estimación técnica para validar si el Kriging ofrecía una mejora sustancial frente a la práctica tradicional.

## Acción (A): Flujo de Trabajo Geoestadístico
Implementé un riguroso proceso de evaluación técnica que incluyó:

* **Análisis Exploratorio de Datos (EDA):** Realicé un diagnóstico estadístico profundo de los análisis químicos de los *blast holes*, identificando poblaciones, valores atípicos y comportamientos de las leyes por dominio.
* **Benchmarking IDW vs. Kriging:** Realicé una comparativa crítica entre ambas metodologías, detectando las deficiencias del IDW (como el suavizado excesivo) y las ventajas de precisión del Kriging en la definición de contactos.
* **Diferenciación de Hierro ($FeT$ vs. $FeM$):** Realicé la estimación separada del Hierro Total y el **Hierro Magnético**, variable crítica para determinar la recuperabilidad real en las etapas de concentración magnética.
* **Análisis del Modelo Geológico y Texturas:** Utilicé el modelo geológico para discernir y categorizar el material según su textura: **Brecha, Masivo o Diseminado**. En minería de hierro, esta distinción es vital para predecir el rendimiento de planta y la fragmentación.
* **Análisis Exploratorio y Variografía:** Ejecuté el EDA y modelamiento variográfico de los análisis químicos de los *blast holes*, capturando la continuidad espacial de las leyes dentro de cada dominio textural.
* **Estimación por Kriging:** Ejecuté la estimación de leyes asegurando un comportamiento insesgado, contrastando los resultados mediante validación cruzada frente a la metodología tradicional de Inverso a la Distancia (IDW).
* **Transferencia a Planificación:** Actué como el puente técnico para entregar a Planificación de Corto Plazo no solo un valor de ley, sino una descripción cualitativa y cuantitativa del material a extraer para ajustar la secuencia de minado.

## Resultado (R)
* **Mejora en la Precisión de Leyes:** Se detectaron mejoras significativas en la representatividad del modelo de corto plazo al utilizar Kriging, reduciendo la incertidumbre en los frentes de extracción.
* **Optimización de la Selectividad:** La validación cruzada confirmó que el Kriging permitía una mejor discriminación de bloques, impactando positivamente en la reducción de la dilución operativa.
* **Sustento para el Cambio Metodológico:** Los resultados del EDA y las validaciones proporcionaron el respaldo técnico necesario para justificar la transición de la metodología tradicional hacia flujos geoestadísticos más robustos.
* **Impacto en Reconciliación:** La adopción de este flujo mejoró la confiabilidad de los pronósticos de producción diarios y semanales al estar basados en un modelo de leyes con mayor rigor científico.
* **Superación del Estándar Tradicional:** Las mejoras halladas mediante Kriging frente al IDW validaron un cambio metodológico hacia modelos más robustos y menos suavizados.
* **Sustento del Plan Minero:** Se garantizó que la información entregada a planificación fuera accionable, reduciendo las desviaciones en planta debido a variaciones texturales no previstas.



