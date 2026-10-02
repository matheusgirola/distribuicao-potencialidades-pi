# -*- coding: utf-8 -*-
"""LISA univariado (Moran_Local, esda) sob 3 matrizes W + correcao FDR,
para os dois pipelines (Estoque log1p; CE+RIE log-sinalizada).
Parametros: 999 permutacoes, seed 42, p<0.05, subclasses com >=10 municipios."""
import pickle, numpy as np, pandas as pd, time
from esda.moran import Moran_Local
from esda import fdr

with open('robustez/base.pkl','rb') as f: base = pickle.load(f)
with open('robustez/pairs.pkl','rb') as f: P = pickle.load(f)
idx = base['gdf_index']; n = len(idx); pos = {m:i for i,m in enumerate(idx)}

slog = lambda x: np.sign(x)*np.log1p(np.abs(x))
def build(df, valcol, tf):
    M = {}
    for sub,g in df.groupby('subclasse'):
        if g['mun_norm'].nunique() < 10: continue
        v = np.zeros(n); v[[pos[m] for m in g['mun_norm']]] = tf(g[valcol].values)
        M[sub] = v
    return M

pipes = {
  'estoque': build(base['est_d'], 'Estoque_mun_ano_final', np.log1p),
  'ce_rie':  build(base['ss_d'], 'ce_rie', slog),
}
Ws = {}
for name,key in [('queen','w_queen'),('knn5','w_knn5'),('invdist','w_inv')]:
    w = base[key]; w.transform='r'; Ws[name]=w

rows=[]; t0=time.time(); tot=0
for pipe,M in pipes.items():
    for sub,y in M.items():
        for wn,w in Ws.items():
            ml = Moran_Local(y, w, permutations=999, seed=42)
            sig05 = ml.p_sim < 0.05
            cut_fdr = fdr(ml.p_sim, 0.05)
            sigfdr = ml.p_sim <= cut_fdr
            lab05 = np.where(sig05, ml.q, 0)
            labfdr = np.where(sigfdr, ml.q, 0)
            rows.append(dict(pipe=pipe, sub=sub, W=wn,
                             lab05=lab05, labfdr=labfdr,
                             p=ml.p_sim.copy(), cut_fdr=cut_fdr,
                             n_sig05=int(sig05.sum()), n_sigfdr=int(sigfdr.sum())))
            tot+=1
        if tot % 300 < 3:
            print(f"{tot} rodadas | {time.time()-t0:.0f}s", flush=True)

res = pd.DataFrame(rows)
res.to_pickle('robustez/univariado.pkl')
print("rodadas:", tot, "| tempo:", round(time.time()-t0,1),"s")
for pipe in pipes:
    for wn in Ws:
        d = res[(res.pipe==pipe)&(res.W==wn)]
        print(pipe, wn, "| munic.-sig p<0.05:", d.n_sig05.sum(), "| pos-FDR:", d.n_sigfdr.sum(),
              "| subclasses c/ cluster:", (d.n_sig05>0).sum(), "->", (d.n_sigfdr>0).sum())
