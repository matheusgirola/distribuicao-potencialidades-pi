"""Mapas LISA (univariado e bivariado) das potencialidades T-1."""
import numpy as np, pandas as pd, geopandas as gpd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from esda.moran import Moran_Local, Moran_Local_BV
from spatial_utils_t1 import carregar_malha, pesos_queen, carregar_dados, matriz_intensidade, SEED, PERM, PVAL

import os as _os
AQUI = _os.path.dirname(_os.path.abspath(__file__)).replace(chr(92), '/')   # t1_emergentes/
RAIZ = _os.path.dirname(AQUI)
OUT = AQUI + '/out_lisa'; FIG = f'{OUT}/mapas'
import os; os.makedirs(FIG, exist_ok=True)
np.random.seed(SEED)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'figure.dpi': 150, 'savefig.dpi': 150, 'savefig.bbox': 'tight'})

CQ = {'Alto-Alto': '#c0392b', 'Baixo-Baixo': '#2c6fbb', 'Alto-Baixo': '#e08e79',
      'Baixo-Alto': '#7fb0d8', 'Não significativo': '#eef1f4'}
QN = {1: 'Alto-Alto', 2: 'Baixo-Alto', 3: 'Baixo-Baixo', 4: 'Alto-Baixo'}

g = carregar_malha(); w = pesos_queen(g); d = carregar_dados()
piv = matriz_intensidade(d, g)

def mapa_uni(subclasse, titulo, fname, mostrar_bb=False):
    y = piv[subclasse].values.astype(float); yl = np.log1p(y)
    ml = Moran_Local(yl, w, permutations=PERM, seed=SEED)
    sig = ml.p_sim < PVAL
    cats = []
    for i in range(len(g)):
        if not sig[i]: cats.append('Não significativo'); continue
        q = QN[ml.q[i]]
        if q == 'Baixo-Baixo' and not mostrar_bb and y[i] == 0:
            cats.append('Não significativo')
        else:
            cats.append(q)
    gg = g.copy(); gg['cat'] = cats
    fig, ax = plt.subplots(figsize=(7.2, 7.6))
    gg.plot(ax=ax, color=[CQ[c] for c in gg.cat], edgecolor='white', linewidth=.3)
    ax.set_axis_off()
    mi = Moran_Local  # noqa
    present = [c for c in ['Alto-Alto', 'Alto-Baixo', 'Baixo-Alto', 'Baixo-Baixo', 'Não significativo'] if c in set(cats)]
    ax.legend(handles=[Patch(facecolor=CQ[c], edgecolor='#999', label=c) for c in present],
              loc='lower left', fontsize=9, frameon=True, framealpha=.95, title='Cluster LISA')
    ax.set_title(titulo, fontsize=12, fontweight='bold', pad=8)
    n_aa = cats.count('Alto-Alto')
    ax.text(.5, -.02, f'{n_aa} municípios em cluster Alto-Alto · {int((y>0).sum())} com presença · p<{PVAL}',
            transform=ax.transAxes, ha='center', fontsize=8.5, color='#555')
    fig.savefig(f'{FIG}/{fname}', facecolor='white'); plt.close(fig)
    return n_aa

def mapa_biv(X, Y, titulo, fname):
    x = piv[X].values.astype(float); y = piv[Y].values.astype(float)
    ml = Moran_Local_BV(np.log1p(x), np.log1p(y), w, permutations=PERM, seed=SEED)
    sig = ml.p_sim < PVAL
    cats = []
    for i in range(len(g)):
        if not sig[i] or x[i] == 0: cats.append('Não significativo'); continue
        cats.append(QN[ml.q[i]])
    gg = g.copy(); gg['cat'] = cats
    fig, ax = plt.subplots(figsize=(7.2, 7.6))
    gg.plot(ax=ax, color=[CQ[c] for c in gg.cat], edgecolor='white', linewidth=.3)
    ax.set_axis_off()
    present = [c for c in ['Alto-Alto', 'Alto-Baixo', 'Baixo-Alto', 'Baixo-Baixo', 'Não significativo'] if c in set(cats)]
    ax.legend(handles=[Patch(facecolor=CQ[c], edgecolor='#999', label=c) for c in present],
              loc='lower left', fontsize=9, frameon=True, framealpha=.95, title='LISA bivariado')
    ax.set_title(titulo, fontsize=11.5, fontweight='bold', pad=8)
    ax.text(.5, -.02, f'X = {X[:40]}\nvizinhança de Y = {Y[:40]} · p<{PVAL}',
            transform=ax.transAxes, ha='center', fontsize=8, color='#555')
    fig.savefig(f'{FIG}/{fname}', facecolor='white'); plt.close(fig)

# univariados-chave
mapa_uni('Serviços de comunicação multimídia - SCM', 'SCM (provedores de internet) — cluster de emergência', 'uni_scm.png')
mapa_uni('Fabricação de artefatos de cerâmica e barro cozido para uso na construção, exceto azulejos e pisos', 'Cerâmica vermelha — cluster de emergência', 'uni_ceramica.png')
mapa_uni('Soja em grão', 'Soja em grão — cluster de emergência (valor da produção)', 'uni_soja.png')
mapa_uni('Milho em grão', 'Milho em grão — cluster de emergência', 'uni_milho.png')
mapa_uni('Tilápia', 'Tilápia — cluster de emergência (piscicultura)', 'uni_tilapia.png')
mapa_uni('Tambacu tambatinga', 'Tambacu/tambatinga — cluster de emergência', 'uni_tambacu.png')

# bivariados de destaque
mapa_biv('Milho em grão', 'Mandioca', 'Bivariado: Milho × vizinhança de Mandioca', 'biv_milho_mandioca.png')
mapa_biv('Tilápia', 'Tambacu tambatinga', 'Bivariado: Tilápia × vizinhança de Tambacu', 'biv_tilapia_tambacu.png')
mapa_biv('Tambacu tambatinga', 'Fabricação de alimentos para animais', 'Bivariado: Tambacu × vizinhança de ração animal', 'biv_tambacu_racao.png')
mapa_biv('Fabricação de artefatos de cerâmica e barro cozido para uso na construção, exceto azulejos e pisos', 'Tilápia', 'Bivariado: Cerâmica × vizinhança de Tilápia', 'biv_ceramica_tilapia.png')
print('mapas gerados:', sorted(os.listdir(FIG)))
