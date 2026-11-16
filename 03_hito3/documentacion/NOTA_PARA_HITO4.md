# Entrega técnica del Hito 3 a responsable de Hito 4

## Estado y límites del encargo

El Hito 3 es un **borrador** de resultados conforme a `Reto01.pdf`, p. 4: tabla comparativa, perfiles, gráficos y estabilidad. No sustituye el notebook integral y el informe divulgativo **finales** de Hito 4. Se consolidan aquí resultados sobre 215 municipios (principal) y 204 (sensibilidad), derivados de los Excel del equipo; 221 registros en el auditorio. El archivo GIRS original completo (213 columnas) no fue adjuntado, por lo que las trazas de origen completo aún deben mantenerse a disposición.

## Métodos y cifras verificadas

- Variables: `CSB_cobertura`, `DIF_proporcion`, `ORG_actividad`, `RI_log_p95`, `BOTADERO_indicador` (sin IDs en distancias), edición INEC **2024**.
- K-Means, 5 semillas `(11,23,37,52,97)`, `n_init=30`; Ward distancia euclidiana, `k=2..6`; métricas en las cinco dimensiones.
- **Propuesta descriptiva provisional:** K-Means k=5, semilla 11, silueta **0,593507**. Ward k=5, silueta **0,578667**; acuerdo ARI **0,879070**. K-Means ARI entre semillas media **0,994993**, mínima **0,987483**.
- K-Means k=6 silueta **0,617649** y grupo mínimo 10, mientras k=4 da **0,558368** y grupo mínimo 19. Elegir 5 por diversidad interpretativa sin hacer de la silueta el único criterio; mantener 4 y 6 como contrastes.
- Escenario 215 frente a 204 para K-Means k=5: ARI **0,841207** sobre los **204 municipios compartidos**, 25 asignaciones distintas tras permutar etiquetas; Ward k=5 ARI **1,000**; para K-Means k=4 y 6 ARI **1,000**.
- Z-score alteró partición K-Means k=5 respecto a base (ARI **0,828187**); usar RI absoluto en vez de relativo (ARI **0,684649**); añadir log(1+CRR) estandarizado (ARI **0,340370**). El tamaño de operación condicionaría bastante la agrupación si se incorpora como distancia.
- PCA aplicado a las cinco características: PC1 explica **46,6633 %**, PC2 **18,0605 %**, acumulada **64,7238 %**. PC1 dominado por orgánicos (48,16 % contribución) y diferenciada (41,47 %); PC2 por botadero (94,60 %).

## Perfiles de la opción principal (descriptivos, no ranking)

| Grupo | Municipios | Perfil propuesto | Barrido media | Diferenciada media | Orgánicos (% sí) | Botadero (% sí) | RI mediana kg/mes | CRR mediana t/mes |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| G0 | 107 | Sin diferenciación ni actividad orgánica declarada | 88,54 % | 0,44 % | 0 % | 0 % | 0 | 390 |
| G1 | 42 | Diferenciada y actividad orgánica declaradas | 77,98 % | 96,75 % | 100 % | 7,14 % | 1.020,84 | 186,15 |
| G2 | 29 | Botadero predominante, poca diferenciación | 81,41 % | 0,49 % | 6,9 % | 100 % | 0 | 600 |
| G3 | 19 | Diferenciada sin actividad orgánica declarada | 78,63 % | 99,90 % | 0 % | 10,53 % | 0 | 318,9 |
| G4 | 18 | Actividad orgánica declarada, poca diferenciación | 82,83 % | 5,40 % | 100 % | 0 % | 1.029,38 | 810 |

Ejemplos centrales por proximidad al centroide (no representan calidad de gestión): G0 JAMA; G1 PASTAZA; G2 CHONE; G3 QUITO; G4 CUENCA. Las cifras se reportan en unidades originales y las transformaciones internas del modelo permanecen por separado.

## Qué comunicar sin tergiversar

- Las marcas binarias "sí orgánicos" registran **actividad declarada**, no toneladas efectivamente tratadas.
- Los identificadores fueron recibidos de Excel; algunos `CantonId` pueden haber perdido ceros iniciales. **No reconstruir** sin cotejar con CSV oficial.
- Se mantuvieron cuatro valores `CSB>1`. Hay cinco coberturas no calculables, una proporción DIF>1 y 11 ceros RI ambiguos, con dos escenarios. No identificar ni clasificar los seis sin matriz completa con grupos inventados.
- El reporte no es causal, no es una clasificación ni ranking oficial, no asigna recursos automáticamente. La separación del PCA 2D **no sustituye** las métricas en 5D.
- Cantidad recolectada `CRR` se usó como descriptor externo. Medianas por grupo difieren, por lo que no se afirma independencia absoluta del tamaño.
- El caso k=6 (10 municipios de recuperación relativa alta) puede ser una subestructura real o una separación conducida por atípicos. No descartarlo sin argumentar.

## Material para integrar en el Hito 4

- Script completo `03_hito3/codigo/ejecutar_hito3.py` y notebook `03_hito3/notebooks/Hito3_Clustering_PCA_Perfiles_GIRS_2024.ipynb`, ejecutable en Google Colab desde repositorio público.
- `03_hito3/resultados/comparacion_kmeans_ward_204_215.csv`, `perfiles_kmeans_k5_215.csv`, `semillas_kmeans.csv`, `sensibilidad_204_vs_215.csv`, `sensibilidad_escalado_absolutos_volumen.csv`, `pca_varianza_pesos_contribuciones.csv`, `asignaciones_municipales_kmeans_ward_k5.csv`, `municipios_representativos_k5.csv`, etc.
- Nueve figuras `.png` de `03_hito3/figuras/`; incluir en el informe final solo las más explicativas.
- Bibliografía en `03_hito3/documentacion/referencias.bib`; comprobar formato APA7 y fechas antes de enviar.
- Informe **técnico provisional** `.tex` / `.pdf` es traspaso de Hito 3, no la entrega divulgativa final.

## Propuestas tentativas de exploración por perfil

- G0: solicitar evidencia de separación en fuente, capacidad de reciclaje y cobertura de rutas; explorar pilotos de separación sin inferir que todo municipio carece de gestión.
- G1: examinar trazabilidad de recuperación efectiva y continuidad de las prácticas orgánicas y diferenciadas.
- G2: documentar condiciones del sitio, planes técnicos y alternativas de disposición que podrían requerir evaluación.
- G3: investigar por qué la separación reportada no coincide con actividad orgánica declarada; verificar flujo de materiales.
- G4: estudiar relación entre actividad orgánica y sistemas de recolección diferenciada, para verificar integración operativa.

**El Hito 4 debe preparar su propio texto dirigido a técnicos municipales** y conservar explícitamente las limitaciones y las incertidumbres anteriores.
