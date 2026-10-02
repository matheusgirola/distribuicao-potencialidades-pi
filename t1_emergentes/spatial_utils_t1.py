"""Utilitários espaciais para a análise LISA/Moran das potencialidades T-1 (base depurada)."""
import numpy as np, pandas as pd, geopandas as gpd
from libpysal.weights import Queen

SEED = 42
PERM = 999
PVAL = 0.05
MIN_UNI = 10   # mínimo de municípios copresentes para avaliação univariada
MIN_BIV = 5    # mínimo de municípios copresentes para par bivariado

import os as _os
AQUI = _os.path.dirname(_os.path.abspath(__file__)).replace(chr(92), '/')   # t1_emergentes/
RAIZ = _os.path.dirname(AQUI)
def carregar_malha(path=RAIZ + '/dados/geo/PI_limites_municipais_2025/PI_Municipios_2025.shp'):
    g = gpd.read_file(path)
    g = g.rename(columns={'CD_MUN': 'cod_ibge'})[['cod_ibge', 'NM_MUN', 'geometry']]
    if g.crs is None or g.crs.to_epsg() != 4674:
        g = g.to_crs(4674)
    g = g.sort_values('NM_MUN').reset_index(drop=True)
    return g

def pesos_queen(gdf):
    w = Queen.from_dataframe(gdf, use_index=False)
    w.transform = 'r'   # row-standardized
    return w

def carregar_dados(path=AQUI + '/tabelas/t1_pares_final.csv', apenas_efetiva=True):
    d = pd.read_csv(path, sep=';', decimal=',')
    if apenas_efetiva:
        d = d[d.flag == 'Emergência efetiva (candidata)'].copy()
    return d

def matriz_intensidade(d, gdf, fonte=None):
    """Retorna DataFrame município x subclasse com estoque (0 onde ausente), alinhado à malha."""
    if fonte:
        d = d[d.fonte == fonte]
    piv = d.pivot_table(index='NM_MUN', columns='subclasse', values='estoque', aggfunc='max', fill_value=0)
    piv = piv.reindex(gdf.NM_MUN.values, fill_value=0)
    return piv

QUAD_PT = {1: 'Alto-Alto', 2: 'Baixo-Alto', 3: 'Baixo-Baixo', 4: 'Alto-Baixo'}
