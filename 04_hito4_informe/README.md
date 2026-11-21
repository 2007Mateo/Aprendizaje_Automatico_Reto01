# Hito 4 · Entrega final del Reto 01 — GIRS 2024

**PUCE · Ingeniería en Ciencia de Datos · Isabel Paguay, Mateo Vera y Martín Andrade**

Este directorio reúne la **entrega definitiva** del proyecto: un informe divulgativo en formato PUCE, un notebook reproducible de Google Colab y las evidencias de su ejecución.

## Entregables definitivos publicados

| Archivo | Contenido |
|---|---|
| [`Informe_FINAL_Reto01.pdf`](Informe_FINAL_Reto01.pdf) | **Informe definitivo**; formato PUCE y bibliografía revisada en APA 7 |
| [`Reto01_GIRS_2024_Colab_Final_AUDITADO.ipynb`](Reto01_GIRS_2024_Colab_Final_AUDITADO.ipynb) | **Notebook final**, 27 celdas; usa CSV preparado del Hito 2 y realiza comprobaciones |
| [`Reto01_GIRS_2024_Resultados_Colab.zip`](Reto01_GIRS_2024_Resultados_Colab.zip) | **Evidencias complementarias**: 8 PNG, 10 CSV y 1 JSON |
| [`CONTROL_ARCHIVOS_FINALES.md`](CONTROL_ARCHIVOS_FINALES.md) | Tamaños y huellas de referencia de los archivos destinados a entrega |

### Versiones anteriores conservadas

- [`InformeReto01_PUCE_Revisado.pdf`](InformeReto01_PUCE_Revisado.pdf): revisión editorial **anterior**, no la entrega definitiva.
- [`InformeReto01_PUCE_Proyecto_LaTeX.zip`](InformeReto01_PUCE_Proyecto_LaTeX.zip): fuentes de la revisión anterior.

## Resumen del análisis

Se estudiaron **221** municipios en la auditoría y se construyeron dos escenarios de agrupamiento: **215 municipios (principal)** y **204 (sensibilidad conservadora)**. Se compararon **K-Means y Ward** para `k=2..6`, con cinco perfiles interpretables y un PCA utilizado para visualización.

| Indicador | Resultado |
|---|---:|
| Silueta K-Means, k=5 | 0,593507 |
| Silueta Ward, k=5 | 0,578667 |
| ARI entre algoritmos | 0,879070 |
| ARI medio entre semillas | 0,994993 |
| ARI entre escenarios 215/204 | 0,841207 |
| Varianza explicada PCA 2D | 64,7238 % |

Los perfiles identifican similitudes estadísticas entre municipios. **No son un ranking de desempeño** ni establecen causalidad.

## Reproducibilidad y entrega

El notebook utiliza por defecto un **commit fijo** con el CSV preparado del Hito 2 y verifica su integridad mediante SHA-256. Al ejecutarlo, genera sus tablas y gráficos y un ZIP con 19 evidencias. El CSV original íntegro de 213 columnas no se incluye en este repositorio.

Para el Aula Virtual, los **dos productos obligatorios** son el PDF definitivo y el notebook `.ipynb`; el ZIP de resultados es soporte adicional.

[Volver al README principal](../README.md).
