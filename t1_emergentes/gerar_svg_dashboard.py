"""Gera mapas SVG de clusters LISA (univariado e bivariado) para embutir no painel."""
import numpy as np, pandas as pd, geopandas as gpd, json, io
from esda.moran import Moran, Moran_Local, Moran_Local_BV
from spatial_utils_t1 import carregar_malha, pesos_queen, carregar_dados, matriz_intensidade, SEED, PERM, PVAL

np.random.seed(SEED)
g = carregar_malha().to_crs(4674)
w = pesos_queen(g)
d = carregar_dados()
piv = matriz_intensidade(d, g)

# geometria simplificada apenas para os SVGs embutidos (a análise usa a malha cheia)
g_svg = g.copy()
g_svg['geometry'] = g_svg.geometry.simplify(0.005, preserve_topology=True)

CQ = {'AA': '#c0392b', 'BB': '#2c6fbb', 'AB': '#e08e79', 'BA': '#7fb0d8', 'NS': '#eef1f4'}
QMAP = {1: 'AA', 2: 'BA', 3: 'BB', 4: 'AB'}

# projeção simples para viewBox
minx, miny, maxx, maxy = g_svg.total_bounds
W, H = 420, 470
pad = 8
sx = (W - 2*pad) / (maxx - minx)
sy = (H - 2*pad) / (maxy - miny)
sc = min(sx, sy)
def proj(x, y):
    px = pad + (x - minx) * sc
    py = H - pad - (y - miny) * sc
    return px, py

def path_d(geom):
    polys = geom.geoms if geom.geom_type == 'MultiPolygon' else [geom]
    dd = []
    for poly in polys:
        for ring in [poly.exterior] + list(poly.interiors):
            pts = list(ring.coords)
            seg = ' '.join(f'{proj(x,y)[0]:.1f},{proj(x,y)[1]:.1f}' for x, y in pts)
            dd.append('M' + seg + 'Z')
    return ' '.join(dd)

PATHS = [path_d(geom) for geom in g_svg.geometry]
NAMES = list(g_svg.NM_MUN)

def svg(cats, titulo, subt):
    parts = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;max-height:70vh">']
    parts.append(f'<text x="{W/2}" y="18" text-anchor="middle" font-size="13" font-weight="700" fill="#0d2f4b" font-family="sans-serif">{titulo}</text>')
    for i, p in enumerate(PATHS):
        c = CQ[cats[i]]
        parts.append(f'<path d="{p}" fill="{c}" stroke="#fff" stroke-width="0.4"><title>{NAMES[i]}</title></path>')
    # legenda
    ly = H - 96
    for lab, key in [('Alto-Alto', 'AA'), ('Alto-Baixo', 'AB'), ('Baixo-Alto', 'BA'), ('Não signif.', 'NS')]:
        if any(cats[i] == key for i in range(len(cats))) or key == 'NS':
            parts.append(f'<rect x="10" y="{ly}" width="13" height="13" fill="{CQ[key]}" stroke="#999" stroke-width=".5"/>')
            parts.append(f'<text x="28" y="{ly+11}" font-size="10.5" fill="#333" font-family="sans-serif">{lab}</text>')
            ly += 19
    parts.append(f'<text x="{W/2}" y="{H-6}" text-anchor="middle" font-size="9" fill="#666" font-family="sans-serif">{subt}</text>')
    parts.append('</svg>')
    return ''.join(parts)

def uni_cats(sub, mostrar_bb=False):
    y = piv[sub].values.astype(float)
    ml = Moran_Local(np.log1p(y), w, permutations=PERM, seed=SEED)
    sig = ml.p_sim < PVAL
    cats = []
    for i in range(len(g)):
        if not sig[i]: cats.append('NS'); continue
        q = QMAP[ml.q[i]]
        if q == 'BB' and not mostrar_bb and y[i] == 0: cats.append('NS')
        else: cats.append(q)
    n_aa = cats.count('AA')
    return cats, n_aa, int((y > 0).sum())

