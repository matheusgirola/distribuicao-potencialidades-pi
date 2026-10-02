# -*- coding: utf-8 -*-
"""
00b_matriz_tempo_ors.py
-----------------------
Gera robustez/tempo.pkl (matriz W de tempo de viagem inverso) a partir das
matrizes extraidas do OpenRouteService pelo script local extrair_matriz_ors.py:
  - matriz_ors_duracao_s.csv  (tempos em segundos entre as 224 sedes)
  - matriz_ors_distancia_m.csv (distancias em metros; usada apenas em diagnostico)

Etapas:
  1. valida ordem dos municipios contra a base canonica;
  2. simetriza (a assimetria direcional observada e' desprezivel, ~0,1%);
  3. imputa pares sem rota (sedes ancoradas em trechos OSM nao roteaveis) pela
     relacao tempo~distancia ajustada por MQO sobre a matriz rodoviaria oficial
     (robustez/rede.pkl) nos pares validos;
  4. constroi W = 1/t sobre a banda minima conexa, padronizada por linha.

Depende de: robustez/base.pkl (script 00) e robustez/rede.pkl (script 08).
"""
import pickle
import numpy as np
import pandas as pd
import unicodedata, re
from libpysal.weights import W as PysalW
import comum as C
from comum import norm

DUR_CSV = C.CSV_ORS_DURACAO
DIST_CSV = C.CSV_ORS_DISTANCIA
SAIDA = C.PKL_TEMPO


def main():
    base = C.carregar_base()
    rede = C.carregar_pickle(C.PKL_REDE)
    idx = base['gdf_index']; n = len(idx)
    Dnet = rede['Dnet']                       # distancias rodoviarias oficiais (m)

    dur = pd.read_csv(DUR_CSV, sep=';', decimal=',', encoding='utf-8-sig', index_col=0)
    dis = pd.read_csv(DIST_CSV, sep=';', decimal=',', encoding='utf-8-sig', index_col=0)
    assert [norm(x) for x in dur.index] == idx and [norm(x) for x in dur.columns] == idx, \
        'ordem de municipios do CSV difere da base canonica'
    D = dur.values.astype(float)
    DM = dis.values.astype(float)

    # diagnostico e simetrizacao
    off = ~np.eye(n, dtype=bool)
    assim = np.nanmedian(np.abs(D - D.T)[off] / ((D + D.T)[off] / 2 + 1e-9))
    print(f'assimetria direcional mediana: {assim:.4f}')
    D = (D + D.T) / 2
    DM = (DM + DM.T) / 2
    mask = ~np.isnan(D)
    nan_row = np.isnan(D).sum(axis=1)
    faltantes = [idx[i] for i in np.where(nan_row >= n - 1)[0]]
    print('municipios sem rota (imputados):', faltantes)

    # imputacao: tempo ~ a + b * distancia_rede (MQO nos pares validos)
    iu = np.triu_indices(n, 1)
    v = mask[iu]
    b, a = np.polyfit(Dnet[iu][v], D[iu][v], 1)
    r2 = 1 - ((D[iu][v] - (a + b * Dnet[iu][v]))**2).sum() / ((D[iu][v] - D[iu][v].mean())**2).sum()
    print(f'imputacao: tempo = {a:.0f} + {b*1000:.1f} s/km · dist_rede | R² = {r2:.3f} '
          f'| velocidade implicita {3600/(b*1000):.0f} km/h')
    Di = D.copy()
    Di[~mask] = a + b * Dnet[~mask]
    np.fill_diagonal(Di, 0)
    assert np.isfinite(Di).all()

    valid = ~np.isnan((dur.values.astype(float))[iu])
    print(f'pares validos: {valid.sum()} de {len(iu[0])} | '
          f'corr ORS-dist vs malha oficial: '
          f'{np.corrcoef(DM[iu][v], Dnet[iu][v])[0,1]:.3f}')

    # W de tempo inverso, banda minima conexa
    row_min = np.where(np.eye(n, dtype=bool), np.inf, Di).min(axis=1)
    thr = row_min.max()
    print(f'banda minima conexa (tempo): {thr/60:.0f} min')
    neigh, wts = {}, {}
    for i in range(n):
        js = np.where((Di[i] <= thr) & (np.arange(n) != i))[0]
        neigh[i] = js.tolist(); wts[i] = (1.0 / Di[i, js]).tolist()
    w_tempo = PysalW(neigh, wts, silence_warnings=True)
    w_tempo.transform = 'r'
    print(f'W_tempo: vizinhos medios = '
          f'{np.mean(list(w_tempo.cardinalities.values())):.1f} | ilhas = {w_tempo.islands}')

    with open(SAIDA, 'wb') as f:
        pickle.dump(dict(Di=Di, thr=thr, w_tempo=w_tempo, impute=(a, b, r2)), f)
    print('gravado:', SAIDA)

if __name__ == '__main__':
    main()
