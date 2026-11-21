# Hito 4 · Integración de la entrega final (GIRS 2024)

**PUCE · Aprendizaje Automático Inicial · equipo: Isabel Paguay, Mateo Vera y Martín Andrade.**

Este directorio conserva las versiones editoriales anteriores y agrega el notebook final auditado. El trabajo compara **K-Means y Ward** con `k=2..6`, dos escenarios de **215 y 204** municipios y PCA sobre cinco indicadores. El agrupamiento se evalúa en cinco dimensiones; los perfiles son exploratorios y no representan un ranking municipal.

## Contenido disponible en GitHub

- [Notebook final auditado](Reto01_GIRS_2024_Colab_Final_AUDITADO.ipynb): cuaderno de 27 celdas listo para Google Colab; lee el CSV preparado de la edición 2024 y contrasta las cifras del informe.
- [Informe editorial anterior](InformeReto01_PUCE_Revisado.pdf): documento previo a la corrección bibliográfica de la entrega definitiva; **no** confundir con el PDF final.
- [Proyecto LaTeX de la revisión anterior](InformeReto01_PUCE_Proyecto_LaTeX.zip): antecedentes de edición.

## Archivos definitivos que faltan por subir a GitHub

Los siguientes archivos **no están publicados aquí** todavía y no deben presentarse como existentes en el repositorio:

1. `Informe_Reto01_PUCE_ENTREGA_DEFINITIVA.pdf` — PDF final en formato PUCE con ajustes APA 7.
2. `Reto01_GIRS_2024_Resultados_Colab.zip` — archivo ZIP generado por la ejecución real en Colab: 8 imágenes PNG, 10 tablas CSV y 1 JSON.
3. Opcionalmente, `Reto01_ENTREGA_FINAL_AULA_VIRTUAL.zip` — paquete con los dos productos obligatorios.

Las huellas SHA-256 y los tamaños se registran en [CONTROL_ARCHIVOS_FINALES.md](CONTROL_ARCHIVOS_FINALES.md) para cotejar las cargas pendientes. Una vez añadidos, conviene actualizar también el README de la raíz.

## Cifras de referencia comprobadas

| Control | Valor |
| --- | ---: |
| K-Means, silueta k=5 | 0.593507 |
| Ward, silueta k=5 | 0.578667 |
| ARI K-Means frente a Ward | 0.879070 |
| ARI medio entre semillas | 0.994993 |
| Sensibilidad de muestras 215/204 (ARI) | 0.841207 |
| PCA, variación explicada PC1 + PC2 | 64.7238 % |

Se conservan las decisiones documentadas en los Hitos 1–3; no se sustituyen el informe o las métricas por valores inventados.
