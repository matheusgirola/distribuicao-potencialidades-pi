# -*- coding: utf-8 -*-
"""
00_base_malha_e_matrizes.py
---------------------------
Gera robustez/base.pkl, insumo de todos os demais scripts:
  - gdf_index : lista dos 224 municipios em ordem canonica (nome normalizado ASCII)
  - coords    : centroides em projecao metrica (EPSG:5880), array 224x2
  - w_queen   : contiguidade Queen (linha de base)
  - w_knn5    : k vizinhos mais proximos, k=5
  - w_inv     : distancia inversa euclidiana, banda minima conexa (76,5 km)

Insumo: shapefile oficial IBGE PI_Municipios_2025.shp (+ .shx/.dbf/.prj).
Ajuste SHP_PATH conforme o ambiente.
"""
import pickle, os
import numpy as np
import unicodedata, re
import geopandas as gpd
from libpysal.weights import Queen, KNN, DistanceBand, min_threshold_distance
import comum as C
from comum import norm

SHP_PATH = C.SHP
SAIDA = C.PKL_BASE


def main():
    os.makedirs(C.ROBUSTEZ, exist_ok=True)
    gdf = gpd.read_file(SHP_PATH)
    assert 'NM_MUN' in gdf.columns, 'shapefile sem coluna NM_MUN'
    gdf['mun_norm'] = gdf['NM_MUN'].map(norm)
    gdf = gdf.sort_values('mun_norm').reset_index(drop=True)   # ordem canonica
    assert len(gdf) == C.N_MUN, f'esperados 224 municipios, lidos {len(gdf)}'

    # Queen sobre a geometria original (EPSG:4674)
    w_queen = Queen.from_dataframe(gdf, use_index=True, silence_warnings=True)

    # matrizes de distancia sobre centroides em projecao metrica
    gdf_m = gdf.to_crs(5880)                       # SIRGAS 2000 / Brazil Polyconic
    w_knn5 = KNN.from_dataframe(gdf_m, k=5)
    cent = gdf_m.geometry.centroid
    coords = np.column_stack([cent.x, cent.y])
    thr = min_threshold_distance(coords)           # menor banda que conecta todos
    w_inv = DistanceBand(coords, threshold=thr, binary=False, alpha=-1.0,
                         silence_warnings=True)

    for nome, w in [('queen', w_queen), ('knn5', w_knn5), ('invdist', w_inv)]:
        w.transform = 'r'
        viz = np.mean(list(w.cardinalities.values()))
        print(f'{nome}: n={w.n} | ilhas={w.islands} | vizinhos medios={viz:.1f}')
    print(f'banda minima conexa (euclidiana): {thr/1000:.1f} km')

    with open(SAIDA, 'wb') as f:
        pickle.dump(dict(gdf_index=gdf['mun_norm'].tolist(), coords=coords,
                         w_queen=w_queen, w_knn5=w_knn5, w_inv=w_inv), f)
    print('gravado:', SAIDA)

if __name__ == '__main__':
    main()
