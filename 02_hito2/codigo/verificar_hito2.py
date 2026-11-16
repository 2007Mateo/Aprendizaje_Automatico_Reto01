"""Verificación determinista del Hito 2, sin instalar dependencias externas."""
from pathlib import Path
import csv, math, collections, hashlib
R=Path(__file__).resolve().parents[2]
def rows(p):
 with (R/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
base=rows('02_hito2/datos/base_preparada_221.csv')
inc=rows('02_hito2/datos/incidencias_17.csv')
assert len(base)==221 and len(inc)==17
assert len(set(x['CantonId'] for x in base))==221
assert collections.Counter(x['Motivo_exclusion'] for x in inc)=={
 'CSB sin denominador válido':5,
 'Proporción diferenciada fuera de 0-1':1,
 'RI cero con material recuperado marcado':11}
fields=['CSB_cobertura','DIF_proporcion','ORG_actividad','RI_log_p95','BOTADERO_indicador']
for n,flag in [(215,'Alternativo_215'),(204,'Estricto_204')]:
 m=rows(f'02_hito2/matrices/matriz_{n}.csv')
 k=rows(f'02_hito2/matrices/claves_{n}.csv')
 selected=[r for r in base if r[flag]=='1']
 assert len(m)==len(k)==len(selected)==n
 assert all(list(row.keys())==fields for row in m)
 assert all(all(v and math.isfinite(float(v)) for v in row.values()) for row in m)
 assert all(a['CantonId']==b['CantonId'] for a,b in zip(k,selected))
 assert not any(col in m[0] for col in ['CantonId','Provin','NombreCantón'])
 assert all(math.isclose(float(row['CSB_cobertura']),float(s['CSB_original']),abs_tol=1e-12) for row,s in zip(m,selected))
 print('OK',n,'municipios, 5 variables, sin nulos ni identificadores')
print('OK: auditoría 221, incidencias 17, matriz principal 215 y sensibilidad 204')
