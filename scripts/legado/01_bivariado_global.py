# -*- coding: utf-8 -*-
"""Moran bivariado global (CE+RIE, transform. log-sinalizada) para todos os pares
candidatos sob tres matrizes W. Esquema de permutacao identico ao esda.Moran_BV
(zx fixo, zy permutado; validado contra esda: |dI| ~ 1e-17)."""
import pickle, numpy as np, pandas as pd, time

with open('robustez/base.pkl','rb') as f: base = pickle.load(f)
with open('robustez/pairs.pkl','rb') as f: P = pickle.load(f)
M, pairs, foc = P['M'], P['pairs'], P['foc']
n = 224
subs_all = sorted(M.keys())

Ws = {}
for name, key in [('queen','w_queen'), ('knn5','w_knn5'), ('invdist','w_inv')]:
    w = base[key]; w.transform = 'r'; Ws[name] = w.sparse

def z(v): return (v - v.mean()) / v.std(ddof=1)

ZX = np.column_stack([z(M[a]) for a in foc])            # 224 x 290
foc_pos = {a:i for i,a in enumerate(foc)}
partners = sorted({b for _,b in pairs})
pairs_by_partner = {}
for a,b in pairs: pairs_by_partner.setdefault(b, []).append(a)

rng = np.random.default_rng(42)
PIDX = np.array([rng.permutation(n) for _ in range(999)])   # 999 x 224
den = n - 1.0

rows = []
t0 = time.time()
U = {wn: Ws[wn].T @ ZX for wn in Ws}                     # 224 x 290 por W
for k,b in enumerate(partners):
    zy = z(M[b])
    G = zy[PIDX]                                          # 999 x 224
    focs_b = pairs_by_partner[b]
    cols = np.array([foc_pos[a] for a in focs_b])
    for wn in Ws:
        Ub = U[wn][:, cols]                               # 224 x k
        obs = (Ub.T @ zy) / den                           # k
        sims = (G @ Ub) / den                             # 999 x k
        larger = (sims >= obs[None,:]).sum(axis=0)
        larger = np.minimum(larger, 999 - larger)
        pvals = (larger + 1) / 1000.0
        for a, o, pv in zip(focs_b, obs, pvals):
            rows.append((a, b, wn, o, pv))
    if k % 200 == 0:
        print(f"{k}/{len(partners)} parceiros | {time.time()-t0:.0f}s", flush=True)

df = pd.DataFrame(rows, columns=['focal','parceiro','W','I','p_sim'])
df.to_pickle('robustez/bivariado_global.pkl')
print("total linhas:", len(df), "| tempo:", round(time.time()-t0,1), "s")
for wn in Ws:
    d = df[df['W']==wn]
    print(wn, "| pares sig p<0.05:", (d['p_sim']<0.05).sum())
