# -*- coding: utf-8 -*-
"""Prepara numeros, tabelas (tab/tabelas.json) e figuras (fig/) do relatorio."""
import sys, os, json, pickle, numpy as np, pandas as pd, unicodedata, re
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import figuras as F
import geopandas as gpd
import comum as C
from comum import norm

os.makedirs(C.TAB, exist_ok=True); os.makedirs(C.FIG, exist_ok=True)
def fmt(x, d=1): return F.fmt(x, d)
def fint(x): return F.fmt(x, 0)

base = C.carregar_base()
T5 = pd.read_pickle(C.ROBUSTEZ / 't1t2_5w_estoque.pkl')
X = C.carregar_pickle(C.ROBUSTEZ / 't1t2_v2_extra.pkl')
R5 = C.carregar_pickle(C.ROBUSTEZ / 'resumo_5w.pkl')
idx = base['gdf_index']
elig, labs, rec, M, pres = T5['elig'], T5['labs'], T5['rec'], T5['M'], T5['pres']
uni, fdr_lab, bq, cutb = X['uni'], X['fdr_lab'], X['bq'], X['cutb']
ALTS = ['knn5','invdist','rede','tempo']

gdf = C.malha_ordenada()
disp = dict(zip(gdf['mun_norm'], gdf['NM_MUN']))

# ---------- descritivos ----------
est = C.ler_estoque(tipos=None)
n_reg_total = len(est)
t12 = est[est['classificacao_regiao'].isin(['T1','T2'])].copy()
t12['mun_norm'] = t12['NM_MUN'].map(norm)
n_reg_t12 = len(t12)
ded = t12.sort_values('Estoque_mun_ano_final', ascending=False).drop_duplicates(['mun_norm','subclasse'])
stats = dict(n_reg_total=n_reg_total, n_reg_t12=n_reg_t12, n_pares=len(ded),
             n_sub=int(ded['subclasse'].nunique()), n_mun=int(ded['mun_norm'].nunique()),
             n_elig=len(elig))

# ---------- univariado ----------
sig_uni = sorted([s for s in elig if uni[s]['pI']<0.05], key=lambda s:-uni[s]['I'])
stats['n_sig_uni'] = len(sig_uni)
aa_count = np.zeros(224, int)
tot_aa = 0; muns_aa = set()
lin_t1 = [["Subclasse","Municípios\npresentes","I de Moran\nglobal","p","Núcleos\nAA","Pós-FDR\n(sig.)","Robustos às\n4 W alt."]]
for s in sig_uni:
    lab = labs[(s,'queen')]; aa = lab==1
    aa_count += aa.astype(int)
    tot_aa += int(aa.sum()); muns_aa |= set(np.where(aa)[0])
for s in sig_uni[:12]:
    lab = labs[(s,'queen')]; m_ = lab!=0
    q4 = m_.copy()
    for alt in ALTS: q4 &= (labs[(s,alt)]==lab)
    lin_t1.append([s if len(s)<=52 else s[:50]+'…', fint(int(pres[s].sum())),
                   fmt(uni[s]['I'],3), fmt(uni[s]['pI'],3),
                   fint(int((lab==1).sum())), fint(int((fdr_lab[s]!=0).sum())), fint(int(q4.sum()))])
stats['tot_aa'] = tot_aa; stats['muns_aa'] = len(muns_aa)
top_mun_aa = [(disp[idx[i]], int(aa_count[i])) for i in np.argsort(-aa_count)[:14] if aa_count[i]>0]
stats['top_mun_aa'] = top_mun_aa
stats['I_max_sub'] = sig_uni[0]; stats['I_max'] = float(uni[sig_uni[0]]['I'])

# ---------- robustez (tabela 5W, estoque) ----------
u5 = R5[('estoque','uni')]; b5 = R5[('estoque','biv')]
def pct(a,b): return fmt(100*a/b,1)+'%'
lin_t2 = [["Análise","Sig. sob\nQueen","KNN-5","Dist.\ninversa","Rede\nrodoviária","Tempo de\nviagem","As 4\nalternativas"],
 ["LISA univariado", fint(u5['tot']), pct(u5['knn5'],u5['tot']), pct(u5['invdist'],u5['tot']),
  pct(u5['rede'],u5['tot']), pct(u5['tempo'],u5['tot']), pct(u5['quatro'],u5['tot'])],
 ["Moran bivariado global", fint(b5['sigq']), pct(b5['knn5'],b5['sigq']), pct(b5['invdist'],b5['sigq']),
  pct(b5['rede'],b5['sigq']), pct(b5['tempo'],b5['sigq']), pct(b5['quatro'],b5['sigq'])]]
