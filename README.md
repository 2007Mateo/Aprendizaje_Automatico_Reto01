# Reto 01 · Aprendizaje automático inicial · GIRS 2024

**PUCE — Ciencia de Datos · Reto 01 (Andrés Merino, período 2026-2)**

Objetivo: explorar perfiles de gestión de residuos de los municipios de Ecuador a partir de **la edición 2024 de la base GIRS del INEC**. Los grupos no son rankings, clasificaciones oficiales ni resultados causales.

## Estado real del proyecto

| Hito (Reto01.pdf, página 4) | Actividades guía | Estado |
|---|---|---|
| **Hito 1.** Auditoría y propuesta de características | **1-2** | Documentado y auditado con salidas de Colab. |
| **Hito 2.** Matriz preparada y propuesta de K-Means, jerárquico y PCA | **3-4 + plan 5-7** | **Entregado**: escenarios de 215 y 204 municipios; plan detallado. |
| **Hito 3.** Resultados, perfiles, gráficas y estabilidad | **5-8** | Pendiente de ejecutar/evaluar; código de experimentos preparado. |
| **Hito 4.** Notebook e informe divulgativo finales | **Integración 1-8** | Pendiente. |

### Organización
- `00_enunciado`: rúbrica y formato PUCE; PDF institucional original.
- `01_hito1`: informe, notebook y salidas de auditoría.
- `02_hito2/datos`: fuente parcial relevante de 41 columnas, base preparada de 221 y 17 incidencias trazables.
- `02_hito2/matrices`: matrices **sin identificadores** de 215 y 204 y sus archivos de claves separados.
- `02_hito2/notebooks`: validación reproducible y presentación de las matrices para el Hito 2.
- `02_hito2/codigo`: verificaciones automáticas.
- `03_hito3_preparacion`: script de experimentos para el siguiente hito, **no es un resultado final**.
- `docs`: plan metodológico y seguimiento de hitos y actividades.

### Decisión metodológica
La **matriz 215** es principal **provisionalmente**; los 11 ceros de RI ambiguos siguen documentados y no se sustituyen por cantidades inventadas. La **204** es sensibilidad conservadora. Excluir 17 filas no significa borrar municipios del registro auditado de 221.

Las matrices **no incluyen CantonId, Provin, ni NombreCantón**. La característica `RI_log_p95` fue construida con referencia fija del percentil 95 de los 204 casos para que ambos escenarios sean directamente comparables. El resto conserva sus unidades/proporciones y banderas de atipicidad; no se recorta `CSB>1`.

### Para ejecutar
1. Colab: abrir `02_hito2/notebooks/Hito2_Preparacion_y_Plan.ipynb`, cargar o clonar el repositorio y seguir sus celdas.
2. Validar: `python 02_hito2/codigo/verificar_hito2.py` desde la raíz del repositorio.
3. Hito 3: ejecutar `python 03_hito3_preparacion/experimentos_hito3.py` desde la raíz (requiere NumPy, scikit-learn y matplotlib), revisar los resultados y **no** escoger grupos solo por silueta.

**Advertencia de reproducibilidad:** la edición CSV de 213 columnas no acompaña este paquete. `fuente_relevante_221.csv` preserva las 41 columnas tomadas de los libros del equipo, no sustituye al CSV original. La documentación del INEC debe permitir localizar la edición oficial y reproducir la auditoría completa.
