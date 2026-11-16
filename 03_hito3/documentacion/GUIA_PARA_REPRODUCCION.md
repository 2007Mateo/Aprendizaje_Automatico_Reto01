# Guía breve de ejecución y verificación

**Notebook a ejecutar**: `notebooks/Hito3_Clustering_PCA_Perfiles_GIRS_2024.ipynb`, publicado en Drive `5TO SEMESTRE/Aprendizaje Automático/` y en GitHub `03_hito3/notebooks/`.

- Para Colab: abrir notebook, ejecutar *Entorno de ejecución > Ejecutar todas*. Necesita GitHub público con los datos Hito 2 ya publicados. El notebook invoca el script por `subprocess` y genera sus 9 figuras y CSV.
- Para computadora: `git clone https://github.com/2007Mateo/Aprendizaje_Automatico_Reto01.git && cd Aprendizaje_Automatico_Reto01 && pip install -r 03_hito3/documentacion/requirements.txt && python 03_hito3/codigo/ejecutar_hito3.py && python 03_hito3/codigo/verificar_hito3.py`.
- Los archivos de resultados se sobrescriben **de manera determinista** con cada corrida. Si el algoritmo o la versión de scikit-learn difieren, contrastar los resultados con la tabla de comparación publicada y registrar la versión.
- Si en GitHub se modifican las matrices del Hito 2, los resultados publicados dejan de reflejar esa versión; volver a ejecutar y revisar Hitos 2 y 3.
- Para entregar a compañera de Hito 4: `NOTA_PARA_HITO4.md`, `.bib`, PDF provisional, notebook y figuras.

**No entregar el informe técnico como divulgativo final.** El informe final debe usar formato de tareas PUCE en LaTeX y bibliografía APA 7.
