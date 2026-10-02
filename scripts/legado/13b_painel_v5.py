# -*- coding: utf-8 -*-
"""Painel v5 a partir do v4 (ja com dois escopos): substitui os mapas do escopo
t1t2 por versoes com flags de robustez sob 4 matrizes alternativas (KNN-5,
dist. inversa, rede rodoviaria, tempo de viagem ORS) e atualiza a introducao."""
import json, pickle, numpy as np, pandas as pd, warnings, time, unicodedata, re
warnings.filterwarnings('ignore')
from esda.moran import Moran_Local_BV

def norm(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii','ignore').decode().upper()
    return re.sub(r'[^A-Z0-9]+',' ', s).strip()

with open('robustez/base.pkl','rb') as f: base = pickle.load(f)
T5 = pd.read_pickle('robustez/t1t2_5w_estoque.pkl')
with open('robustez/t1t2_v2_extra.pkl','rb') as f: X = pickle.load(f)
elig, labs, rec, M, pres = T5['elig'], T5['labs'], T5['rec'], T5['M'], T5['pres']
uni, fdr_lab, bq, cutb, meta = X['uni'], X['fdr_lab'], X['bq'], X['cutb'], X['meta']
idx = base['gdf_index']
ALTS = ['knn5','invdist','rede','tempo']

h = open('/mnt/project/painel_potencialidades_v4.html', encoding='utf-8').read()
s0 = h.index('const LISA = ') + len('const LISA = ')
depth=0
for i,c in enumerate(h[s0:], s0):
    if c=='{': depth+=1
    elif c=='}':
        depth-=1
        if depth==0: e0=i+1; break
L = json.loads(h[s0:e0])
painel_names = [norm(x) for x in L['names']]
reorder = np.array([idx.index(m) for m in painel_names])
secao_old = {m['rotulo']: m.get('secao','') for m in L['mapas'] if m['tipo']=='uni'}
L['mapas'] = [m for m in L['mapas'] if m.get('esc','tm1')!='t1t2']   # remove t1t2 antigos
print("mapas tm1 preservados:", len(L['mapas']))

Q2CAT = {1:0, 4:1, 2:2, 3:3}
def to_cats(lab):
    c = np.full(224, 4, dtype=int)
    for q,cat in Q2CAT.items(): c[lab==q] = cat
    return c[reorder].tolist()
def fbr(x, nd=3): return f"{x:.{nd}f}".replace('.',',')
def secao(sub):
    if sub in secao_old: return secao_old[sub]
    f = meta.get(sub,'')
    return f"IBGE/{f}" if f in ('PAM','PPM','PEVS') else "MTE/RAIS"

novos = []
sig_uni = sorted([s for s in elig if uni[s]['pI']<0.05], key=lambda s:-uni[s]['I'])
for s in sig_uni:
    lab = labs[(s,'queen')]; m_ = lab!=0
    n_aa = int((lab==1).sum()); npres = int(pres[s].sum())
    nfdr = int((fdr_lab[s]!=0).sum())
    q4 = m_.copy()
    for alt in ALTS: q4 = q4 & (labs[(s,alt)]==lab)
    subt = (f"I de Moran = {fbr(uni[s]['I'])} · {n_aa} núcleos Alto-Alto · {npres} municípios presentes "
            f"· I global signif. · pós-FDR: {nfdr} sig. · robustos às 4 W alt. (incl. rede e tempo): {int(q4.sum())}")
    novos.append(dict(tipo='uni', esc='t1t2', rotulo=s, secao=secao(s),
                      I=round(float(uni[s]['I']),4), n_aa=n_aa, npres=npres,
                      subt=subt, cats=to_cats(lab)))
print("uni:", len(novos))

sig_uni_set = set(sig_uni)
posit = sorted([(a,b) for (a,b,wn),(o,p) in rec.items()
                if wn=='queen' and p<0.05 and o>0 and a in sig_uni_set],
               key=lambda ab: -rec[(ab[0],ab[1],'queen')][0])
svp = set(map(tuple, bq[(bq['p']<=cutb)&(bq['I']>0)][['focal','parceira']].values))
def conf4(ab):
    oq = rec[(*ab,'queen')][0]
    return all(rec[(*ab,alt)][1]<0.05 and np.sign(rec[(*ab,alt)][0])==np.sign(oq) for alt in ALTS)
wq = base['w_queen']; wq.transform='r'
t0=time.time()
for k,(a,b) in enumerate(posit):
    mlb = Moran_Local_BV(M[a], M[b], wq, permutations=999, seed=42)
    lab = np.where(mlb.p_sim<0.05, mlb.q, 0)
    n_aa = int((lab==1).sum()); cop = int((pres[a]&pres[b]).sum())
    I = rec[(a,b,'queen')][0]
    rob = (a,b) in svp; c4 = conf4((a,b))
    rot = ('★ ' if rob else '') + a[:30] + ' × ' + b[:30]
    subt = (f"I bivariado = {fbr(I,4)} · {n_aa} núcleos AA · {cop} copresentes"
            + (" · robusto (FDR)" if rob else "") + (" · confirmado sob as 4 W alt." if c4 else ""))
    novos.append(dict(tipo='biv', esc='t1t2', rotulo=rot, secao=secao(a),
                      I=round(float(I),4), n_aa=n_aa,
                      titulo_full=f"{a} × vizinhança de {b}", subt=subt, cats=to_cats(lab)))
    if k%400==0: print(k, round(time.time()-t0),'s', flush=True)
print("biv:", len(posit), "| ★:", sum(1 for ab in posit if ab in svp),
      "| conf. 4W:", sum(1 for ab in posit if conf4(ab)))

L['mapas'] = L['mapas'] + novos
h2 = h[:s0] + json.dumps(L, ensure_ascii=False, separators=(',',':')) + h[e0:]

intro_old = ("incluindo uma matriz de <b>distância rodoviária</b> "
             "construída sobre a malha viária estadual e federal (13,9 mil km).")
intro_new = ("incluindo uma matriz de <b>distância rodoviária</b> (malha estadual e federal, 13,9 mil km) "
             "e uma de <b>tempo de viagem</b> entre sedes municipais (OpenRouteService/OpenStreetMap).")
assert intro_old in h2, "texto de introdução do v4 não encontrado"
h2 = h2.replace(intro_old, intro_new)

out = '/mnt/user-data/outputs/painel_potencialidades_v5.html'
open(out,'w',encoding='utf-8').write(h2)
import os
print("v5:", round(os.path.getsize(out)/1e6,2), "MB | mapas:", len(L['mapas']))
