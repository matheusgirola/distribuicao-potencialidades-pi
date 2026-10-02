import pickle, numpy as np, pandas as pd, time, warnings
warnings.filterwarnings('ignore')
from esda.moran import Moran_Local
from esda import fdr
with open('robustez/base.pkl','rb') as f: base = pickle.load(f)
idx=base['gdf_index']; n=len(idx); pos={m:i for i,m in enumerate(idx)}
slog = lambda x: np.sign(x)*np.log1p(np.abs(x))
def build(df,valcol,tf):
    M={}
    for sub,g in df.groupby('subclasse'):
        if g['mun_norm'].nunique()<10: continue
        v=np.zeros(n); v[[pos[m] for m in g['mun_norm']]]=tf(g[valcol].values); M[sub]=v
    return M
pipes={'estoque':build(base['est_d'],'Estoque_mun_ano_final',np.log1p),
       'ce_rie':build(base['ss_d'],'ce_rie',slog)}
w=base['w_queen']; w.transform='r'
rows=[]; t0=time.time(); k=0
for pipe,M in pipes.items():
    for sub,y in M.items():
        ml=Moran_Local(y,w,permutations=9999,seed=42,n_jobs=-1)
        cut=fdr(ml.p_sim,0.05)
        rows.append(dict(pipe=pipe,sub=sub,n05=int((ml.p_sim<0.05).sum()),
                         nfdr=int((ml.p_sim<=cut).sum()),cut=cut))
        k+=1
        if k%150==0: print(k, round(time.time()-t0),'s', flush=True)
pd.DataFrame(rows).to_pickle('robustez/univ_fdr9999.pkl')
print("done", k, round(time.time()-t0),"s")
