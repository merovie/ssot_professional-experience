---
ID: "estimacion_mp"
Macro_Asociado: "mina_cmp"
Verticales: ["V1"]
Dominios: ["QAQC", "OreControl", "AuditoriaTecnica", "EstimacionRecursos", "StakeholderManagement", "TechnicalTranslation", "InteroperabilidadTecnica"]
---

# Estimación de Recursos de Mediano Plazo (Sondajes Multibanco y Diseño de Malla)

## 🚩 Situación y Tarea (S-T)
El desafío consistía en generar un modelo de bloques robusto para la planificación trimestral, extendiendo la estimación a **3 bancos** de profundidad. La complejidad radicaba en la integración de fuentes de datos con distinta jerarquía de precisión: sondajes diamantinos (DDH), perforaciones de aire reverso (RC) y pozos de tronadura (blastholes). Mi responsabilidad incluía el diseño de la campaña de perforación interbanco y la consolidación de un modelo que minimizara la incertidumbre geológica en el avance de la mina.

## 🛠️ Acción (A): Diseño, Coordinación y Ponderación Geoestadística
Lideré el flujo de trabajo desde el diseño físico hasta la validación del modelo:

* **Diseño de Malla de Perforación (RC):** Diseñé la malla de perforaciones de aire reverso para el muestreo interbanco, optimizando la cobertura espacial para alimentar el modelo de mediano plazo.
* **Gestión de Stakeholders (P&T):** Coordiné directamente con el equipo de Perforación y Tronadura para la asignación y uso de maquinaria, gestionando la disponibilidad de equipos como cliente interno para la ejecución de la campaña de geología.
* **Jerarquización de Datos y Reglas de Ponderación:** Implementé reglas de ponderación en el Kriging para dar prioridad a los predictores más precisos. Se otorgó mayor peso a los sondajes diamantinos (DDH) sobre las perforaciones de aire reverso y blastholes, reconociendo su superioridad técnica en la recuperación de muestra.
* **Ponderación por Calidad de Datos (Kriging de Varianzas):** Implementé reglas de priorización integradas directamente en los ponderadores del Kriging. Utilicé la **varianza del error** de cada tipo de perforación para ponderar el conjunto de datos, asegurando que el predictor diera prioridad natural a los sondajes diamantinos sobre el aire reverso y los pozos de tronadura debido a su mayor precisión analítica y de muestreo.
* **Definición de Zonas de Confianza:** Apliqué zonas de confianza específicas en los sectores del mediano plazo, permitiendo una interpretación clara de la incertidumbre para el equipo de planificación.
* **Modelamiento Multibanco y Textural:** Realicé la compositación y el análisis variográfico para proyectar leyes ($FeT$ y $FeM$) y texturas (**Brecha, Masivo y Diseminado**) a través de los 3 bancos de diseño.

## 📈 Resultado (R)
* **Optimización del Modelo Predictor:** El uso de reglas de ponderación permitió un modelo de mediano plazo con menor sesgo, utilizando la diamantina como el estándar de oro para calibrar los datos de menor precisión.
* **Eficiencia Operativa en Perforación:** La coordinación exitosa con P&T garantizó la ejecución de las mallas de diseño en los tiempos requeridos por la planificación mensual.
* **Reducción de Incertidumbre Geometalúrgica:** La delimitación de zonas de confianza permitió identificar áreas críticas donde la variabilidad textural del hierro podía impactar el rendimiento de la planta.
* **Confiabilidad en el Plan de Minado:** Se logró una alta correlación entre el modelo proyectado y el corto plazo real, asegurando la continuidad operativa y el cumplimiento de las metas de producción.

---