"""Guion reproducible para el Hito 3; NO sustituye la interpretación ni el informe.
Ejecutar desde la raíz: python 03_hito3_preparacion/experimentos_hito3.py
"""
from pathlib import Path
import csv,json,itertools
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

ROOT=Path(__file__).resolve().parents[1]
FEATS=['CSB_cobertura','DIF_proporcion','ORG_actividad','RI_log_p95','BOTADERO_indicador']
SEEDS=(11,23,37,52,97)
KS=(2,3,4,5,6)

def load(n):
    with (ROOT/f'02_hito2/matrices/matriz_{n}.csv').open(encoding='utf-8-sig',newline='') as f:
        X=np.array([[float(r[c]) for c in FEATS] for r in csv.DictReader(f)])
    with (ROOT/f'02_hito2/matrices/claves_{n}.csv').open(encoding='utf-8-sig',newline='') as f:
        keys=list(csv.DictReader(f))
    assert X.shape==(n,5) and np.isfinite(X).all() and len(keys)==n
    return X,keys

def fit(X):
    results=[]; labelmaps={}
    for k in KS:
        labels_seeds={}
        for s in SEEDS:
            labs=KMeans(n_clusters=k,n_init=30,random_state=s).fit_predict(X)
            labels_seeds[s]=labs
            sizes=np.bincount(labs,minlength=k).tolist()
            results.append({'algoritmo':'K-Means','k':k,'seed':s,'silueta_5d':round(float(silhouette_score(X,labs)),6),'tamanos':sizes})
        aris=[adjusted_rand_score(labels_seeds[a],labels_seeds[b]) for a,b in itertools.combinations(SEEDS,2)]
        for r in results:
            if r['algoritmo']=='K-Means' and r['k']==k:r['ARI_estabilidad_medio']=round(float(np.mean(aris)),6)
        labelmaps[('K-Means',k)]=labels_seeds[SEEDS[0]]
        try:
            labs=AgglomerativeClustering(n_clusters=k,linkage='ward',metric='euclidean').fit_predict(X)
        except TypeError: # compatibilidad sklearn antiguo
            labs=AgglomerativeClustering(n_clusters=k,linkage='ward',affinity='euclidean').fit_predict(X)
        results.append({'algoritmo':'Jerárquico Ward','k':k,'seed':None,'silueta_5d':round(float(silhouette_score(X,labs)),6),'tamanos':np.bincount(labs,minlength=k).tolist()})
        labelmaps[('Ward',k)]=labs
    pca=PCA(n_components=2).fit(X)
    return results,labelmaps,pca

def main():
    X215,k215=load(215); X204,k204=load(204)
    out=ROOT/'03_hito3_preparacion/resultados_piloto';out.mkdir(exist_ok=True)
    datasets=[('215_principal',X215,k215),('204_sensibilidad',X204,k204)]
    # Sensibilidad de escalado con medias/varianzas fijadas usando 215
    scaler=StandardScaler().fit(X215)
    datasets += [('215_zscore_sensibilidad',scaler.transform(X215),k215),('204_zscore_sensibilidad',scaler.transform(X204),k204)]
    label_maps={}
    for name,X,keys in datasets:
        results,labels,pca=fit(X)
        (out/f'comparacion_{name}.json').write_text(json.dumps({'escenario':name,'n':len(X),'resultados':results,'varianza_pca':pca.explained_variance_ratio_.tolist(),'varianza_acumulada':pca.explained_variance_ratio_.cumsum().tolist(),'componentes':pca.components_.tolist()},indent=2,ensure_ascii=False),encoding='utf-8')
        label_maps[name]=({r['CantonId']:int(y) for r,y in zip(keys,labels[('K-Means',3)])},labels)
        print(name,'datos',X.shape,'PCA varianza total 2 componentes',round(pca.explained_variance_ratio_.sum(),3))
    # Ejemplo comparativo sobre el universo compartido de 204 (el ARI exige el mismo conjunto).
    m215=label_maps['215_principal'][0];m204=label_maps['204_sensibilidad'][0]
    shared=sorted(set(m204)&set(m215))
    ari=adjusted_rand_score([m215[k] for k in shared],[m204[k] for k in shared])
    print('ARI entre escenarios 215 y 204 para k=3 (KMeans, semilla 11, solo compartidos):',round(float(ari),4))
    print('Resultados piloto generados en',out,'; necesitan interpretación y revisión en Hito 3')

if __name__=='__main__':main()
