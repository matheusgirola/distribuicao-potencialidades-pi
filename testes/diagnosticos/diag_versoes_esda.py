# -*- coding: utf-8 -*-
"""Diagnostico: quantos LISA divergem do pickle/painel na versao de esda instalada."""
import sys, warnings
from pathlib import Path
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
import comum as C
import esda
from esda.moran import Moran_Local

print('esda', esda.__version__, '| numpy', np.__version__)
base = C.carregar_base(); ws = C.carregar_ws(base)
t5 = pd.read_pickle(C.ROBUSTEZ / 't1t2_5w_estoque.pkl')
for nj in (1, -1):
    tot = dif = mun = 0
    for s in t5['elig']:
        for wn in ('queen', 'knn5'):
            ml = Moran_Local(t5['M'][s], ws[wn], permutations=999, seed=42, n_jobs=nj)
            lab = np.where(ml.p_sim < 0.05, ml.q, 0)
            ref = t5['labs'][(s, wn)]
            tot += 1; d = int((lab != ref).sum()); dif += d > 0; mun += d
    print(f'n_jobs={nj}: LISA divergentes {dif}/{tot}, municipios divergentes {mun}')

L = C.ler_lisa_painel((C.SAIDAS / 'painel_potencialidades_v6.html').read_text(encoding='utf-8'))[0]
reorder = C.reordenacao_painel(L, base['gdf_index'])
ss = C.deduplicar(C.ler_shiftshare(), 'ce_rie')
M, pres = C.montar_matriz(ss, 'ce_rie', C.slog, base['gdf_index'])
for nj in (1, -1):
    dif = mun = 0
    for m in [m for m in L['mapas'] if m.get('esc') == 'cerie' and m['tipo'] == 'uni']:
        ml = Moran_Local(M[m['rotulo']], ws['queen'], permutations=999, seed=42, n_jobs=nj)
        c = C.para_cats(np.where(ml.p_sim < 0.05, ml.q, 0), reorder)
        d = sum(a != b for a, b in zip(c, m['cats'])); dif += d > 0; mun += d
    print(f'cerie n_jobs={nj}: mapas divergentes {dif}/28, municipios {mun}')
