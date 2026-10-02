import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon
from libpysal.weights import Queen
from libpysal.weights.spatial_lag import lag_spatial
from esda.moran import Moran, Moran_Local, Moran_Local_BV, Moran_BV

def z(v): return (v-v.mean())/v.std()

# Define coordinates for 5 square polygons
poly1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
poly2 = Polygon([(1, 0), (2, 0), (2, 1), (1, 1)])
poly3 = Polygon([(1, 1), (2, 1), (2, 2), (1, 2)])
#poly4 = Polygon([(2, 2), (3, 2), (3, 3), (2, 3)])
poly4 = Polygon([(0, 1), (1, 1), (1, 2), (0, 2)])

# Create the GeoDataFrame
gdf = gpd.GeoDataFrame(
    data={"id": [1, 2, 3, 4], 
          "name": ["Square A", "Square B", "Square C", "Square D"]},
    geometry=[poly1, poly2, poly3, poly4],
    crs="EPSG:4326"
)

print(gdf)

gdf.boundary.plot()

w_queen = Queen.from_dataframe(gdf, use_index=True, silence_warnings=True)

# Recupera a matriz de vizinhança Queen
dense_matrix, ids = w_queen.full()
print(dense_matrix)

# Normaliza a matriz de vizinhança
w_queen.transform = 'r'
dense_matrix, ids = w_queen.full()
print(dense_matrix)

# COLOCAR COLUNAS DE DADOS ------------------------------------------------------

gdf = gpd.GeoDataFrame(
    data={"id": [1, 2, 3, 4], 
          "name": ["Square A", "Square B", "Square C", "Square D"],
          "X": [90, 210, 155, 50],
          "Y": [120, 195, 140, 80]
          },
    geometry=[poly1, poly2, poly3, poly4],
    crs="EPSG:4326"
)

print(gdf)

gdf.boundary.plot()

w_queen = Queen.from_dataframe(gdf, use_index=True, silence_warnings=True)
w_queen.transform = 'r'
# Recupera a matriz de vizinhança Queen
dense_matrix, ids = w_queen.full()
print(dense_matrix)

# Já noramliza a variavel X
ml = Moran_Local(gdf["X"], w_queen, seed=12345)
print(ml.Is)

tmp = z(np.asarray(gdf[['X']]).flatten())
# Moran Local é o produto de Hammard da do vetor z com Wz
print(tmp*(dense_matrix@tmp))

# soma dos locais é proporcional (1/n) ao local
m = Moran(gdf["X"], w_queen)
print(m.I)
print(tmp@(dense_matrix@tmp)/4)

# Moran Bivariado -------------------------------------------------
lm_bv = Moran_Local_BV(gdf["Y"], gdf["X"], w_queen,
                       seed=12345)


XY = np.column_stack([z(np.asarray(gdf[[a]]).flatten()) for a in ['X','Y']])

def z(v): return (v-v.mean())/v.std(ddof = 1)

x = z(np.asarray(gdf[['X']]).flatten())
y = z(np.asarray(gdf[['Y']]).flatten())

(y.T@(dense_matrix@x))/(y*y).sum()
