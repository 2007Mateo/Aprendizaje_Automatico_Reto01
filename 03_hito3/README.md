# Hito 3 · Reto 01: agrupamiento no supervisado de residuos municipales (INEC GIRS 2024)

**Estado:** entregable técnico de Hito 3 ejecutado y comprobado; **NO es el informe divulgativo final del Hito 4**.

## Reproducir desde Google Colab

1. En Drive, abrir `Hito3_Clustering_PCA_Perfiles_GIRS_2024.ipynb`.
2. Ejecutar las celdas en orden. La primera clona `https://github.com/2007Mateo/Aprendizaje_Automatico_Reto01`.
3. La celda central ejecuta `03_hito3/codigo/ejecutar_hito3.py`, regenerando tablas CSV, figuras y validaciones. El notebook ofrece una descarga ZIP opcional.
4. Validación extra desde el repo: `python 03_hito3/codigo/verificar_hito3.py`.

Dependencias: Python 3.10+, NumPy, SciPy, scikit-learn, matplotlib, IPython/Jupyter. Las pruebas de creación se hicieron en Python 3.13, scikit-learn 1.8.0.

## Actividades guía 5–8 y productos

| Actividad | Producto verificable |
|---|---|
| 5. Comparar agrupamientos | `resultados/comparacion_kmeans_ward_204_215.csv`, KMeans y Ward para k=2..6 |
| 6. Evaluar / estabilidad | `semillas_kmeans.csv`, `sensibilidad_204_vs_215.csv`, `sensibilidad_escalado_absolutos_volumen.csv` |
| 7. PCA | `pca_varianza_pesos_contribuciones.csv`, `pca_coordenadas_215.csv`, figuras 03–05 |
| 8. Comunicar / interpretar | `perfiles_kmeans_k5_215.csv`, `asignaciones_municipales_kmeans_ward_k5.csv`, representantes, nota técnica y figuras |

## Selección razonada (provisional)

- **215 municipios** y cinco características, K-Means `k=5`, semilla `11`, `n_init=30`; se contrastó con Ward euclidiano y k=2..6.
- **Silueta en espacio 5D:** 0,593507 (KMeans), 0,578667 (Ward), ARI entre los dos 0,879070.
- PCA PC1 46,6633%, PC2 18,0605%, suma 64,7238%. PCA es una figura, NO sirve para recalcular siluetas.
- k=6 obtiene 0,617649 de silueta K-Means, pero crea subgrupo de 10 municipios de alta recuperación relativa. k=4 tiene mayor compacidad y estabilidad de escenario. k=5 se eligió como equilibrio interpretativo, no por maximizar métrica.
- Estabilidad cinco semillas K-Means k5 ARI medio 0,994993; sensibilidad 215/204 ARI 0,841207 sobre los mismos 204 municipios. Los 11 ceros ambiguos se conservan como reportados en 215 y se excluyen solo en 204.
- Escalado, recuperación absoluta o añadir volumen `CRR` cambia el agrupamiento: los resultados se deben interpretar con cautela.

## Advertencias académicas

- Se aplica exclusivamente edición **2024**. `fuente_relevante_221.csv` contiene **41 columnas** del extracto del equipo, no las **213** columnas del CSV original del INEC.
- `CantonId` se preserva textualmente **tal como aparece en los Excel suministrados**; pudieron perderse ceros iniciales antes de recibirlos. No inferir ni reconstruir IDs sin cotejar la edición original.
- Las variables binarias representan **actividad declarada**, no toneladas recuperadas; no elaborar rankings, afirmar causalidad ni asignar recursos.
- No deduplicar municipios con vectores idénticos ni recortar coberturas superiores a uno.
- El Hito 4 (otra integrante) debe elaborar su propio informe divulgativo final y notebook integral; [nota de entrega](documentacion/NOTA_PARA_HITO4.md) y [bibliografía](documentacion/referencias.bib) son insumos para esa fase.

## Referencias técnicas y de datos

- [INEC/ANDA · Diccionario y edición GIRS 2024](https://anda.inec.gob.ec/anda5/index.php/catalog/1294/data-dictionary)
- [INEC/ANDA · Formulario y materiales relacionados 2024](https://anda.inec.gob.ec/anda5/index.php/catalog/1294/related-materials)
- [scikit-learn · silhouette_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html)
- [scikit-learn · adjusted_rand_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html)
- [scikit-learn · PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)
