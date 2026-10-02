# Piauí T1/T2 Spatial Cluster Analysis

Spatial cluster analysis of the **T1** and **T2** potentiality subclasses from
`potencialidades_consolidado.csv`, covering all **224** municipalities of Piauí.
Mesh: official **IBGE Malha Municipal Digital 2025** (`PI_Municipios_2025`).

See **`report.md`** for the binary (presence/absence) analysis and
**`report_estoque.md`** for the value-weighted analysis using the `Estoque`
magnitude. The two analyses write to fully separate files.

## Contents

```
report.md                     Full write-up (start here)
scripts/
  spatial_utils.py            Shared geometry + Queen weights helpers
  01_build_binary_matrix.py   Binary municipio x subclasse presence matrix
  02_univariate_lisa.py       Local Moran (LISA) per subclasse -> HH clusters
  03_multivariate_spatial.py  Bivariate Moran -> HH/LL co-location clusters
  04_generate_maps.py         LISA cluster maps (PNG)
  05_overview_montage.py      Overview montage figures
  11_build_value_matrix.py    Estoque (magnitude) value matrix
  12_univariate_lisa_estoque.py    LISA on log1p(Estoque) -> HH clusters
  13_multivariate_spatial_estoque.py  Bivariate Moran on log1p(Estoque)
  14_generate_maps_estoque.py      Value LISA cluster maps
  15_overview_montage_estoque.py   Value overview montages
data/
  binary_matrix_municipios_subclasses.csv   224 x 710 presence matrix
  subclasse_prevalence.csv                  municipios per subclasse
  global_moran_by_subclasse.csv             univariate Moran + quadrant counts
  lisa_hh_clusters.csv                      significant High-High municipios
  lisa_all_significant.csv                  all significant LISA municipios
  bivariate_moran_pairs.csv                 all candidate pairs + bivariate I
  multivariate_hh_ll_clusters.csv           significant HH & LL (bivariate)
  top20_pairs.csv                           the 20 mapped pairs
  value_matrix_municipios_subclasses.csv    224 x 710 raw Estoque matrix
  subclasse_units.csv                       unit + Estoque totals per subclasse
  estoque_global_moran_by_subclasse.csv     value univariate Moran
  estoque_lisa_hh_clusters.csv              value significant High-High
  estoque_lisa_all_significant.csv          value all significant LISA
  estoque_bivariate_moran_pairs.csv         value candidate pairs + biv I
  estoque_multivariate_hh_ll_clusters.csv   value significant HH & LL
  estoque_top20_pairs.csv                   the 20 value pairs mapped
  piaui_municipios_clean.geojson            merged 224-municipio mesh (GeoJSON)
  piaui_shp_2025/                           official IBGE 2025 shapefile (+ LEIA-ME)
figures/
  overview_univariate_lisa.png              top-6 single-subclasse montage
  overview_bivariate_lisa.png               top-6 pair montage
  overview_univariate_lisa_estoque.png      value top-6 single-subclasse montage
  overview_bivariate_lisa_estoque.png       value top-6 pair montage
  univariate_lisa/uni_01..12_*.png          top 12 single-subclasse maps
  bivariate_lisa/biv_01..20_*.png           Top 20 co-located pair maps
  univariate_lisa_estoque/uni_01..12_*.png  value top 12 single-subclasse maps
  bivariate_lisa_estoque/biv_01..20_*.png   value Top 20 pair maps
```

## Estoque (magnitude) version

A parallel analysis using the continuous `Estoque_mun_ano_final` value
(log-transformed) instead of binary presence. See **`report_estoque.md`**.

```
report_estoque.md                     Full write-up for the magnitude version
scripts/E01..E05_*_estoque.py         Pipeline (mirrors 01..05)
data_estoque/
  estoque_matrix_raw.csv              raw Estoque (0 = absent)
  estoque_matrix_log.csv              log1p(Estoque), used by the statistics
  subclasse_estoque_summary.csv       per-subclasse coverage & value summary
  global_moran_by_subclasse_estoque.csv
  lisa_hh_clusters_estoque.csv / lisa_all_significant_estoque.csv
  bivariate_moran_pairs_estoque.csv / multivariate_hh_ll_clusters_estoque.csv
  top20_pairs_estoque.csv
figures_estoque/
  overview_univariate_lisa_estoque.png / overview_bivariate_lisa_estoque.png
  univariate_lisa/uni_01..12_*.png / bivariate_lisa/biv_01..20_*.png
```

## Reproduce

```bash
pip install pandas geopandas libpysal esda matplotlib mapclassify
cd scripts
python 01_build_binary_matrix.py
python 02_univariate_lisa.py
python 03_multivariate_spatial.py
python 04_generate_maps.py
python 05_overview_montage.py
```

Parameters: Queen contiguity (row-standardised), 999 permutations, seed 42,
significance p < 0.05.

## Caveats
* Presence/absence only (stock magnitude not used).
* All **224** municipios included (official IBGE 2025 mesh).
* Bivariate Moran is directional; see report §2.4.
