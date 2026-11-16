# Entrega y coordinación del Reto 01 (GIRS 2024)

**Lectura indispensable para el equipo.** En el enunciado de Andrés Merino, las **actividades guía 1–8** son tareas técnicas y los **Hitos 1–4** son productos de seguimiento. No son la misma numeración: las actividades **3 y 4** tratan preparación y redundancia; **NO** equivalen a los Hitos 3 y 4.

## Estado y responsables

| Hito | Producto exigido por Reto01 | Actividades involucradas | Responsable y estado |
|---|---|---|---|
| 1 | Auditoría inicial, 4–8 características, plan justificado | 1 auditar, 2 seleccionar | Avances hechos y auditados mediante Colab |
| 2 | Matriz preparada y propuesta K-Means / jerárquico / PCA | 3 preparar, 4 evitar redundancia; plan de 5–7 | Responsable: equipo coordinado por el estudiante; preparado y revisable |
| 3 | Borrador con tabla comparativa, perfiles, visualizaciones y estabilidad | Ejecutar 5 (agrupamiento), 6 (evaluación), 7 (PCA), 8 (comunicación) | Estudiante, **ejecutado y publicado**: resultados y borrador técnico disponible |
| 4 | Entrega final de notebook reproducible y **informe divulgativo** | Integración y resultados de 1–8 | Compañera responsable del documento final; ya dispone de Hito 3, pendiente del producto divulgativo y notebook integral |

### Revisión prioritaria para el compañero: Hito 2

Leer **en este orden**:

1. [Informe y plan Hito 2](HITO2_INFORME_Y_PLAN.md): interpretación, decisiones de datos, comparación y PCA.
2. [Excel preparación (221)](../02_hito2/Libros_preparacion_221.xlsx): columnas fuentes, indicadores calculados, incidencias y filtros.
3. [Excel de matrices](../02_hito2/Libros_matrices.xlsx): datos y claves; comparar 215 y 204.
4. [Base preparada de 221](../02_hito2/datos/base_preparada_221.csv), [17 incidencias](../02_hito2/datos/incidencias_17.csv), [matriz 215](../02_hito2/matrices/matriz_215.csv), [matriz 204](../02_hito2/matrices/matriz_204.csv).
5. [Claves 215](../02_hito2/matrices/claves_215.csv) y [claves 204](../02_hito2/matrices/claves_204.csv): los IDs y nombres son externos a distancias.
6. [Notebook Hito 2](../02_hito2/notebooks/Hito2_Preparacion_y_Plan.ipynb), [verificador](../02_hito2/codigo/verificar_hito2.py), [verificador de origen](../02_hito2/codigo/verificar_origen.py).

### Contexto previo

- [Mapa hitos y actividades](MAPA_HITOS_Y_ACTIVIDADES.md).
- [PDF informe Hito 1](../01_hito1/Informe_Hito1.pdf).
- [Auditoría Hito 1 en Colab](../01_hito1/Auditoria_Colab_Hito1.ipynb) y [ejecución PDF](../01_hito1/Auditoria_Colab_resultados.pdf).
- El texto del profesor `Reto01.pdf` y el formato de LaTeX `formatoInforme.pdf` se proporcionan aparte por el equipo; **no están publicados en este repositorio público**.

### Decisiones que NO cambiar sin justificar

- Universo GIRS **edición 2024**, 221 municipios originales y 213 columnas en CSV oficial.
- Cinco atributos: cobertura de barrido, recolección diferenciada, actividad orgánica, recuperación inorgánica relativa transformada y botadero principal.
- **215 municipios** matriz principal provisional, **204** para sensibilidad; diferencia: 11 ceros ambiguos de recuperación. Cinco CSB no calculables y un DIF/MR453 mayor que 1 se excluyen de casos completos; los cuatro CSB mayores que 1 **permanecen**.
- Un cero, una ausencia y un salto de formulario son situaciones distintas. No recortar a 1, ni eliminar municipios simplemente por mejorar silueta.
- Conservar separados indicadores de distancia y claves de identificación municipal.
- Matrices no equivalen a clusters: **no se han ejecutado ni interpretado los resultados del Hito 3**.

### Qué recibirá el compañero del Hito 3 para cerrar Hito 4

El Hito 3 ya está publicado en [`03_hito3/`](../03_hito3/README.md). La responsable de Hito 4 dispone de: configuraciones y semillas, tablas comparativas de K-Means y jerárquico para al menos tres k entre 2–6, silueta calculada en matriz de clustering, tamaños, estabilidad entre semillas y escenarios, PCA con varianza explicada y cargas, gráficos, perfiles en unidades originales, ejemplos, limitaciones y propuestas. Con ello integrará el notebook de Colab reproducible y el informe dirigido a técnicos municipales en el formato PUCE LaTeX (bibliografía .bib, APA 7), de acuerdo con el enunciado.

### Enlaces Colab (Drive privado del estudiante)

Los notebooks están en `5TO SEMESTRE/Aprendizaje Automático/`. Para abrir, Google Drive → abrir con Google Colaboratory, o Colab → Archivo → Abrir notebook → Google Drive.

- [Hito 1](https://drive.google.com/file/d/1_9C9QPpqAVklIN_uV6M9zofHmWCXwZ9w/view?usp=drivesdk)
- [Hito 2](https://drive.google.com/file/d/14eywPATCZrego3B1PyC0TRx-vDf6yLPV/view?usp=drivesdk)
- [Limpieza preliminar de referencia](https://drive.google.com/file/d/1TmtnAnOxi-CfhjOcFdOm8bZ0AJbrQ-tP/view?usp=drivesdk)

Los enlaces de Drive no necesariamente sirven al compañero si no se ha otorgado acceso; **para revisión basta el repositorio**. El archivo de limpieza preliminar es de referencia y no debe sustituir sin cotejo las matrices ya auditadas del equipo.

## Control de calidad antes de entrega final

Verificar que el notebook final pueda ejecutarse en un runtime de Colab desde cero, que las figuras coincidan con las tablas y que no se presente un ranking, efecto causal o clasificación oficial. Los resultados deben explicarse en el contexto de prácticas municipales y reconocer incertidumbre y disponibilidad.

### Actualización 15 de noviembre de 2026: material de Hito 3

La carpeta [`03_hito3/`](../03_hito3/README.md) tiene el [borrador técnico PDF](../03_hito3/documentacion/Informe_Tecnico_Hito3.pdf), [notebook reproducible](../03_hito3/notebooks/Hito3_Clustering_PCA_Perfiles_GIRS_2024.ipynb), [resultados CSV](../03_hito3/resultados/) y [figuras](../03_hito3/figuras/). Además existe una [nota de traspaso](../03_hito3/documentacion/NOTA_PARA_HITO4.md) y [bibliografía .bib](../03_hito3/documentacion/referencias.bib) para la compañera del Hito 4. Mantener separadas las actividades guía 5–8 del **Hito 4 final**. No usar los nombres de clusters como ranking.
