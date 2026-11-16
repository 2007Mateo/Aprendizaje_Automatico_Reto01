# Hito 2 — Matriz preparada y propuesta de comparación (GIRS 2024)

**Alcance exacto:** en `Reto01.pdf` el Hito 2 es una **matriz preparada** con una **propuesta de comparación de K-Means y agrupamiento jerárquico y PCA**. Las tablas finales de métricas y perfiles se evaluarán en el Hito 3.

## 1. Origen y trazabilidad
Se conserva una tabla de 221 registros (identificados por `CantonId`, como texto) y 41 campos relevantes extraídos de los Excel del equipo, con una ficha de 22 columnas que registra los cinco indicadores y decisiones por municipio. El INEC publica la edición 2024 con 221 observaciones y 213 columnas; esta exportación parcial **no** debe confundirse con el CSV íntegro original.

## 2. Las cinco columnas numéricas (sin identificadores)

| Columna de la matriz | Código(s) fuente | Interpretación | Preparación |
|---|---|---|---|
| `CSB_cobertura` | `CSB`, contraste `VB/MR4223` | Cobertura de barrido, proporción | Se preservan 4 valores >1, sin truncamiento ni corrección arbitraria; 5 casos sin denominador no entran en completos. |
| `DIF_proporcion` | `DIF`, `MR453` | Parte de residuos diferenciados sobre recolectados, toneladas/día | Razón de unidades compatibles y denominador positivo; Piñas >1 se marca inválida. |
| `ORG_actividad` | `MR441`, `MR442` | Actividad orgánica reportada, indicador 0/1 | 1 si alguna actividad sí; 0 si ambas no. Los códigos 1/2 no se usan como escala continua. |
| `RI_log_p95` | `RI` (kg/mes), `CRR` (ton/mes) | Intensidad relativa de recuperación inorgánica transformada | Primero RI/(1000*CRR) y después log1p(100*x)/log1p(100*q95), con q95 FIJO calculado de los 204; 11 ceros contradictorios revisados mediante sensibilidad. |
| `BOTADERO_indicador` | `MR461` | Utilización de botadero principal, 0/1 | 1 si código 3; 0 si códigos 1-2; guardar categoría fuente para interpretación. |

Las variables de contexto (`CRR_ton_mes_contexto`, provincia, nombre, población urbana de referencia) solo describen los grupos; no entran en las distancias. No se incorporan `TROT` (unidades cuestionadas), `PORG` (cobertura limitada), `Pob` como población cantonal 2024, ni `RI` junto a `RIR`.

## 3. Casos y escenarios

| Nivel | Filas | Razón |
|---|---:|---|
| Auditoría / información sin pérdidas | 221 | Todos los municipios originales presentes. |
| Principal provisional | 215 | Fuera cinco `CSB` sin denominador válido y Piñas con `DIF/MR453 > 1`. Los once ceros dudosos de RI permanecen como cero **reportado** y marcados. |
| Conservador / sensibilidad | 204 | Aparte de los seis anteriores se excluyen once con materiales marcados recuperados y `RI = 0`. |

Los 17 casos **no** son necesariamente valores erróneos. Las decisiones están registradas en `incidencias_17.csv`. Los cuatro `CSB > 1` permanecen en ambas matrices y deben describirse. No se elimina ningún municipio por ser atípico o por mejorar métricas.

## 4. Escala y tratamiento de atípicos
La matriz de trabajo conserva proporciones e indicadores 0/1; `RI` está comprimida por el logaritmo con un q95 de referencia fija, obtenido previamente sobre la muestra conservadora. Este mismo denominador se aplica a los dos escenarios, de modo que no cambie la escala al variar la muestra. Hay valores >1 en `CSB` y en `RI_log_p95`; **no se recortan**.

**Decisión principal:** utilizar esta matriz numérica transformada de cinco columnas **sin z-score adicional**, porque las variables ya tienen interpretación de proporción, binaria o recuperación referida a un cuantil. La distancia euclidiana refleja una diferencia de ~1 en cada dimensión, aunque no implica igual utilidad sustantiva. **Sensibilidad:** `StandardScaler` ajustado SOLO con 215 y aplicado tanto a 215 como a 204, para evaluar el efecto de dar varianza unitaria a indicadores binarios escasos. Se documentarán las distribuciones y el efecto sobre grupos; no escoger escalado porque aumente silueta.

## 5. Plan preciso para algoritmos y PCA (siguiente hito)
1. Sobre la MISMA matriz de cada escenario (cinco variables sin IDs), comparar K-Means y jerárquico aglomerativo Ward + distancia euclidiana.
2. Fijar `k = 2,3,4,5,6` (cinco valores, supera mínimo de tres); para K-Means semillas `11,23,37,52,97` y `n_init=30` por semilla; documentar convergencia y variación.
3. Calcular silueta euclidiana en los cinco atributos originales/preparados usados para agrupar, nunca en la proyección PCA; registrar tamaño mínimo, máximo y todos los tamaños de grupos. Evaluar si hay particiones degeneradas o grupos diminutos.
4. Estabilidad interna: ARI entre inicializaciones para igual k; sensibilidad entre escenarios: concordancia ARI calculada SOLO sobre los mismos 204 `CantonId` y sin requerir igualdad del número de etiqueta.
5. PCA con dos componentes sobre exactamente la misma matriz de entrada del clustering; reportar contribuciones o pesos (cargas), varianza explicada por eje y acumulada. Colorear por grupos solo como visualización.
6. Interpretar diferencias con indicadores en unidades originales (`RI` kg/mes; `CRR` ton/mes; CSB y DIF proporciones) y descripción de municipios, usando claves externas.
7. Comprobar la pregunta de escala de operación: comparar las características del agrupamiento con `log(1+CRR)` **externamente**, y repetir experimento de sensibilidad incluyendo dicha variable de manera separada y explícita.
8. No dar nombres de rendimiento o ranking automático a grupos; proponer apoyos tentativos y aclarar limitaciones.

## 6. Riesgos y límites
- Diferentes municipios comparten exactamente el mismo vector de cinco atributos. Esto NO son registros cantonales duplicados. No deduplicar los vectores para entrenar, porque cada municipio es una observación legítima.
- Los 11 ceros dudosos deben cotejarse contra formulario/diccionario. La hipótesis de cantidad cero reportada y actividad presente se somete a sensibilidad, no a una corrección arbitraria.
- La correlación `DIF_proporcion` vs `ORG_actividad` no justifica descartar una variable automáticamente; revisar con/sin ella en análisis de sensibilidad.
- La transformación `RI_log_p95` usa un cuantil fijado sobre los 204 y sigue válida para el escenario de 215; NO recalcular el cuantil por escenario, pues alteraría la comparación.
- Las matrices son para **exploración no supervisada**, no requieren separación train/test ni clasificación oficial.

## 7. Condición de salida del Hito 2
Matriz 215 y matriz 204, claves separadas, incidencias, verificador, celdas de diagnóstico en Colab, semillas, distancia, k, PCA, límites y plan listos. **No atribuir perfiles ni siluetas definitivos sin ejecutar y discutir el Hito 3.**
