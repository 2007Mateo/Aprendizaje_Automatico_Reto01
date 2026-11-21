# Control de archivos definitivos · Reto 01

Los tres entregables principales se encuentran en el directorio `04_hito4_informe/` de la rama `main`. Los tamaños se cotejaron con la lista de archivos de GitHub.

**Nota de integridad:** las huellas SHA-256 siguientes se calcularon sobre las copias de entrega originales. Para verificar *byte a byte* los archivos descargados de GitHub, comparar su SHA-256 localmente con el valor documentado; la coincidencia de tamaño, por sí sola, no equivale a una validación criptográfica.

| Archivo publicado en GitHub | Tamaño (bytes) | SHA-256 de la copia original | Estado |
|---|---:|---|---|
| [`Reto01_GIRS_2024_Colab_Final_AUDITADO.ipynb`](Reto01_GIRS_2024_Colab_Final_AUDITADO.ipynb) | 43923 | `9e44a212f3aa992d18cbc67fc9498091ed906e59e50f76d046ded6915f2a95ca` | Publicado |
| [`Informe_FINAL_Reto01.pdf`](Informe_FINAL_Reto01.pdf) | 1299611 | `8a9c670cda34aa25515b7d8d5d00031ac19ecb507e166e795a1fcb4418312f95` | Publicado |
| [`Reto01_GIRS_2024_Resultados_Colab.zip`](Reto01_GIRS_2024_Resultados_Colab.zip) | 518687 | `13e0b0c4dc52784d368a79b00d91220f5e04ba57e6aa5a15f7049b18efd891dd` | Publicado |
| `Reto01_ENTREGA_FINAL_AULA_VIRTUAL.zip` | 1220191 | `60c4fd89e2375650f538cf19d0e041e71f49f356d9879c2585bc412b47bb7f6d` | Paquete opcional **no publicado** |

## Verificar copias descargadas

```bash
python -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" Reto01_GIRS_2024_Resultados_Colab.zip
```

Los dos productos obligatorios para el Aula Virtual son el **PDF definitivo** y el **notebook .ipynb**. El ZIP de 19 resultados constituye evidencia complementaria.
