#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hito 3 - Reto 01 GIRS 2024. Reproducible desde raiz GitHub.
Matrices derivadas de los Excel preparados Hito 2; no modifica datos ni escoge k por una métrica única.
Ejemplo: python 03_hito3/codigo/ejecutar_hito3.py
Dependencias: numpy, scipy, scikit-learn, matplotlib.
"""
from __future__ import annotations
import csv, hashlib, json, os, sys
from pathlib import Path
from itertools import combinations
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import kruskal
from scipy.optimize import linear_sum_assignment
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, silhouette_samples, adjusted_rand_score, confusion_matrix
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).resolve()
ROOT = Path(os.environ.get('GIRS_REPO_ROOT', HERE.parents[2])).resolve()
OUT = Path(os.environ.get('GIRS_OUTPUT_DIR', ROOT/'03_hito3'/'resultados')).resolve()
FIG = Path(os.environ.get('GIRS_FIG_DIR', ROOT/'03_hito3'/'figuras')).resolve()
SOURCE = ROOT/'02_hito2'
FEATS = ['CSB_cobertura','DIF_proporcion','ORG_actividad','RI_log_p95','BOTADERO_indicador']
FEAT_LABELS = ['Barrido','Diferenciada','Orgánicos','Recup. inorg.','Botadero']
KS = (2,3,4,5,6)
SEEDS = (11,23,37,52,97)
K_SELECTED = 5
SEED_SELECTED = 11
PALETTE = ('#156c8c','#d58932','#4d9b73','#8a63a8','#cf5d5d','#567286')


def readcsv(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

def savecsv(path, rows, cols=None):
    path.parent.mkdir(parents=True,exist_ok=True)
    rows = list(rows)
    if cols is None: cols = list(rows[0]) if rows else []
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore')
        writer.writeheader();writer.writerows(rows)

def jsonsave(path, payload):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(payload,ensure_ascii=False,indent=2,default=str),encoding='utf-8')

def num(r,key):
    val = r.get(key,'')
    if val is None or str(val).strip()=='': return float('nan')
    return float(str(val).replace(',','.'))

def loadscenario(n,raw):
    mat=readcsv(SOURCE/f'matrices/matriz_{n}.csv')
    keys=readcsv(SOURCE/f'matrices/claves_{n}.csv')
    assert len(mat)==len(keys)==n, f'Longitud incorrecta en escenario {n}'
    assert list(mat[0])==FEATS, 'Columnas no coinciden con contrato Hito 2'
    X=np.array([[num(x,f) for f in FEATS] for x in mat],dtype=float)
    assert X.shape==(n,5) and np.isfinite(X).all()
    ids=[x['CantonId'].strip() for x in keys]
    assert len(set(ids))==n
    assert all(k in raw for k in ids)
    return {'n':n,'X':X,'keys':keys,'ids':ids,'raw':[raw[k] for k in ids]}

def ward(X,k):
    return AgglomerativeClustering(n_clusters=k,linkage='ward',metric='euclidean').fit_predict(X)

def km(X,k,seed):
    return KMeans(n_clusters=k,random_state=seed,n_init=30,max_iter=500).fit_predict(X)

def make_colorful_plot():
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':175,
                         'axes.titleweight':'semibold','font.family':'DejaVu Sans','axes.labelcolor':'#28323f'})

def plot_save(name):
    plt.savefig(FIG/name,bbox_inches='tight',pad_inches=.12);plt.close()

def get_group_names(X,labels):
    # Descriptive labels are semantic and not an ordinal performance ranking.
    means={g:X[labels==g].mean(axis=0) for g in np.unique(labels)}
    result={}
    for g,m in means.items():
        if m[4]>.5:
            name='Botadero predominante, poca diferenciación'
        elif m[2]>.5 and m[1]>.5:
            name='Diferenciada y actividad orgánica'
        elif m[2]>.5:
            name='Actividad orgánica, poca diferenciación'
        elif m[1]>.5:
            name='Diferenciada sin actividad orgánica'
        else:
            name='Sin diferenciación ni actividad orgánica'
        result[int(g)]=name
    if len(set(result.values()))!=len(result): raise AssertionError('Revisar etiquetas descriptivas: no son únicas')
    return result

def align_count(a,b):
    a,b=np.asarray(a),np.asarray(b)
    u,v=np.unique(a),np.unique(b)
    conf=np.array([[( (a==x)&(b==y) ).sum() for y in v] for x in u])
    ri,ci=linear_sum_assignment(-conf)
    return int(conf[ri,ci].sum())

def silhouette(X,y):
    if len(np.unique(y))<2: return float('nan')
    return float(silhouette_score(X,y,metric='euclidean'))

def profiles(S,y,scores):
    X=S['X']; names=get_group_names(X,y);ids=S['ids'];raw=S['raw']
    out=[];samples=[]
    for label in np.unique(y):
        inds=np.flatnonzero(y==label); a=X[inds];rr=[raw[i] for i in inds]
        m=a.mean(0); cent=X[inds].mean(0)
        ds=np.linalg.norm(X[inds]-cent,axis=1)
        chosen=inds[np.argsort(ds)]
        eligible=[idx for idx in chosen if raw[idx].get('RI_estado','').lower() not in ['cero_ambiguo','cero contradictorio']]
        repr_inds=(eligible or list(chosen))[:3]
        nneg=int((scores[inds]<0).sum())
        relatives=np.array([num(q,'RI_intensidad') for q in rr]);ri=np.array([num(q,'RI_kg_mes') for q in rr]);crr=np.array([num(q,'CRR_ton_mes_contexto') for q in rr]);
        row={
            'id_grupo':int(label),'perfil':names[int(label)],'municipios':len(inds),
            'barrido_media_pct':round(m[0]*100,2),'barrido_mediana_pct':round(float(np.median(a[:,0]))*100,2),
            'diferenciada_media_pct':round(m[1]*100,2),'diferenciada_mediana_pct':round(float(np.median(a[:,1]))*100,2),
            'actividad_organica_pct_municipios':round(m[2]*100,2),
            'recuperacion_relativa_mediana_pct':round(float(np.nanmedian(relatives))*100,4),
            'recuperacion_relativa_media_pct':round(float(np.nanmean(relatives))*100,4),
            'RI_kg_mes_mediana':round(float(np.nanmedian(ri)),2),
            'RI_kg_mes_p75':round(float(np.nanpercentile(ri,75)),2),
            'RI_con_cantidad_positiva_pct':round(float((ri>0).mean())*100,2),
            'botadero_pct_municipios':round(m[4]*100,2),
            'CRR_ton_mes_mediana_contexto':round(float(np.nanmedian(crr)),2),
            'CRR_ton_mes_p75_contexto':round(float(np.nanpercentile(crr,75)),2),
            'silueta_media_grupo':round(float(np.mean(scores[inds])),4),
            'n_silueta_negativa':nneg,
            'n_CSB_superior_100':int(sum(X[i,0]>1 for i in inds)),
            'ceros_RI_ambiguos':sum('ambigu' in raw[i].get('RI_estado','').lower() for i in inds)
        }
        out.append(row)
        for rank,i in enumerate(repr_inds,1):
            samples.append({'id_grupo':int(label),'perfil':names[int(label)],'representatividad':rank,
                'CantonId':ids[i],'NombreCantón':S['keys'][i].get('NombreCantón',''),
                'Provin':S['keys'][i].get('Provin',''),
                'distancia_a_centroide':round(float(np.linalg.norm(X[i]-cent)),4),
                'silueta_individual':round(float(scores[i]),4)})
    return out,samples,names

def main():
    make_colorful_plot(); OUT.mkdir(parents=True,exist_ok=True);FIG.mkdir(parents=True,exist_ok=True)
    rawlist=readcsv(SOURCE/'datos/base_preparada_221.csv'); assert len(rawlist)==221
    raw={r['CantonId']:r for r in rawlist};assert len(raw)==221
    inc=readcsv(SOURCE/'datos/incidencias_17.csv');assert len(inc)==17
    scen={str(n):loadscenario(n,raw) for n in (215,204)}
    assert set(scen['204']['ids']).issubset(scen['215']['ids'])
    # No repeated geographic identifiers; repeated five-dimensional profiles are legitimate observations.
    audit={str(n):{'filas':n,'columnas':5,'identificadores_unicos':len(set(S['ids'])),
         'perfiles_vectores_unicos':len(np.unique(S['X'],axis=0)),
         'minimos':dict(zip(FEATS,np.round(S['X'].min(0),6).tolist())),
         'maximos':dict(zip(FEATS,np.round(S['X'].max(0),6).tolist()))} for n,S in scen.items()}
    assert audit['215']['perfiles_vectores_unicos']==141 and audit['204']['perfiles_vectores_unicos']==137
    jsonsave(OUT/'control_integridad.json',{'origen':'INEC GIRS 2024; matrices derivadas Hito 2',
      'escenarios':audit,'incidencias':len(inc),'algoritmos':['KMeans','Jerarquico Ward euclidiano'],'k':KS,
      'semillas':SEEDS,'n_init':30,'scikit_learn':__import__('sklearn').__version__})

    comparison=[];initrows=[];labelsets={};scoresets={}
    for sn,S in scen.items():
        X=S['X']; labels={}
        for k in KS:
            klabels={}
            for seed in SEEDS:
                y=km(X,k,seed);klabels[seed]=y
                initrows.append({'escenario':sn,'algoritmo':'K-Means','k':k,'semilla':seed,
                    'silueta_5d':round(silhouette(X,y),6),'min_grupo':int(np.bincount(y).min()),
                    'max_grupo':int(np.bincount(y).max()),'tamanos_ordenados':str(sorted(np.bincount(y).tolist()))})
            aris=[adjusted_rand_score(klabels[a],klabels[b]) for a,b in combinations(SEEDS,2)]
            mean_sil=np.mean([silhouette(X,y) for y in klabels.values()])
            lab_km=klabels[SEED_SELECTED]
            yw=ward(X,k)
            for meth,y,extra in [('K-Means',lab_km,{'ari_semillas_medio':np.mean(aris),'ari_semillas_min':np.min(aris),
                                                    'silueta_min_semillas':min(silhouette(X,l) for l in klabels.values()),
                                                    'silueta_max_semillas':max(silhouette(X,l) for l in klabels.values())}),
                                 ('Ward',yw,{'ari_semillas_medio':None,'ari_semillas_min':None,
                                             'silueta_min_semillas':None,'silueta_max_semillas':None})]:
                comparison.append({'escenario':sn,'algoritmo':meth,'k':k,'silueta_5d':round(silhouette(X,y),6),
                       'tamanos_por_cluster':';'.join(str(int(v)) for v in np.bincount(y)),'min_grupo':int(np.bincount(y).min()),
                       'max_grupo':int(np.bincount(y).max()),'ari_kmeans_vs_ward':round(adjusted_rand_score(lab_km,yw),6),
                       **{kk:(round(float(v),6) if v is not None else '') for kk,v in extra.items()}})
                labels[(meth,k)]=y
        labelsets[sn]=labels
    savecsv(OUT/'comparacion_kmeans_ward_204_215.csv',comparison)
    savecsv(OUT/'semillas_kmeans.csv',initrows)

    # Inter-scenario ARI only for 204 shared municipalities; label numbers have no ordinal meaning.
    common=sorted(set(scen['204']['ids'])&set(scen['215']['ids']))
    assert len(common)==204
    aris_changes=[]
    for method in ('K-Means','Ward'):
        for k in KS:
            l215=dict(zip(scen['215']['ids'],labelsets['215'][(method,k)]))
            l204=dict(zip(scen['204']['ids'],labelsets['204'][(method,k)]))
            one=[l215[t] for t in common];two=[l204[t] for t in common]
            aris_changes.append({'algoritmo':method,'k':k,'n_comunes':204,
                'ARI_215_contra_204':round(float(adjusted_rand_score(one,two)),6),
                'igualdad_optima_municipios':align_count(one,two),
                'cambios_optimos_municipios':len(common)-align_count(one,two)})
    savecsv(OUT/'sensibilidad_204_vs_215.csv',aris_changes)

    # Principal candidate k=5, K-Means seed 11; Ward k=5 validates agreement independently.
    X=scen['215']['X']; S=scen['215']; y=labelsets['215'][('K-Means',K_SELECTED)]
    yw=labelsets['215'][('Ward',K_SELECTED)]
    ss=silhouette_samples(X,y,metric='euclidean')
    profile,samples,names=profiles(S,y,ss)
    savecsv(OUT/'perfiles_kmeans_k5_215.csv',profile)
    savecsv(OUT/'municipios_representativos_k5.csv',samples)
    assert len(profile)==5 and sum(z['municipios'] for z in profile)==215
    members=[]
    for i,(key,rawr) in enumerate(zip(S['keys'],S['raw'])):
        members.append({'CantonId':key['CantonId'],'NombreCantón':key.get('NombreCantón',''),'Provin':key.get('Provin',''),
            'grupo_kmeans':int(y[i]),'nombre_grupo':names[int(y[i])],
            'grupo_ward':int(yw[i]),'silueta_individual':round(float(ss[i]),6),
            'CSB_original':rawr['CSB_original'],'DIF_proporcion':rawr['DIF_proporcion'],
            'ORG_indicador':rawr['ORG_indicador'],'RI_kg_mes':rawr['RI_kg_mes'],
            'RI_intensidad':rawr['RI_intensidad'],'RI_estado':rawr['RI_estado'],
            'BOTADERO_indicador':rawr['BOTADERO_indicador'],'CRR_ton_mes_contexto':rawr['CRR_ton_mes_contexto']})
    savecsv(OUT/'asignaciones_municipales_kmeans_ward_k5.csv',members)
    doubtful=[r for r in members if r['silueta_individual']<0]
    savecsv(OUT/'municipios_silueta_negativa_k5.csv',doubtful,
        cols=list(members[0]))

    # PCA: centered raw 5-D matrix as fit to clustering. Not used to calculate silhouettes.
    pca=PCA(n_components=5,svd_solver='full').fit(X)
    coords=pca.transform(X)
    expl=pca.explained_variance_ratio_
    pca_rows=[]
    for j in range(5):
        for i,f in enumerate(FEATS):
            pca_rows.append({'componente':j+1,'caracteristica':f,'peso_vector_propio':round(float(pca.components_[j,i]),7),
                  'contribucion_eje_pct':round(float(100*pca.components_[j,i]**2),4),
                  'varianza_explicada_pct':round(float(100*expl[j]),4),
                  'varianza_acumulada_pct':round(float(100*expl[:j+1].sum()),4)})
    savecsv(OUT/'pca_varianza_pesos_contribuciones.csv',pca_rows)
    coordrows=[]
    for i,key in enumerate(S['keys']):
        coordrows.append({'CantonId':key['CantonId'],'NombreCantón':key.get('NombreCantón',''),
               'PC1':round(float(coords[i,0]),6),'PC2':round(float(coords[i,1]),6),
               'grupo_kmeans':int(y[i]),'grupo_ward':int(yw[i]),'perfil_kmeans':names[int(y[i])]})
    savecsv(OUT/'pca_coordenadas_215.csv',coordrows)

    # Scale alternatives: z-score fitted once to 215. Alternative with absolute RI  (same ratio transform with fixed quantile 204).
    normalizer=StandardScaler().fit(X)
    z215=normalizer.transform(X)
    S204=scen['204'];z204=normalizer.transform(S204['X'])
    q95_abs=float(np.percentile([num(r,'RI_kg_mes') for r in S204['raw']],95))
    assert q95_abs>0
    absolute_X=X.copy()
    absolute_X[:,3]=np.log1p([num(r,'RI_kg_mes') for r in S['raw']])/np.log1p(q95_abs)
    crr=np.array([num(r,'CRR_ton_mes_contexto') for r in S['raw']])
    lncrr=np.log1p(crr)
    scale_crr=np.std(lncrr)
    contextual_X=np.column_stack([X,(lncrr-np.mean(lncrr))/scale_crr])
    sensitivity=[]
    for method in ('K-Means','Ward'):
        base=labelsets['215'][(method,K_SELECTED)]
        def lab(A):return km(A,K_SELECTED,SEED_SELECTED) if method=='K-Means' else ward(A,K_SELECTED)
        for title,AA in [('Z-score de cinco variables',z215),('RI absoluto en lugar de relativo',absolute_X),('Añadir ln(1+CRR) estandarizado',contextual_X)]:
            yl=lab(AA)
            sensitivity.append({'algoritmo':method,'experimento':title,'k':K_SELECTED,'n':215,
               'silueta_en_su_propia_matriz':round(silhouette(AA,yl),6),
               'ARI_vs_matriz_principal':round(float(adjusted_rand_score(base,yl)),6),
               'coincidencias_optimas':align_count(base,yl),'tamanos_ordenados':';'.join(map(str,sorted(np.bincount(yl).tolist())))})
    savecsv(OUT/'sensibilidad_escalado_absolutos_volumen.csv',sensitivity)
    # Additional diagnostics for how operation size varies externally by profile.
    loggroups=[np.log1p([num(S['raw'][i],'CRR_ton_mes_contexto') for i in np.flatnonzero(y==g)]) for g in range(5)]
    kw=kruskal(*loggroups)
    jsonsave(OUT/'diagnostico_escala_y_modelo.json',{
       'medianas_CRR_ton_mes':{names[g]:round(float(np.median(np.expm1(v))),2) for g,v in enumerate(loggroups)},
       'kruskal_log1p_CRR':{'estadistico':round(float(kw.statistic),6),'p_descriptivo':float(kw.pvalue),
        'nota':'Asociacion descriptiva, NO prueba causal; los grupos no son muestras aleatorias'},
       'pca_varianza_pct':list(np.round(expl*100,4)),
       'pca_varianza_acumulada_pct':list(np.round(np.cumsum(expl)*100,4)),
       'silueta_kmeans_k5':silhouette(X,y),
       'silueta_ward_k5':silhouette(X,yw),
       'ari_kmeans_ward_k5':float(adjusted_rand_score(y,yw)),
       'siluetas_negativas':len(doubtful),'grupo_kmeans_nombres':names,
       'RI_absoluto_q95_referencia_204_kg_mes':q95_abs,
       'scaler_zscore_215_media':normalizer.mean_.tolist(),
       'scaler_zscore_215_escala':normalizer.scale_.tolist()})

    # Matplotlib figures: all metrics are computed before PCA, on the actual 5D feature matrix.
    fig,ax=plt.subplots(figsize=(8.6,4.8))
    for method,c,marker in [('K-Means','#156c8c','o'),('Ward','#d58932','s')]:
        rr=[r for r in comparison if r['escenario']=='215' and r['algoritmo']==method]
        ax.plot([r['k'] for r in rr],[r['silueta_5d'] for r in rr],marker=marker,color=c,lw=2,label=method)
    ax.axvline(K_SELECTED,ls='--',color='#777',alpha=.7)
    ax.set(xticks=list(KS),xlabel='Número de grupos (k)',ylabel='Silueta promedio (en cinco dimensiones)',title='Comparación K-Means y Ward · muestra 215')
    ax.grid(alpha=.19);ax.legend();plot_save('01_comparacion_silueta.png')

    fig,ax=plt.subplots(figsize=(8.5,4.9))
    km_counts=np.bincount(y,minlength=5);wa_counts=np.bincount(yw,minlength=5);xi=np.arange(5)
    ax.bar(xi-.18,km_counts,width=.36,label='K-Means',color='#156c8c')
    ax.bar(xi+.18,wa_counts,width=.36,label='Ward',color='#d58932')
    ax.set(xticks=xi,xticklabels=[f'G{g}' for g in xi],ylabel='Municipios',title='Tamaño de grupos · k=5, 215 municipios')
    ax.legend();ax.grid(axis='y',alpha=.15);plot_save('02_tamanos_k5.png')

    for method,lab in [('kmeans',y),('ward',yw)]:
        fig,ax=plt.subplots(figsize=(8,6))
        for g in range(5):
            idx=lab==g
            ax.scatter(coords[idx,0],coords[idx,1],s=35,alpha=.75,color=PALETTE[g],label=f'G{g}: {int(idx.sum())}')
        ax.set(xlabel=f'PC1 ({expl[0]*100:.1f}% de la varianza)',ylabel=f'PC2 ({expl[1]*100:.1f}% de la varianza)',
               title=f'PCA 2D para visualizar grupos {method.upper()} · k=5')
        ax.grid(alpha=.15);ax.legend(title='Número no ordinal',ncol=2,fontsize=8)
        plot_save('03_pca_kmeans_k5.png' if method=='kmeans' else '04_pca_ward_k5.png')

    fig,ax=plt.subplots(figsize=(9,4.9))
    pc_contrib=(pca.components_[:2]**2*100).T
    w=.36;ix=np.arange(5)
    ax.bar(ix-w/2,pc_contrib[:,0],width=w,label='PC1',color='#156c8c')
    ax.bar(ix+w/2,pc_contrib[:,1],width=w,label='PC2',color='#d58932')
    ax.set(xticks=ix,xticklabels=FEAT_LABELS,ylabel='Contribución por componente (%)',
           title='Importancia de variables en PC1 y PC2 (vectores propios al cuadrado)')
    ax.legend();ax.grid(axis='y',alpha=.18);plot_save('05_pca_contribuciones.png')

    fig,ax=plt.subplots(figsize=(9.5,4.8))
    order=sorted(profile,key=lambda q:q['municipios'],reverse=True)
    features=['barrido_media_pct','diferenciada_media_pct','actividad_organica_pct_municipios','recuperacion_relativa_mediana_pct','botadero_pct_municipios']
    # Same units: all relative percent except median relative recovery percent may be small.
    data=np.array([[float(q[f]) for f in features] for q in order])
    # winsorize display at 100% only for heatmap VISUAL (not underlying fit or exported data).
    shown=np.minimum(data,100)
    h=ax.imshow(shown,aspect='auto',vmin=0,vmax=100,cmap='YlGnBu')
    ax.set(yticks=np.arange(len(order)),yticklabels=[f'G{q["id_grupo"]} · {q["municipios"]} municipios' for q in order],
           xticks=np.arange(5),xticklabels=['Barrido','Diferenciada','Orgánicos','Recuperación\nrelativa mediana','Botadero'],
           title='Perfiles municipales · k=5 (porcentajes originales)')
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            ax.text(j,i,f'{data[i,j]:.1f}',ha='center',va='center',fontsize=9,color='white' if shown[i,j]>=57 else '#17212b')
    fig.colorbar(h,ax=ax,label='Porcentaje (escala visual limitada a 100)')
    plot_save('06_perfiles_porcentajes.png')

    fig,ax=plt.subplots(figsize=(9,4.5))
    for g in range(5):
        values=ss[y==g]; vals=np.sort(values)
        ax.barh(np.arange(len(vals))+sum((y==j).sum() for j in range(g)), vals,height=.9,color=PALETTE[g],label=f'G{g}: {len(vals)}')
    ax.axvline(0,color='#333',lw=.9);ax.set(xlabel='Silueta individual en las 5 características',ylabel='Municipios ordenados por grupo',title='Calidad individual de asignación · K-Means k=5')
    ax.legend(loc='lower right',fontsize=8);plot_save('07_silueta_individual.png')

    fig,ax=plt.subplots(figsize=(8.5,4.5))
    kcomp=[r for r in comparison if r['algoritmo']=='K-Means' and r['escenario']=='215']
    kcomp204=[r for r in comparison if r['algoritmo']=='K-Means' and r['escenario']=='204']
    ax.plot(KS,[r['silueta_5d'] for r in kcomp],marker='o',label='215 municipios',color='#156c8c')
    ax.plot(KS,[r['silueta_5d'] for r in kcomp204],marker='s',label='204 municipios',color='#4d9b73')
    ax.set(xticks=list(KS),xlabel='k',ylabel='Silueta (en matriz de trabajo)',title='Sensibilidad al tratamiento de 11 ceros ambiguos')
    ax.grid(alpha=.2);ax.legend();plot_save('08_sensibilidad_204_vs_215.png')

    fig,ax=plt.subplots(figsize=(9.5,4.1))
    rawvals=X
    for j in range(5):
        vv=rawvals[:,j]
        ax.hist(vv,bins=24,alpha=.45,label=FEAT_LABELS[j])
    ax.set(xlabel='Valor numérico transformado (NO interpretable entre variables)',ylabel='Municipios',
           title='Distribuciones superpuestas · diagnóstico de escalas')
    ax.legend(fontsize=8);ax.grid(axis='y',alpha=.2);plot_save('09_distribuciones_matriz.png')

    # user-facing semantic examples and caution for the Hito 4 editorial team
    report={
       'edicion':'INEC GIRS 2024','escenario_principal':215,'escenario_sensibilidad':204,
       'metodo_principal':'K-Means', 'k_principal_propuesto':5,'semilla_representativa':11,
       'k_mas_silueta_observada':6,'k_justificacion':'Cinco perfiles distinguibles y grupos de 18 o mas; seis produce 10; k=4 permanece como contraste simplificado. No elegir solo por silueta.',
       'limitaciones':['14-? no usar; 11 ceros RI con actividad sin cantidad se mantienen como reportados en 215',
           'La matriz deriva de 41 columnas relevantes exportadas por el equipo, no sustituye archivo INEC integral 213',
           'La actividad orgánica es SI/NO de gestión declarada, no volumen tratado',
           'Grupos exploratorios, no escalafón oficial ni causal ni criterio suficiente de inversión',
           'La solución cambia bajo escalado y al incluir volumen absoluto',
           'Nombres descriptivos no equivalen a calificación de eficiencia'],
       'varianza_pc1_pct':round(float(100*expl[0]),4),'varianza_pc2_pct':round(float(100*expl[1]),4),
       'varianza_pc1_pc2_pct':round(float(100*(expl[0]+expl[1])),4),
       'perfiles':profile,'contraste':'Consultar tablas completas CSV para k=2..6, estabilidad semillas, ARI cruzado y sensibilidad.'}
    report['limitaciones'][0]='11 ceros RI con actividad reportada y cantidad cero; quedan con bandera y se comparan con escenario 204'
    jsonsave(OUT/'resumen_hito3_para_equipo.json',report)
    digest={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(OUT.glob('*')) if f.is_file()}
    jsonsave(OUT/'SHA256_resultados.json',digest)
    print('RESULTADO HITO 3')
    print('k=5 215 KMeans silhouette',round(silhouette(X,y),6),'ARI vs Ward',round(float(adjusted_rand_score(y,yw)),6))
    print('PCA (PC1, PC2, acum):',np.round([expl[0],expl[1],expl[:2].sum()]*np.array([100,100,100]),4))
    for pr in profile:print(pr['id_grupo'],pr['perfil'],pr['municipios'])
    print('Resultados',OUT,'Figuras',FIG)

if __name__=='__main__':main()
