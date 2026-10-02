# -*- coding: utf-8 -*-
"""
19_dados_planilha.py
--------------------
Gera os seis pickles consumidos por gerar_planilha.py, para os dois pipelines:
  robustez/xls_uni_est.pkl  / xls_uni_ss.pkl   (LISA univariado por subclasse,
      com contagem nominal a 9.999 permutacoes usada na taxa de FDR)
  robustez/xls_core_est.pkl / xls_core_ss.pkl  (nucleo robusto de pares)
  robustez/xls_mun_est.pkl  / xls_mun_ss.pkl   (contagens municipais de nucleos AA)

Depende de: robustez/base.pkl (00), robustez/t1t2_5w_estoque.pkl (12),
robustez/t1t2_v2_extra.pkl (10) e robustez/ss_state.pkl (16).
"""
import pickle, warnings
import numpy as np
import pandas as pd
import unicodedata, re
warnings.filterwarnings('ignore')
from esda.moran import Moran_Local, Moran_Local_BV
import geopandas as gpd
import comum as C
from comum import norm

ALTS = ['knn5', 'invdist', 'rede', 'tempo']
SHP_PATH = C.SHP


def gerar(pipe, M, pres, elig, uni, labs, fdr_lab, rec, bq, cutb, wq, idx, disp):
    n = len(idx)
    # ---- univariado por subclasse (inclui nominais a 9.999 perm.) ----
    rows = []
    for s in elig:
        lab = labs[(s, 'queen')]; m_ = lab != 0
        q4 = m_.copy()
        for alt in ALTS: q4 &= (labs[(s, alt)] == lab)
        ml9 = Moran_Local(M[s], wq, permutations=9999, seed=42, n_jobs=-1)
        rows.append(dict(subclasse=s, presentes=int(pres[s].sum()),
                         I=round(float(uni[s]['I']), 4), p=float(uni[s]['pI']),
                         sig=int(uni[s]['pI'] < 0.05), n_sig=int(m_.sum()),
                         n_aa=int((lab == 1).sum()),
                         nom9999=int((ml9.p_sim < 0.05).sum()),
                         pos_fdr=int((fdr_lab[s] != 0).sum()),
                         rob4=int(q4.sum())))
    dfu = pd.DataFrame(rows)
    dfu.to_pickle(C.ROBUSTEZ / f'xls_uni_{pipe}.pkl')

    # ---- nucleo robusto de pares + contagens municipais ----
    sig_uni = sorted([s for s in elig if uni[s]['pI'] < 0.05], key=lambda s: -uni[s]['I'])
    sig_set = set(sig_uni)
    posit = [(a, b) for (a, b, wn), (o, p) in rec.items()
             if wn == 'queen' and p < 0.05 and o > 0 and a in sig_set]
    svp = set(map(tuple, bq[(bq['p'] <= cutb) & (bq['I'] > 0)][['focal', 'parceira']].values))
    def conf4(ab):
        oq = rec[(*ab, 'queen')][0]
        return all(rec[(*ab, alt)][1] < 0.05 and np.sign(rec[(*ab, alt)][0]) == np.sign(oq)
                   for alt in ALTS)
    core = sorted([ab for ab in posit if ab in svp and conf4(ab)],
                  key=lambda ab: -rec[(*ab, 'queen')][0])
    pmap = dict(zip(map(tuple, bq[['focal', 'parceira']].values), bq['p'].values))
    aa_uni = np.zeros(n, int); aa_biv = np.zeros(n, int)
    for s in sig_uni: aa_uni += (labs[(s, 'queen')] == 1).astype(int)
    crows = []
    for k, (a, b) in enumerate(core, 1):
        mlb = Moran_Local_BV(M[a], M[b], wq, permutations=999, seed=42)
        lab = np.where(mlb.p_sim < 0.05, mlb.q, 0)
        aa_biv += (lab == 1).astype(int)
        crows.append(dict(rank=k, focal=a, parceira=b,
                          I=round(rec[(a, b, 'queen')][0], 4), p=float(pmap[(a, b)]),
                          n_aa=int((lab == 1).sum()),
                          copresentes=int((pres[a] & pres[b]).sum())))
    pd.DataFrame(crows).to_pickle(C.ROBUSTEZ / f'xls_core_{pipe}.pkl')
    pd.DataFrame(dict(mun=[disp[m] for m in idx], aa_uni=aa_uni, aa_biv=aa_biv)
                 ).to_pickle(C.ROBUSTEZ / f'xls_mun_{pipe}.pkl')
    print(f'[{pipe}] subclasses={len(dfu)} sig={dfu.sig.sum()} | nom9999={dfu.nom9999.sum()} '
          f'pos_fdr={dfu.pos_fdr.sum()} | nucleo robusto={len(core)} pares')

def main():
    base = C.carregar_base()
    idx = base['gdf_index']
    wq = base['w_queen']; wq.transform = 'r'
    gdf = gpd.read_file(SHP_PATH)
    gdf['mun_norm'] = gdf['NM_MUN'].map(norm)
    gdf = gdf.sort_values('mun_norm').reset_index(drop=True)
    disp = dict(zip(gdf['mun_norm'], gdf['NM_MUN']))

    # estoque: labs/rec do 12; global/fdr/bq do 10
    T5 = pd.read_pickle(C.ROBUSTEZ / 't1t2_5w_estoque.pkl')
    X = C.carregar_pickle(C.ROBUSTEZ / 't1t2_v2_extra.pkl')
    gerar('est', T5['M'], T5['pres'], T5['elig'], X['uni'], T5['labs'], X['fdr_lab'],
          T5['rec'], X['bq'], X['cutb'], wq, idx, disp)

    # ce_rie: estado completo do 16
    S = C.carregar_pickle(C.ROBUSTEZ / 'ss_state.pkl')
    gerar('ss', S['M'], S['pres'], S['elig'], S['uni'], S['labs'], S['fdr_lab'],
          S['rec'], S['bq'], S['cutb'], wq, idx, disp)

if __name__ == '__main__':
    main()
