"""Moran global e LISA univariado para as subclasses emergentes T-1 (base depurada).

Segue os parâmetros do projeto: Queen row-standardized, log1p, 999 permutações,
seed 42, p<0.05, mínimo de 10 municípios copresentes por subclasse.
"""
import numpy as np, pandas as pd, json, os
from esda.moran import Moran, Moran_Local
from spatial_utils_t1 import (carregar_malha, pesos_queen, carregar_dados,
                              matriz_intensidade, SEED, PERM, PVAL, MIN_UNI, QUAD_PT)

import os as _os
AQUI = _os.path.dirname(_os.path.abspath(__file__)).replace(chr(92), '/')   # t1_emergentes/
RAIZ = _os.path.dirname(AQUI)
OUT = AQUI + '/out_lisa'
os.makedirs(OUT, exist_ok=True)
np.random.seed(SEED)

g = carregar_malha()
w = pesos_queen(g)
d = carregar_dados()
piv = matriz_intensidade(d, g)   # todas as fontes juntas: cada subclasse tem sua unidade própria

# a intensidade só é comparável dentro da mesma subclasse, então tratamos coluna a coluna
subs = [c for c in piv.columns if (piv[c] > 0).sum() >= MIN_UNI]
print(f'{len(subs)} subclasses com >= {MIN_UNI} municípios presentes (de {piv.shape[1]})')

def rotulo_secao(s):
    sub = d[d.subclasse == s]
    if not len(sub):
        return ''
    sec = sub.secao_nome.iloc[0]
    if str(sec).startswith('Z'):
        return f'IBGE/{sub.fonte.iloc[0]}'
    return sec

glob_rows = []
lisa_records = []   # (subclasse, NM_MUN, quadrante, p, estoque)
for s in subs:
    y = piv[s].values.astype(float)
    yl = np.log1p(y)
    mi = Moran(yl, w, permutations=PERM)
    ml = Moran_Local(yl, w, permutations=PERM, seed=SEED)
    sig = ml.p_sim < PVAL
    n_aa = int(((ml.q == 1) & sig).sum())
    n_bb = int(((ml.q == 3) & sig).sum())
    n_ab = int(((ml.q == 4) & sig).sum())
    n_ba = int(((ml.q == 2) & sig).sum())
    glob_rows.append(dict(
        subclasse=s, secao=rotulo_secao(s),
        municipios_presentes=int((y > 0).sum()), I=round(float(mi.I), 4), p_norm=round(float(mi.p_norm), 4),
        p_sim=round(float(mi.p_sim), 4), n_sig=int(sig.sum()),
        AA=n_aa, AB=n_ab, BA=n_ba, BB=n_bb))
    lag = ml.w.sparse.dot(yl)
    for i in np.where(sig)[0]:
        # só registramos clusters onde a própria subclasse está presente (evita
        # o vasto campo de Baixo-Baixo de ausência conjunta, que não informa emergência)
        if y[i] > 0 or ml.q[i] in (1, 2):  # presente, ou vizinhança alta (spillover)
            lisa_records.append(dict(subclasse=s, secao=rotulo_secao(s), NM_MUN=g.NM_MUN.iloc[i],
                                     quadrante=QUAD_PT[ml.q[i]], p_sim=round(float(ml.p_sim[i]), 4),
                                     estoque=float(y[i]), lag=round(float(lag[i]), 3)))

gdf_glob = pd.DataFrame(glob_rows).sort_values('I', ascending=False)
gdf_glob.to_csv(f'{OUT}/moran_global_univariado.csv', index=False, sep=';', decimal=',')
lisa = pd.DataFrame(lisa_records)
lisa.to_csv(f'{OUT}/lisa_univariado_clusters.csv', index=False, sep=';', decimal=',')

sig_glob = gdf_glob[gdf_glob.p_sim < PVAL]
print(f'{len(sig_glob)} subclasses com I global significativo (p<{PVAL})')
print(sig_glob.head(20).to_string(index=False))

aa = lisa[lisa.quadrante == 'Alto-Alto']
resumo = dict(
    n_subclasses_avaliadas=len(subs),
    n_I_significativo=int(len(sig_glob)),
    I_medio=round(float(gdf_glob.I.mean()), 4),
    I_medio_sig=round(float(sig_glob.I.mean()), 4),
    total_clusters_locais_relevantes=int(len(lisa)),
    clusters_por_quadrante=lisa.quadrante.value_counts().to_dict() if len(lisa) else {},
    n_clusters_AA=int(len(aa)),
    top_AA_municipios=aa.NM_MUN.value_counts().head(15).to_dict() if len(aa) else {},
    top_AA_subclasses=aa.subclasse.value_counts().head(15).to_dict() if len(aa) else {},
)
json.dump(resumo, open(f'{OUT}/resumo_univariado.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(resumo, ensure_ascii=False, indent=1))
