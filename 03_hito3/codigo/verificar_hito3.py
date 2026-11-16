"""Comprobación independiente de resultados Hito3. Ejecutar desde raíz del repositorio.
python 03_hito3/codigo/verificar_hito3.py
"""
import csv,json,sys
from pathlib import Path
from collections import Counter
from math import isclose
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'03_hito3/resultados'
FIG=ROOT/'03_hito3/figuras'

def read(name):
 with (OUT/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

comp=read('comparacion_kmeans_ward_204_215.csv')
assert len(comp)==20, 'Se esperan 2 escenarios x 2 métodos x 5 k'
assert {(r['escenario'],r['algoritmo'],int(r['k'])) for r in comp}=={(s,a,k) for s in ('215','204') for a in ('K-Means','Ward') for k in range(2,7)}
seeds=read('semillas_kmeans.csv'); assert len(seeds)==50
assert {int(x['semilla']) for x in seeds}=={11,23,37,52,97}
prof=read('perfiles_kmeans_k5_215.csv'); assert len(prof)==5 and sum(int(x['municipios']) for x in prof)==215
assert sorted(int(x['municipios']) for x in prof)==[18,19,29,42,107]
assert sum(int(x['n_CSB_superior_100']) for x in prof)==4
assert sum(int(x['ceros_RI_ambiguos']) for x in prof)==11
ass=read('asignaciones_municipales_kmeans_ward_k5.csv');assert len(ass)==215
assert len({r['CantonId'] for r in ass})==215
assert Counter(int(x['grupo_kmeans']) for x in ass)==Counter({0:107,1:42,2:29,3:19,4:18})
assert all(-1<=float(r['silueta_individual'])<=1 for r in ass)
assert len(read('pca_varianza_pesos_contribuciones.csv'))==25
variance=json.loads((OUT/'diagnostico_escala_y_modelo.json').read_text())
assert isclose(variance['silueta_kmeans_k5'],.5935067764523089,rel_tol=2e-3)
assert isclose(variance['ari_kmeans_ward_k5'],.8790700988429987,rel_tol=2e-3)
assert isclose(sum(variance['pca_varianza_pct']),100,abs_tol=.001)
assert all((FIG/f'{i:02d}_{name}.png').exists() for i,name in enumerate([
'comparacion_silueta','tamanos_k5','pca_kmeans_k5','pca_ward_k5','pca_contribuciones',
'perfiles_porcentajes','silueta_individual','sensibilidad_204_vs_215','distribuciones_matriz'],1))
cross=read('sensibilidad_204_vs_215.csv');assert len(cross)==10
record=next(z for z in cross if z['algoritmo']=='K-Means' and z['k']=='5')
assert record['n_comunes']=='204' and record['cambios_optimos_municipios']=='25'
assert isclose(float(record['ARI_215_contra_204']),0.841207,abs_tol=.000002)
print('Hito 3: OK | 20 modelos comparados | 50 inicializaciones | 5 perfiles | PCA 5 componentes | 9 figuras | 11 ceros trazados')
