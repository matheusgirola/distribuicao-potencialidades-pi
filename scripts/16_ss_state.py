# -*- coding: utf-8 -*-
"""Estado completo do pipeline CE+RIE (T1+T2) para o painel e o cruzamento:
labs 5W, Moran global, fdr_lab 9999, rec bivariado 5W (999) e bq queen 9999."""
import pickle, numpy as np, pandas as pd, warnings, unicodedata, re, time
warnings.filterwarnings('ignore')
from esda.moran import Moran, Moran_Local
from esda import fdr
import comum as C
from comum import norm


base = C.carregar_base()
idx = base['gdf_index']; n=len(idx); pos={m:i for i,m in enumerate(idx)}
Ws = C.carregar_ws(base)
slog = C.slog

ded = C.deduplicar(C.ler_shiftshare(), 'ce_rie')
M, pres = {}, {}
for sub,g in ded.groupby('subclasse'):
    v=np.zeros(n); ii=[pos[m] for m in g['mun_norm']]
    v[ii]=slog(g['ce_rie'].values); M[sub]=v
    p=np.zeros(n,bool); p[ii]=True; pres[sub]=p
elig = sorted([s for s in M if pres[s].sum()>=10])

uni, labs, fdr_lab = {}, {}, {}
t0=time.time()
for sub in elig:
    mg = C.moran_global(M[sub], Ws['queen'])
    uni[sub] = dict(I=float(mg.I), pI=float(mg.p_sim))
    for wn,w in Ws.items():
        ml = Moran_Local(M[sub], w, permutations=999, seed=42, n_jobs=-1)
        labs[(sub,wn)] = np.where(ml.p_sim<0.05, ml.q, 0)
    ml9 = Moran_Local(M[sub], Ws['queen'], permutations=9999, seed=42, n_jobs=-1)
    cut = fdr(ml9.p_sim, 0.05)
    fdr_lab[sub] = np.where(ml9.p_sim<=cut, ml9.q, 0)
print("uni ok", round(time.time()-t0),"s")

def z(v): return (v-v.mean())/v.std(ddof=1)
pairs = [(a,b) for a in elig for b in M if b!=a and (pres[a]&pres[b]).sum()>=5]
ZX = np.column_stack([z(M[a]) for a in elig]); fpos={a:i for i,a in enumerate(elig)}
pbp={}
for a,b in pairs: pbp.setdefault(b,[]).append(a)
den=n-1.0
def grid(NP, wnames):
    rng=np.random.default_rng(42); P=np.array([rng.permutation(n) for _ in range(NP)])
    rec={}
    for wn in wnames:
        U=Ws[wn].sparse.T@ZX
        for b,fs in pbp.items():
            zy=z(M[b]); G=zy[P]; cols=np.array([fpos[a] for a in fs]); Ub=U[:,cols]
            obs=(Ub.T@zy)/den; sims=(G@Ub)/den
            larger=(sims>=obs[None,:]).sum(axis=0); larger=np.minimum(larger,NP-larger)
            for a,o,q_ in zip(fs,obs,(larger+1)/(NP+1)): rec[(a,b,wn)]=(float(o),float(q_))
    return rec
rec = grid(999, list(Ws))
bq_rows = grid(9999, ['queen'])
bq = pd.DataFrame([(a,b,o,p_) for (a,b,wn),(o,p_) in bq_rows.items()],
                  columns=['focal','parceira','I','p'])
cutb = float(fdr(bq['p'].values, 0.05))
print("biv ok", round(time.time()-t0),"s | cutb:", round(cutb,5))
with open(C.ROBUSTEZ / 'ss_state.pkl','wb') as f:
    pickle.dump(dict(M=M, pres=pres, elig=elig, uni=uni, labs=labs, fdr_lab=fdr_lab,
                     rec=rec, bq=bq, cutb=cutb), f)
print("estado salvo")
