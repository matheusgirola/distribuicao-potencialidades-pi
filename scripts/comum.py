# -*- coding: utf-8 -*-
"""
comum.py
--------
Caminhos, parametros e funcoes compartilhadas por todo o pipeline.

Todo script do projeto importa daqui em vez de redefinir `norm`, caminhos ou
parametros. Os caminhos sao absolutos a partir da raiz do projeto, entao os
scripts rodam de qualquer diretorio (`python scripts/12_t1t2_5w.py`).
"""
import json
import pickle
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------- caminhos
RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / 'dados'
GEO = DADOS / 'geo'
ROBUSTEZ = RAIZ / 'robustez'          # pickles intermediarios (regeneraveis)
SAIDAS = RAIZ / 'saidas'              # produtos: painel, csv, xlsx, docx
TAB = SAIDAS / 'tab'                  # tabelas json do relatorio
FIG = SAIDAS / 'fig'                  # figuras do relatorio
LOGS = RAIZ / 'logs'
INDEX_PAGES = RAIZ / 'index.html'    # painel publicado no GitHub Pages (script 23)

SHP = GEO / 'PI_limites_municipais_2025' / 'PI_Municipios_2025.shp'
SEDES = GEO / 'PI_localidades' / 'PI_localidades_2022.gpkg'
RODOVIAS = GEO / 'RODOVIAS'
CSV_ESTOQUE = DADOS / 'potencialidades_consolidado_v2.csv'
CSV_SHIFTSHARE = DADOS / 'shift-share-consolidado-Brasil.csv'
CSV_ORS_DURACAO = DADOS / 'matriz_ors_duracao_s.csv'
CSV_ORS_DISTANCIA = DADOS / 'matriz_ors_distancia_m.csv'

PKL_BASE = ROBUSTEZ / 'base.pkl'
PKL_REDE = ROBUSTEZ / 'rede.pkl'
PKL_TEMPO = ROBUSTEZ / 'tempo.pkl'

# -------------------------------------------------------------- parametros
N_MUN = 224
SEED = 42
PERM = 999            # LISA e Moran global
PERM_FDR = 9999       # LISA/bivariado usados na correcao FDR
PVAL = 0.05
MIN_UNI = 10          # municipios presentes para a subclasse entrar no univariado
MIN_BIV = 5           # municipios copresentes para o par entrar no bivariado
MIN_AA_HOTSPOT = 3    # nucleos AA ROBUSTOS as 4 W alt. para entrar no painel sem I global signif.
TIPOS_T1T2 = ('T1', 'T2')
W_NOMES = ('queen', 'knn5', 'invdist', 'rede', 'tempo')
ALTS = ('knn5', 'invdist', 'rede', 'tempo')   # matrizes alternativas a Queen

# quadrante esda (1 HH, 2 LH, 3 LL, 4 HL) -> categoria do painel
# (0 Alto-Alto, 1 Alto-Baixo, 2 Baixo-Alto, 3 Baixo-Baixo, 4 Nao signif.)
Q2CAT = {1: 0, 4: 1, 2: 2, 3: 3}
QUAD_PT = {1: 'Alto-Alto', 2: 'Baixo-Alto', 3: 'Baixo-Baixo', 4: 'Alto-Baixo'}

# formato dos CSV de saida (Excel pt-BR)
CSV_OUT = dict(sep=';', decimal=',', index=False, encoding='utf-8-sig')


# ------------------------------------------------------------------ texto
def norm(s):
    """Normalizacao canonica de nomes de municipio usada em TODO o projeto:
    sem acento, maiuscula, qualquer caractere nao alfanumerico vira espaco."""
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode().upper()
    return re.sub(r'[^A-Z0-9]+', ' ', s).strip()


def fbr(x, nd=3):
    """Numero com virgula decimal (sem separador de milhar)."""
    return f"{x:.{nd}f}".replace('.', ',')


# --------------------------------------------------------- transformacoes
def slog(x):
    """Log sinalizado: preserva o sinal de CE+RIE e comprime a magnitude."""
    return np.sign(x) * np.log1p(np.abs(x))


def z(v):
    """Padronizacao com ddof=1 (mesma do Moran bivariado global vetorizado)."""
    return (v - v.mean()) / v.std(ddof=1)


# ---------------------------------------------------------- malha e W
def carregar_pickle(caminho):
    with open(caminho, 'rb') as f:
        return pickle.load(f)


def carregar_base():
    """base.pkl (script 00): ordem canonica dos 224 municipios + W geometricas."""
    base = carregar_pickle(PKL_BASE)
    assert len(base['gdf_index']) == N_MUN
    return base


def carregar_ws(base=None, nomes=W_NOMES):
    """Dicionario {nome: W} ja padronizadas por linha, na ordem canonica."""
    base = base or carregar_base()
    todas = {'queen': lambda: base['w_queen'], 'knn5': lambda: base['w_knn5'],
             'invdist': lambda: base['w_inv'],
             'rede': lambda: carregar_pickle(PKL_REDE)['w_rede'],
             'tempo': lambda: carregar_pickle(PKL_TEMPO)['w_tempo']}
    ws = {}
    for nome in nomes:
        w = todas[nome]()
        w.transform = 'r'
        ws[nome] = w
    return ws