def biv_cats(X, Y):
    x = piv[X].values.astype(float); yv = piv[Y].values.astype(float)
    ml = Moran_Local_BV(np.log1p(x), np.log1p(yv), w, permutations=PERM, seed=SEED)
    sig = ml.p_sim < PVAL
    cats = []
    for i in range(len(g)):
        if not sig[i] or x[i] == 0: cats.append('NS')
        else: cats.append(QMAP[ml.q[i]])
    return cats, cats.count('AA')

# ---- catálogo univariado: todas as subclasses com I global significativo ----
import os as _os
AQUI = _os.path.dirname(_os.path.abspath(__file__)).replace(chr(92), '/')   # t1_emergentes/
RAIZ = _os.path.dirname(AQUI)
gl = pd.read_csv(AQUI + '/out_lisa/moran_global_univariado.csv', sep=';', decimal=',')
sig_subs = gl[gl.p_sim < PVAL].sort_values('I', ascending=False)

# ---- catálogo univariado: subclasses com hotspots locais (>=3 núcleos AA) ----
# Incluímos mesmo quando o I global não é significativo: uma atividade muito
# difundida (ex.: SCM em 111 municípios) pode ter I global ~0 e, ainda assim,
# formar hotspots locais nítidos. O critério de interesse é o cluster local.
gl = pd.read_csv(AQUI + '/out_lisa/moran_global_univariado.csv', sep=';', decimal=',')
gl = gl.sort_values('I', ascending=False)

CATCODE = {'AA': 0, 'AB': 1, 'BA': 2, 'BB': 3, 'NS': 4}
MIN_AA = 3
catalog = []
for _, r in gl.iterrows():
    sub = r['subclasse']
    cats, n_aa, npres = uni_cats(sub)
    if n_aa < MIN_AA:
        continue
    gsig = ' · I global signif.' if r['p_sim'] < PVAL else ' · hotspots locais'
    catalog.append(dict(tipo='uni', rotulo=sub, secao=str(r['secao']),
                        I=round(float(r['I']), 4), n_aa=int(n_aa), npres=int(npres),
                        subt=f"I de Moran = {str(r['I']).replace('.',',')} · {n_aa} núcleos Alto-Alto · {npres} municípios presentes{gsig}",
                        cats=[CATCODE[c] for c in cats]))
catalog.sort(key=lambda c: c['n_aa'], reverse=True)

# ---- catálogo bivariado: melhores pares ----
bv = pd.read_csv(AQUI + '/out_lisa/moran_bivariado_pares.csv', sep=';', decimal=',')
bv = bv[bv.I_BV > 0].sort_values('I_BV', ascending=False).head(24)
biv_cat = []
for _, r in bv.iterrows():
    cats, n_aa = biv_cats(r['X'], r['Y'])
    if n_aa == 0: continue
    biv_cat.append(dict(tipo='biv', rotulo=f"{r['X'][:30]} × {r['Y'][:30]}", secao=str(r['secao_Y']),
                        I=round(float(r['I_BV']), 4), n_aa=int(n_aa),
                        titulo_full=f"{r['X']} × vizinhança de {r['Y']}",
                        subt=f"I bivariado = {str(r['I_BV']).replace('.',',')} · {n_aa} núcleos AA · {int(r['copresentes'])} copresentes",
                        cats=[CATCODE[c] for c in cats]))
catalog = catalog + biv_cat

print('mapas no catálogo:', len(catalog), '| uni:', sum(1 for c in catalog if c['tipo']=='uni'), '| biv:', sum(1 for c in catalog if c['tipo']=='biv'))
bundle = dict(W=W, H=H, paths=PATHS, names=NAMES,
              cores=['#c0392b', '#e08e79', '#7fb0d8', '#2c6fbb', '#eef1f4'],
              rotulos_cat=['Alto-Alto', 'Alto-Baixo', 'Baixo-Alto', 'Baixo-Baixo', 'Não signif.'],
              mapas=catalog)
json.dump(bundle, open(AQUI + '/out_lisa/catalogo_svg.json', 'w'), ensure_ascii=False, separators=(',', ':'))
sz = len(json.dumps(bundle, ensure_ascii=False, separators=(',', ':')))
print('tamanho JSON:', round(sz/1e6, 2), 'MB')
