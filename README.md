# Reto 01 · Aprendizaje automático inicial · GIRS 2024

Trabajo académico de Ciencia de Datos (PUCE): **Ecuador y sus residuos: descubrir perfiles de gestión municipal**. Fuente: edición INEC GIRS 2024. Los grupos son exploratorios: no representan clasificaciones oficiales, rankings ni efectos causales.

## Seguimiento por HITOS y ACTIVIDADES GUÍA (Reto01.pdf)

| Hito | Actividades | Estado |
|---|---|---|
| **Hito 1.** Auditoría y propuesta de variables | 1-2 | Completo en lo esencial; datos contrastados con Colab |
| **Hito 2.** Matriz preparada y plan K-Means/Ward/PCA | 3-4 y plan 5-7 | **Preparado y verificado** |
| **Hito 3.** Comparación, métricas, perfiles, PCA y estabilidad | 5-8 | Pendiente |
| **Hito 4.** Notebook reproducible e informe divulgativo | Integración de 1-8 | Pendiente |

## Matriz Hito 2
Cinco columnas numéricas: `CSB_cobertura`, `DIF_proporcion`, `ORG_actividad`, `RI_log_p95`, `BOTADERO_indicador`. Los códigos, nombres y provincias van **fuera** de las distancias.

- **221** municipios auditados; **17** incidencias trazadas: 5 CSB sin denominador, 1 proporción DIF inválida (Piñas), 11 ceros ambiguos de RI.
- **215** municipios = matriz principal provisional, conserva 11 ceros ambiguos como informados, con bandera.
- **204** municipios = análisis conservador de sensibilidad, excluye esos once registros adicionales.
- Los cuatro CSB superiores a uno **no** fueron recortados ni se eliminan municipios para maximizar silueta.
- RI se expresa con cociente de unidades compatibles y logaritmo normalizado por el mismo q95 (referencia 204) en ambos escenarios.
- No se incluyen RI y RIR a la vez, ni totales con todos sus componentes.

## Plan aprobado en Hito 2
Comparar K-Means (semillas 11, 23, 37, 52, 97; `n_init=30`) y aglomerativo Ward-euclidiano para `k=2,3,4,5,6` sobre la **misma matriz de cinco dimensiones**. Evaluar silueta en cinco dimensiones (nunca en PCA 2D), tamaños, estabilidad por ARI y comparación 204/215; PCA de dos componentes exclusivamente para interpretar y visualizar con varianza explicada. Como sensibilidad adicional estudiar estandarización Z-score e influencia de volumen `CRR`.

## Fuente y advertencia
El archivo **completo** del INEC tiene 221×213; el extracto del equipo contiene 41 columnas de interés y NO lo sustituye. Para trazabilidad reproducir a partir de la edición oficial 2024 `BDD_GIRS_2024_VF.csv` (separador punto y coma, decimal coma, Windows-1252, `CantonId` texto).

La entrega local completa (documentos, libros del equipo y CSV) está disponible en el paquete creado en la conversación. Este repositorio se publica en fases para conservar evidencia y no afirmar resultados de agrupamiento antes del Hito 3.