def nomes_exibicao(base=None):
    """{mun_norm: NM_MUN com acentos} a partir do shapefile oficial."""
    import geopandas as gpd
    gdf = gpd.read_file(SHP)
    d = dict(zip(gdf['NM_MUN'].map(norm), gdf['NM_MUN']))
    idx = (base or carregar_base())['gdf_index']
    assert set(idx) == set(d), 'shapefile e base.pkl com municipios diferentes'
    return d


def malha_ordenada():
    """GeoDataFrame da malha na ordem canonica (a mesma de base.pkl)."""
    import geopandas as gpd
    gdf = gpd.read_file(SHP)
    gdf['mun_norm'] = gdf['NM_MUN'].map(norm)
    return gdf.sort_values('mun_norm').reset_index(drop=True)


# ------------------------------------------------------------ insumos
def ler_estoque(tipos=TIPOS_T1T2):
    """Consolidado de potencialidades (estoques). `tipos=None` mantem todas as
    tipologias. Acrescenta `mun_norm`."""
    est = pd.read_csv(CSV_ESTOQUE, sep=';', decimal=',', encoding='utf-8-sig')
    if tipos is not None:
        est = est[est['classificacao_regiao'].isin(tipos)].copy()
    est['mun_norm'] = est['NM_MUN'].map(norm)
    return est


def ler_shiftshare(tipos=TIPOS_T1T2):
    """Consolidado shift-share da RAIS (latin-1), so linhas com CE e RIE
    definidos. `tipos=None` mantem todas as tipologias. Acrescenta `mun_norm`
    e `ce_rie`."""
    ss = pd.read_csv(CSV_SHIFTSHARE, sep=';', decimal=',', quotechar='"', encoding='latin-1')
    if tipos is not None:
        ss = ss[ss['classificacao_regiao'].isin(tipos)]
    ss = ss.dropna(subset=['CE', 'RIE']).copy()
    ss['mun_norm'] = ss['NM_MUN_RAIS'].str.replace('PI.', '', regex=False).map(norm)
    ss['ce_rie'] = ss['CE'] + ss['RIE']
    return ss


def deduplicar(df, valcol):
    """Uma linha por (municipio, subclasse): fica a de MAIOR `valcol` entre os
    tres anos-base. No estoque o valor e identico entre anos-base; no CE+RIE
    isso escolhe o ano-base mais favoravel (convencao do projeto)."""
    return df.sort_values(valcol, ascending=False).drop_duplicates(['mun_norm', 'subclasse'])


def montar_matriz(df, valcol, tf, idx):
    """Vetores municipio x subclasse na ordem canonica `idx`.

    Retorna (M, pres): dicionarios {subclasse: array(224)}. M guarda tf(valor)
    onde a subclasse esta presente e 0 no resto; pres e o booleano de presenca
    (a linha existe em `df`)."""
    n = len(idx)
    pos = {m: i for i, m in enumerate(idx)}
    faltam = set(df['mun_norm']) - set(pos)
    assert not faltam, f'municipios fora da malha: {sorted(faltam)[:5]}'
    M, pres = {}, {}
    for sub, g in df.groupby('subclasse'):
        ii = [pos[m] for m in g['mun_norm']]
        v = np.zeros(n)
        v[ii] = tf(g[valcol].values)
        p = np.zeros(n, bool)
        p[ii] = True
        M[sub], pres[sub] = v, p
    return M, pres


def elegiveis(pres, minimo=MIN_UNI):
    return sorted(s for s in pres if pres[s].sum() >= minimo)


# ------------------------------------------------------------- estatistica
def moran_global(y, w, permutations=PERM):
    """I de Moran global com pseudo p reprodutivel (esda.Moran nao aceita seed)."""
    from esda.moran import Moran
    np.random.seed(SEED)
    return Moran(y, w, permutations=permutations)


def lisa_rotulos(y, w, permutations=PERM, alpha=PVAL):
    """Quadrante do LISA onde p_sim < alpha, 0 no resto. Retorna (rotulos, Moran_Local)."""
    from esda.moran import Moran_Local
    ml = Moran_Local(y, w, permutations=permutations, seed=SEED, n_jobs=1)
    return np.where(ml.p_sim < alpha, ml.q, 0), ml


# ------------------------------------------------------------------ painel
def ler_lisa_painel(html):
    """Extrai o objeto `const LISA = {...}` do HTML do painel.
    Retorna (LISA, inicio, fim) com as posicoes do JSON no texto."""
    ini = html.index('const LISA = ') + len('const LISA = ')
    obj, fim = json.JSONDecoder().raw_decode(html, ini)
    return obj, ini, fim


def ler_db_painel(html):
    """Extrai o objeto `const DB = {...}` do HTML do painel."""
    ini = html.index('const DB = ') + len('const DB = ')
    obj, fim = json.JSONDecoder().raw_decode(html, ini)
    return obj, ini, fim


def gravar_lisa_painel(html, lisa, ini, fim):
    return html[:ini] + json.dumps(lisa, ensure_ascii=False, separators=(',', ':')) + html[fim:]


def reordenacao_painel(lisa, idx):
    """Indices que levam a ordem canonica `idx` para a ordem de LISA.names."""
    nomes = [norm(x) for x in lisa['names']]
    assert sorted(nomes) == sorted(idx), 'LISA.names e base.pkl com municipios diferentes'
    return np.array([idx.index(m) for m in nomes])


def para_cats(lab, reorder):
    """Rotulos de quadrante (ordem canonica) -> lista de categorias do painel."""
    c = np.full(len(lab), 4, dtype=int)
    for q, cat in Q2CAT.items():
        c[lab == q] = cat
    return c[reorder].tolist()
