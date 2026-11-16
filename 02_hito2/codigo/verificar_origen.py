"""Auditoría independiente de los CSV exportados de los dos libros de GIRS 2024."""
import csv, math
from pathlib import Path
from collections import Counter
P=Path(__file__).resolve().parents[1]

def read(rel):
    with (P/rel).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def num(x):
    if x is None or x.strip()=='':return None
    return float(x)

def eq(a,b):
    x,y=num(a),num(b)
    return (x is None and y is None) or (x is not None and y is not None and math.isclose(x,y,rel_tol=1e-9,abs_tol=1e-10))

def required(x):
    if not x: raise AssertionError('Condición de validación no cumplida')

src=read('datos/fuente_relevante_221.csv')
prep=read('datos/base_preparada_221.csv')
inc=read('datos/incidencias_17.csv')
assert len(src)==len(prep)==221 and len(inc)==17
assert len(src[0])==41 and len(prep[0])==22
assert len({x['CantonId'] for x in prep})==221
assert [x['CantonId'] for x in src]==[x['CantonId'] for x in prep]
assert sum(x['Estricto_204']=='1' for x in prep)==204
assert sum(x['Alternativo_215']=='1' for x in prep)==215
reasons=Counter(x['Motivo_exclusion'] for x in inc)
assert reasons=={'CSB sin denominador válido':5, 'Proporción diferenciada fuera de 0-1':1, 'RI cero con material recuperado marcado':11}
assert [x['CantonId'] for x in inc]==[x['CantonId'] for x in prep if x['Estricto_204']=='0']
assert sum(x['CSB_gt1']=='1' for x in prep)==4
assert sum(x['ORG_indicador']=='1' for x in prep)==63
assert sum(x['BOTADERO_indicador']=='1' for x in prep)==35
raw_material=[x for x in src[0] if x.startswith('MR4341') and x!='MR4341_TOTAL_RES_REC']
for s,t in zip(src,prep):
    assert eq(s['CSB'],t['CSB_original'])
    a,b=num(s['DIF']),num(s['MR453'])
    dif=a/b if a is not None and b is not None and b>0 else None
    assert eq(str(dif) if dif is not None else '',t['DIF_proporcion'])
    assert eq(str(num(s['RI'])/(1000*num(s['CRR']))),t['RI_intensidad'])
    organic=1 if (s['MR441']=='1' or s['MR442']=='1') else (0 if s['MR441']=='2' and s['MR442']=='2' else None)
    assert eq('' if organic is None else str(organic),t['ORG_indicador'])
    bot=1 if s['MR461']=='3' else 0 if s['MR461'] in ('1','2') else None
    assert eq('' if bot is None else str(bot),t['BOTADERO_indicador'])
    flagged=int(any(s[k]=='1' for k in raw_material))
    assert int(t['Material_recuperado_si'])==flagged
    assert eq(s['RI'],t['RI_kg_mes'])
    assert eq(s['CRR'],t['CRR_ton_mes_contexto'])
vals=sorted(num(x['RI_intensidad']) for x in prep if x['Estricto_204']=='1')
idx=(len(vals)-1)*.95
q=vals[int(idx)]+(vals[int(idx)+1]-vals[int(idx)])*(idx-int(idx))
assert math.isclose(q,0.06698492579365073,abs_tol=1e-14)
for t in prep:
    expected=math.log1p(100*num(t['RI_intensidad']))/math.log1p(100*q)
    assert eq(t['RI_log_p95'],repr(expected))
colmap={'CSB_cobertura':'CSB_original','DIF_proporcion':'DIF_proporcion','ORG_actividad':'ORG_indicador','RI_log_p95':'RI_log_p95','BOTADERO_indicador':'BOTADERO_indicador'}
for n,flag in ((204,'Estricto_204'),(215,'Alternativo_215')):
    matrix=read(f'matrices/matriz_{n}.csv'); keys=read(f'matrices/claves_{n}.csv')
    filt=[x for x in prep if x[flag]=='1']
    assert len(matrix)==len(keys)==len(filt)==n
    for i,(m,k,s) in enumerate(zip(matrix,keys,filt),1):
        assert int(k['Fila_matriz'])==i and k['CantonId']==s['CantonId']
        assert len(m)==5 and all(v!='' for v in m.values())
        for mc,sc in colmap.items():assert eq(m[mc],s[sc])
print('OK: 221 registros de preparación, 17 incidencias, matrices 204/215, cinco cálculos, trazabilidad y escala RI.')