stats['u5']=u5; stats['b5']=b5

# ---------- FDR ----------
nom_uni = sum(1 for s in elig for _ in [0])  # placeholder
n05 = 6042; nfdr = 4032   # calculados na etapa 10 (base v2, 9.999 perm.)
stats['fdr_uni'] = (n05, nfdr)
nomb = int((bq['p']<0.05).sum()); nsurv = int((bq['p']<=cutb).sum()); nsurvpos = int(((bq['p']<=cutb)&(bq['I']>0)).sum())
stats['fdr_biv'] = (nomb, nsurv, nsurvpos, float(cutb))

# ---------- bivariado: nucleo robusto ----------
sig_uni_set = set(sig_uni)
posit = [(a,b) for (a,b,wn),(o,p) in rec.items() if wn=='queen' and p<0.05 and o>0 and a in sig_uni_set]
svp = set(map(tuple, bq[(bq['p']<=cutb)&(bq['I']>0)][['focal','parceira']].values))
def conf4(ab):
    oq = rec[(*ab,'queen')][0]
    return all(rec[(*ab,alt)][1]<0.05 and np.sign(rec[(*ab,alt)][0])==np.sign(oq) for alt in ALTS)
core = [ab for ab in posit if ab in svp and conf4(ab)]
stats['n_posit']=len(posit); stats['n_fdr_focal']=sum(1 for ab in posit if ab in svp)
stats['n_conf4']=sum(1 for ab in posit if conf4(ab)); stats['n_core']=len(core)
pmap = dict(zip(map(tuple, bq[['focal','parceira']].values), bq['p'].values))
core_sorted = sorted(core, key=lambda ab: -rec[(*ab,'queen')][0])
from esda.moran import Moran_Local_BV
import warnings; warnings.filterwarnings('ignore')
wq = base['w_queen']; wq.transform='r'
aa_biv = np.zeros(224, int)
lin_t3 = [["#","Subclasse focal (x)","Subclasse parceira (lag y)","I biv.","p (9.999\nperm.)","Núcleos\nAA","Copre-\nsentes"]]
for k,(a,b) in enumerate(core_sorted, 1):
    mlb = Moran_Local_BV(M[a], M[b], wq, permutations=999, seed=42)
    lab = np.where(mlb.p_sim<0.05, mlb.q, 0)
    aa_biv += (lab==1).astype(int)
    if k<=20:
        lin_t3.append([str(k), a if len(a)<=40 else a[:38]+'…', b if len(b)<=40 else b[:38]+'…',
                       fmt(rec[(a,b,'queen')][0],3), fmt(pmap[(a,b)],4),
                       fint(int((lab==1).sum())), fint(int((pres[a]&pres[b]).sum()))])
top_mun_biv = [(disp[idx[i]], int(aa_biv[i])) for i in np.argsort(-aa_biv)[:12] if aa_biv[i]>0]
stats['top_mun_biv'] = top_mun_biv
json.dump({'t1':lin_t1,'t2':lin_t2,'t3':lin_t3}, open(C.TAB / 'tabelas.json','w'), ensure_ascii=False)

# ---------- figuras (mapas) ----------
F.aplicar_estilo()
gplot = gdf.to_crs(5880)
for nome, vals, tit in [('f1', aa_count, 'Nº de subclasses'), ('f2', aa_biv, 'Nº de pares')]:
    fig, ax = plt.subplots(figsize=(6.4, 6.2))
    v = vals.astype(float)
    gplot.assign(v=v).plot(column='v', cmap='Blues', linewidth=0.3, edgecolor='#999999',
                           legend=True, ax=ax,
                           legend_kwds={'label': tit, 'shrink': 0.55})
    # destaca contorno dos maiores
    top = np.argsort(-vals)[:8]
    gplot.iloc[top].boundary.plot(ax=ax, color=F.C['ALT'], linewidth=1.1)
    ax.set_axis_off(); ax.grid(False)
    F.salvar(fig, nome)
F.salvar_dimensoes()
json.dump(stats, open(C.TAB / 'stats.json','w'), ensure_ascii=False, default=str)
print(json.dumps({k:v for k,v in stats.items() if k not in ('u5','b5')}, ensure_ascii=False, indent=1, default=str))
