# -*- coding: utf-8 -*-
"""Constroi a matriz de distancias rodoviarias entre os 224 municipios:
grafo da malha (rodovias estaduais + federais construidas), no em intersecoes,
densificacao a cada 2 km, snap dos centroides ao no mais proximo com perna de
acesso euclidiana, Dijkstra (scipy) de todas as sedes. Gera W_rede (1/d, banda
minima conexa, padronizada por linha)."""
import numpy as np, pickle, geopandas as gpd, pandas as pd
from shapely.ops import unary_union
from shapely.geometry import LineString
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
from scipy.spatial import cKDTree
from libpysal.weights import W as PysalW
import comum as C

fe = gpd.read_file(C.RODOVIAS / 'RODOVIAS_FEDERAIS_PI.gpkg')
fe = fe[fe['ds_superfi']!='PLA']            # exclui planejadas
es = gpd.read_file(C.RODOVIAS / 'RODOVIAS_EST_PI.gpkg')
roads = pd.concat([fe[['geometry']], es[['geometry']]]).to_crs(5880)
print("trechos:", len(roads), "| extensão total (km):", round(roads.length.sum()/1000))

# nodar a rede (unary_union quebra nas interseções)
net = unary_union(roads.geometry.values)
segs = list(net.geoms) if hasattr(net,'geoms') else [net]
print("segmentos nodados:", len(segs))

# densifica e monta grafo
STEP = 2000.0
node_id, nodes = {}, []
def nid(x, y):
    k = (round(x,1), round(y,1))
    if k not in node_id:
        node_id[k] = len(nodes); nodes.append(k)
    return node_id[k]

ei, ej, ew = [], [], []

for seg in segs:
    L = seg.length
    if L == 0: continue
    npts = max(2, int(np.ceil(L/STEP))+1)
    ds = np.linspace(0, L, npts)
    pts = [seg.interpolate(d) for d in ds]
    ids = [nid(p.x, p.y) for p in pts]
    for a,b,d0,d1 in zip(ids[:-1], ids[1:], ds[:-1], ds[1:]):
        if a!=b: ei.append(a); ej.append(b); ew.append(d1-d0)
        
nodesA = np.array(nodes)
NN = len(nodesA)
A = coo_matrix((ew+ew, (ei+ej, ej+ei)), shape=(NN,NN)).tocsr()
print("nós:", NN, "| arestas:", len(ew))

# componente gigante
from scipy.sparse.csgraph import connected_components
ncomp, lab = connected_components(A, directed=False)
sizes = np.bincount(lab)
giant = sizes.argmax()
print("componentes:", ncomp, "| gigante:", sizes[giant], f"({sizes[giant]/NN:.1%})")

base = C.carregar_base()
coords = base['coords']; idx = base['gdf_index']; n = len(idx)

# snap: nó do componente gigante mais próximo de cada sede
mask = lab==giant
tree = cKDTree(nodesA[mask])
d_acc, j = tree.query(coords)
snap = np.where(mask)[0][j]
print("perna de acesso (km): média", round(d_acc.mean()/1000,1), "| máx", round(d_acc.max()/1000,1),
      "| mun. c/ acesso >20km:", int((d_acc>20000).sum()))

# dijkstra das 224 sedes
D = dijkstra(A, directed=False, indices=snap)
Dnet = D[:, snap] + d_acc[:,None] + d_acc[None,:]
np.fill_diagonal(Dnet, 0)
assert np.isfinite(Dnet).all()
# comparação com euclidiana
from scipy.spatial.distance import cdist
De = cdist(coords, coords)
iu = np.triu_indices(n,1)
ratio = Dnet[iu]/De[iu]
print("razão rede/euclidiana: mediana", round(np.median(ratio),2), "| p90", round(np.percentile(ratio,90),2))
print("correlação:", round(np.corrcoef(Dnet[iu], De[iu])[0,1],3))

# W_rede: banda mínima conexa + 1/d
row_min = np.where(np.eye(n,dtype=bool), np.inf, Dnet).min(axis=1)
thr = row_min.max()
print("banda mínima conexa (rede, km):", round(thr/1000,1))
neigh, wts = {}, {}
for i in range(n):
    js = np.where((Dnet[i]<=thr) & (np.arange(n)!=i))[0]
    neigh[i] = js.tolist(); wts[i] = (1.0/Dnet[i,js]).tolist()
w_rede = PysalW(neigh, wts, silence_warnings=True)
w_rede.transform='r'
print("W_rede: vizinhos médios:", round(np.mean(list(w_rede.cardinalities.values())),1), "| ilhas:", w_rede.islands)
with open(C.PKL_REDE,'wb') as f:
    pickle.dump(dict(Dnet=Dnet, thr=thr, w_rede=w_rede, d_acc=d_acc), f)
