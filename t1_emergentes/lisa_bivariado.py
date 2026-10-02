"""Moran bivariado (LISA bivariado) para pares de subclasses emergentes T-1.

Para cada par (X, Y) com >= MIN_BIV municípios copresentes, mede se a intensidade
de X num município se associa à intensidade de Y na sua vizinhança.
Foca nos candidatos identificados: SCM, cerâmica vermelha, soja, piscicultura.
"""
import numpy as np, pandas as pd, json, os, itertools
from esda.moran import Moran_BV, Moran_Local_BV
from spatial_utils_t1 import (carregar_malha, pesos_queen, carregar_dados,
                              matriz_intensidade, SEED, PERM, PVAL, MIN_BIV, QUAD_PT)

import os as _os
AQUI = _os.path.dirname(_os.path.abspath(__file__)).replace(chr(92), '/')   # t1_emergentes/
RAIZ = _os.path.dirname(AQUI)
OUT = AQUI + '/out_lisa'
os.makedirs(OUT, exist_ok=True)
np.random.seed(SEED)

g = carregar_malha()
w = pesos_queen(g)
d = carregar_dados()
piv = matriz_intensidade(d, g)

# subclasses candidatas de interesse (âncoras) + parceiras dentro do mesmo domínio
ANCORAS = {
    'SCM': 'Serviços de comunicação multimídia - SCM',
    'Cerâmica': 'Fabricação de artefatos de cerâmica e barro cozido para uso na construção, exceto azulejos e pisos',
    'Soja': 'Soja em grão',
    'Tilápia': 'Tilápia',
    'Tambacu': 'Tambacu tambatinga',
    'Milho': 'Milho em grão',
}
ancoras = {k: v for k, v in ANCORAS.items() if v in piv.columns}
print('âncoras disponíveis:', list(ancoras))

# candidatas a parceiras: subclasses com >= MIN_UNI presença
parceiras = [c for c in piv.columns if (piv[c] > 0).sum() >= 10]

def secao_de(s):
    sub = d[d.subclasse == s]
    if not len(sub): return ''
    sec = sub.secao_nome.iloc[0]
    return f'IBGE/{sub.fonte.iloc[0]}' if str(sec).startswith('Z') else sec

glob = []
biv_clusters = []
for nome, X in ancoras.items():
    x = piv[X].values.astype(float); xl = np.log1p(x)
    for Y in parceiras:
        if Y == X: continue
        y = piv[Y].values.astype(float)
        copres = int(((x > 0) & (y > 0)).sum())
        if copres < MIN_BIV: continue
        yl = np.log1p(y)
        mbv = Moran_BV(xl, yl, w, permutations=PERM)
        if mbv.p_z_sim >= PVAL: continue
        ml = Moran_Local_BV(xl, yl, w, permutations=PERM, seed=SEED)
        sig = ml.p_sim < PVAL
        aa = (ml.q == 1) & sig
        n_aa = int(aa.sum())
        if n_aa == 0: continue
        glob.append(dict(ancora=nome, X=X, Y=Y, secao_Y=secao_de(Y),
                         copresentes=copres, I_BV=round(float(mbv.I), 4),
                         p_sim=round(float(mbv.p_z_sim), 4), n_AA=n_aa,
                         n_sig=int(sig.sum())))
        for i in np.where(aa & (x > 0))[0]:
            biv_clusters.append(dict(ancora=nome, X=X, Y=Y, NM_MUN=g.NM_MUN.iloc[i],
                                     quadrante=QUAD_PT[ml.q[i]], p_sim=round(float(ml.p_sim[i]), 4)))

gb = pd.DataFrame(glob).sort_values(['ancora', 'I_BV'], ascending=[True, False])
gb.to_csv(f'{OUT}/moran_bivariado_pares.csv', index=False, sep=';', decimal=',')
bc = pd.DataFrame(biv_clusters)
bc.to_csv(f'{OUT}/lisa_bivariado_clusters.csv', index=False, sep=';', decimal=',')

print(f'\n{len(gb)} pares bivariados significativos (I_BV, p<{PVAL}, >=1 AA)')
for nome in ancoras:
    sub = gb[gb.ancora == nome].head(6)
    if len(sub):
        print(f'\n=== {nome} ({ancoras[nome][:50]}) ===')
        print(sub[['Y', 'secao_Y', 'copresentes', 'I_BV', 'p_sim', 'n_AA']].to_string(index=False))

resumo = dict(n_pares_significativos=len(gb),
              por_ancora=gb.ancora.value_counts().to_dict() if len(gb) else {},
              total_clusters_AA_bivariados=int(len(bc)))
json.dump(resumo, open(f'{OUT}/resumo_bivariado.json', 'w'), ensure_ascii=False, indent=1)
print('\n', json.dumps(resumo, ensure_ascii=False))
