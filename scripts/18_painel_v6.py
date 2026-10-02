# -*- coding: utf-8 -*-
"""Painel v6 a partir do v5 (projeto): (1) terceiro escopo 'T1+T2 · CE+RIE' na aba
Clusters Espaciais; (2) legenda dos mapas movida para o canto inferior DIREITO,
com fundo branco semitransparente."""
import json, pickle, numpy as np, pandas as pd, warnings, time, unicodedata, re
warnings.filterwarnings('ignore')
from esda.moran import Moran_Local_BV
import comum as C
from comum import norm


base = C.carregar_base()
S = C.carregar_pickle(C.ROBUSTEZ / 'ss_state.pkl')
M, pres, elig = S['M'], S['pres'], S['elig']
uni, labs, fdr_lab, rec, bq, cutb = S['uni'], S['labs'], S['fdr_lab'], S['rec'], S['bq'], S['cutb']
idx = base['gdf_index']
ALTS = ['knn5','invdist','rede','tempo']

h = open(C.SAIDAS / 'painel_potencialidades_v5.html', encoding='utf-8').read()
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
secao_old = {norm(m['rotulo']): m.get('secao','') for m in L['mapas'] if m['tipo']=='uni'}

Q2CAT = {1:0, 4:1, 2:2, 3:3}
def to_cats(lab):
    c = np.full(224, 4, dtype=int)
    for q,cat in Q2CAT.items(): c[lab==q] = cat
    return c[reorder].tolist()
def fbr(x, nd=3): return f"{x:.{nd}f}".replace('.',',')
def secao(sub): return secao_old.get(norm(sub), "MTE/RAIS")

novos = []
sig_uni = sorted([s for s in elig if uni[s]['pI']<0.05], key=lambda s:-uni[s]['I'])
for s in sig_uni:
    lab = labs[(s,'queen')]; m_ = lab!=0
    n_aa = int((lab==1).sum()); npres = int(pres[s].sum())
    nfdr = int((fdr_lab[s]!=0).sum())
    q4 = m_.copy()
    for alt in ALTS: q4 &= (labs[(s,alt)]==lab)
    subt = (f"I de Moran = {fbr(uni[s]['I'])} · {n_aa} núcleos Alto-Alto · {npres} municípios presentes "
            f"· I global signif. · pós-FDR: {nfdr} sig. · robustos às 4 W alt. (incl. rede e tempo): {int(q4.sum())}")
    novos.append(dict(tipo='uni', esc='cerie', rotulo=s, secao=secao(s),
                      I=round(float(uni[s]['I']),4), n_aa=n_aa, npres=npres,
                      subt=subt, cats=to_cats(lab)))
print("uni cerie:", len(novos))

sig_set = set(sig_uni)
posit = sorted([(a,b) for (a,b,wn),(o,p) in rec.items()
                if wn=='queen' and p<0.05 and o>0 and a in sig_set],
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
    novos.append(dict(tipo='biv', esc='cerie', rotulo=rot, secao=secao(a),
                      I=round(float(I),4), n_aa=n_aa,
                      titulo_full=f"{a} × vizinhança de {b}", subt=subt, cats=to_cats(lab)))
print("biv cerie:", len(posit), "| ★:", sum(1 for ab in posit if ab in svp),
      "| conf. 4W:", sum(1 for ab in posit if conf4(ab)), "| tempo:", round(time.time()-t0),"s")

L['mapas'] = L['mapas'] + novos
h2 = h[:s0] + json.dumps(L, ensure_ascii=False, separators=(',',':')) + h[e0:]

# --- botão do novo escopo + rótulo do escopo de estoques ---
btn_old = ('<div class="seg"> <button class="on" data-esc="tm1">Emergentes (T-1)</button> '
           '<button data-esc="t1t2">Classificadas (T1+T2)</button> </div>')
btn_new = ('<div class="seg"> <button class="on" data-esc="tm1">Emergentes (T-1)</button> '
           '<button data-esc="t1t2">T1+T2 · Estoques</button> '
           '<button data-esc="cerie">T1+T2 · CE+RIE</button> </div>')
assert btn_old in h2; h2 = h2.replace(btn_old, btn_new)

# --- introdução ---
intro_old = ("<b>Classificadas (T1+T2)</b> — setores com vantagem competitiva nacional e municipal na decomposição "
             "shift-share (T1: economia municipal dinâmica; T2: mais lenta).")
intro_new = ("<b>T1+T2 · Estoques</b> — magnitude (estoque físico e de emprego) dos setores com vantagem competitiva "
             "nacional e municipal na decomposição shift-share (T1: economia municipal dinâmica; T2: mais lenta) — e "
             "<b>T1+T2 · CE+RIE</b> — a dinâmica competitiva desses mesmos setores (soma dos componentes CE e RIE do "
             "emprego formal RAIS).")
assert intro_old in h2; h2 = h2.replace(intro_old, intro_new)
h2 = h2.replace("No escopo T1+T2, ★ indica", "Nos escopos T1+T2, ★ indica")

# --- legenda dos mapas: canto inferior direito, com fundo ---
leg_old = ("let ly=H-20-legendKeys.length*19;\n    legendKeys.forEach(k=>{\n"
           "      sv+='<rect x=\"10\" y=\"'+ly+'\" width=\"13\" height=\"13\" fill=\"'+cores[k]+'\" stroke=\"#999\" stroke-width=\".5\"/>';\n"
           "      sv+='<text x=\"28\" y=\"'+(ly+11)+'\" font-size=\"10.5\" fill=\"#333\" font-family=\"sans-serif\">'+rc[k]+'</text>';")
import re as _re
mleg = _re.search(r"let ly=H-20-legendKeys\.length\*19;\s*legendKeys\.forEach\(k=>\{\s*"
                  r"sv\+='<rect x=\"10\" y=\"'\+ly\+'\" width=\"13\" height=\"13\" fill=\"'\+cores\[k\]\+'\" stroke=\"#999\" stroke-width=\"\.5\"/>';\s*"
                  r"sv\+='<text x=\"28\" y=\"'\+\(ly\+11\)\+'\" font-size=\"10\.5\" fill=\"#333\" font-family=\"sans-serif\">'\+rc\[k\]\+'</text>';", h2)
assert mleg, "bloco da legenda não encontrado"
leg_new = ("const lx=W-122; let ly=H-20-legendKeys.length*19;\n"
           "    sv+='<rect x=\"'+(lx-8)+'\" y=\"'+(ly-8)+'\" width=\"126\" height=\"'+(legendKeys.length*19+14)+'\" "
           "fill=\"#ffffff\" opacity=\"0.85\" rx=\"4\"/>';\n"
           "    legendKeys.forEach(k=>{\n"
           "      sv+='<rect x=\"'+lx+'\" y=\"'+ly+'\" width=\"13\" height=\"13\" fill=\"'+cores[k]+'\" stroke=\"#999\" stroke-width=\".5\"/>';\n"
           "      sv+='<text x=\"'+(lx+18)+'\" y=\"'+(ly+11)+'\" font-size=\"10.5\" fill=\"#333\" font-family=\"sans-serif\">'+rc[k]+'</text>';")
h2 = h2[:mleg.start()] + leg_new + h2[mleg.end():]

out = C.SAIDAS / 'painel_potencialidades_v6.html'
open(out,'w',encoding='utf-8').write(h2)
import os
print("v6:", round(os.path.getsize(out)/1e6,2), "MB | mapas:", len(L['mapas']))
