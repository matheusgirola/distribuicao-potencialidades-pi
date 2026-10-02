# -*- coding: utf-8 -*-
import pickle, numpy as np, pandas as pd, warnings, unicodedata, re
warnings.filterwarnings('ignore')
from esda.moran import Moran, Moran_Local
from esda import fdr
import comum as C
from comum import norm


# Carrega as matrizes de vizinhança
base = C.carregar_base()

idx=base['gdf_index']; n=len(idx); pos={m:i for i,m in enumerate(idx)}
T5 = pd.read_pickle(C.ROBUSTEZ / 't1t2_5w_estoque.pkl')   # gerado pelo 12
elig, labs, rec, pairs = T5['elig'], T5['labs'], T5['rec'], T5['pairs']

est_d = C.deduplicar(C.ler_estoque(), 'Estoque_mun_ano_final')
meta = est_d.groupby('subclasse')['Fonte'].agg(lambda x: x.mode().iloc[0]).to_dict()

M, pres = {}, {}

for sub,g in est_d.groupby('subclasse'):
    v=np.zeros(n); ii=[pos[m] for m in g['mun_norm']]
    v[ii]=np.log1p(g['Estoque_mun_ano_final'].values); M[sub]=v
    p=np.zeros(n,bool); p[ii]=True; pres[sub]=p

wq = base['w_queen']; wq.transform='r'
uni = {}
n05t=nfdrt=0
fdr_lab = {}
for sub in elig:
    mg = C.moran_global(M[sub], wq)
    ml = Moran_Local(M[sub], wq, permutations=9999, seed=42, n_jobs=-1)
    cut = fdr(ml.p_sim, 0.05)
    fdr_lab[sub] = np.where(ml.p_sim<=cut, ml.q, 0)
    n05t += int((ml.p_sim<0.05).sum()); nfdrt += int((ml.p_sim<=cut).sum())
    uni[sub] = dict(I=mg.I, pI=mg.p_sim)
print(f"[uni FDR v2] nominais={n05t} pos-FDR={nfdrt} ({nfdrt/n05t:.1%})")

# bivariado queen 9999 (FDR)
def z(v): return (v-v.mean())/v.std(ddof=1)
ZX = np.column_stack([z(M[a]) for a in elig]); fpos={a:i for i,a in enumerate(elig)}
pbp={}
for a,b in pairs: pbp.setdefault(b,[]).append(a)
den=n-1.0
rng=np.random.default_rng(42); P=np.array([rng.permutation(n) for _ in range(9999)])
U = wq.sparse.T @ ZX
rows=[]
for b,fs in pbp.items():
    zy=z(M[b]); G=zy[P]
    cols=np.array([fpos[a] for a in fs]); Ub=U[:,cols]
    obs=(Ub.T@zy)/den; sims=(G@Ub)/den
    larger=(sims>=obs[None,:]).sum(axis=0); larger=np.minimum(larger,9999-larger)
    rows += [(a,b,o,q_) for a,o,q_ in zip(fs,obs,(larger+1)/10000.0)]
bq = pd.DataFrame(rows, columns=['focal','parceira','I','p'])
cutb = fdr(bq['p'].values, 0.05)
sv = bq[(bq['p']<=cutb)]
print(f"[biv FDR v2] nominais={(bq['p']<0.05).sum()} surv={len(sv)} (I>0: {(sv['I']>0).sum()}) corte={cutb:.5f}")
# ordem deterministica: muitos pares empatam em p = 0,0001
svpos = sv[sv['I']>0].sort_values(['p','I','focal','parceira'], ascending=[True,False,True,True], kind='mergesort').rename(columns={'focal':'subclasse_focal','parceira':'subclasse_parceira','I':'moran_bv_I','p':'p_pseudo'})
svpos['moran_bv_I']=svpos['moran_bv_I'].round(4)
svpos.to_csv(C.SAIDAS / 'T1T2_pares_bivariados_pos_FDR_estoque.csv', **C.CSV_OUT)
with open(C.ROBUSTEZ / 't1t2_v2_extra.pkl','wb') as f:
    pickle.dump(dict(uni=uni, fdr_lab=fdr_lab, bq=bq, cutb=cutb, M=M, pres=pres, meta=meta), f)
print("ok")
