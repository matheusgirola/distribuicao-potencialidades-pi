# -*- coding: utf-8 -*-
"""Cruzamento formal dos nucleos robustos (340 estoques x 50 CE+RIE):
pares comuns (nao ordenados), I em cada pipeline, municipios AA convergentes,
figura de convergencia e tabelas do relatorio unificado."""
import sys, os, json, pickle, numpy as np, pandas as pd, unicodedata, re, warnings
warnings.filterwarnings('ignore')
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import figuras as F
import geopandas as gpd
from esda.moran import Moran_Local_BV
import comum as C
from comum import norm

fint = lambda x: F.fmt(x,0); fmt = F.fmt

base = C.carregar_base()
idx = base['gdf_index']; n=224
wq = base['w_queen']; wq.transform='r'
EST = pd.read_pickle(C.ROBUSTEZ / 't1t2_5w_estoque.pkl')
SSs = C.carregar_pickle(C.ROBUSTEZ / 'ss_state.pkl')
ce = pd.read_pickle(C.ROBUSTEZ / 'xls_core_est.pkl')
cs = pd.read_pickle(C.ROBUSTEZ / 'xls_core_ss.pkl')
for d in (ce, cs):
    d['fn'] = d['focal'].map(norm); d['pn'] = d['parceira'].map(norm)

# mapeia norm -> nome original por pipeline
e_disp = {norm(k):k for k in EST['M']}
s_disp = {norm(k):k for k in SSs['M']}

eu = {}
for _,r in ce.iterrows(): eu.setdefault(frozenset((r['fn'],r['pn'])), []).append(r)
su = {}
for _,r in cs.iterrows(): su.setdefault(frozenset((r['fn'],r['pn'])), []).append(r)
comuns = sorted(set(eu) & set(su), key=lambda k: -(max(x['I'] for x in eu[k]) + max(x['I'] for x in su[k])))
print("pares comuns:", len(comuns))

def aa_set(Mdict, a, b):
    mlb = Moran_Local_BV(Mdict[a], Mdict[b], wq, permutations=999, seed=42)
    return set(np.where((mlb.p_sim<0.05)&(mlb.q==1))[0])

gdf = gpd.read_file(C.SHP)
gdf['mun_norm']=gdf['NM_MUN'].map(norm); gdf=gdf.sort_values('mun_norm').reset_index(drop=True)
disp = dict(zip(gdf['mun_norm'], gdf['NM_MUN']))

conv_count = np.zeros(n,int)
rows=[]
lin_t6 = [["#","Par de subclasses","I biv.\nEstoques","I biv.\nCE+RIE","AA conv.\n(municípios)"]]
for k,key in enumerate(comuns,1):
    fs = sorted(key)
    Ie = max(x['I'] for x in eu[key]); Is = max(x['I'] for x in su[key])
    aa_e = set()
    for x in eu[key]: aa_e |= aa_set(EST['M'], e_disp[x['fn']], e_disp[x['pn']])
    aa_s = set()
    for x in su[key]: aa_s |= aa_set(SSs['M'], s_disp[x['fn']], s_disp[x['pn']])
    conv = aa_e & aa_s
    for i in conv: conv_count[i]+=1
    nome = ' × '.join(s_disp.get(f, e_disp.get(f,f)) for f in fs)
    rows.append(dict(rank=k, par=nome, I_est=Ie, I_ss=Is,
                     aa_est=len(aa_e), aa_ss=len(aa_s), aa_conv=len(conv),
                     municipios_conv='; '.join(sorted(disp[idx[i]] for i in conv))))
    nm = nome if len(nome)<=72 else nome[:70]+'…'
    lin_t6.append([str(k), nm, fmt(Ie,3), fmt(Is,3), fint(len(conv))])
dfc = pd.DataFrame(rows)
dfc.to_pickle(C.ROBUSTEZ / 'xls_cross.pkl')
print("média AA convergentes/par:", round(dfc['aa_conv'].mean(),1),
      "| pares com >=1 conv:", int((dfc['aa_conv']>0).sum()))
top_conv = [(disp[idx[i]], int(conv_count[i])) for i in np.argsort(-conv_count)[:12] if conv_count[i]>0]
print("top municípios convergentes:", top_conv[:10])

# figura de convergência
F.aplicar_estilo()
gplot = gdf.to_crs(5880)
fig, ax = plt.subplots(figsize=(6.4, 6.2))
gplot.assign(v=conv_count.astype(float)).plot(column='v', cmap='Blues', linewidth=0.3,
    edgecolor='#999999', legend=True, ax=ax, legend_kwds={'label':'Nº de pares do duplo núcleo','shrink':0.55})
top = np.argsort(-conv_count)[:8]
gplot.iloc[top].boundary.plot(ax=ax, color=F.C['ALT'], linewidth=1.1)
ax.set_axis_off(); ax.grid(False)
F.salvar(fig, 'f5conv')
F.salvar_dimensoes()

# tabelas unificadas: reaproveita as existentes e monta a de robustez combinada
Te = json.load(open(C.TAB / 'tabelas.json'))
Ts = json.load(open(C.TAB / 'tabelas_ss.json'))
t3 = [["Análise","Sig. sob\nQueen","KNN-5","Dist.\ninversa","Rede\nrodoviária","Tempo de\nviagem","As 4\nalternativas"],
      ["Estoques — LISA univariado"] + Te['t2'][1][1:],
      ["Estoques — Moran biv. global"] + Te['t2'][2][1:],
      ["CE+RIE — LISA univariado"] + Ts['t2'][1][1:],
      ["CE+RIE — Moran biv. global"] + Ts['t2'][2][1:]]
json.dump({'t1':Te['t1'], 't2':Ts['t1'], 't3':t3, 't4':Te['t3'], 't5':Ts['t3'], 't6':lin_t6},
          open(C.TAB / 'tabelas_unif.json','w'), ensure_ascii=False)
stats = dict(n_comuns=len(comuns), aa_conv_media=float(dfc['aa_conv'].mean()),
             pares_com_conv=int((dfc['aa_conv']>0).sum()), top_conv=top_conv,
             soma_conv=int(conv_count.sum()), muns_conv=int((conv_count>0).sum()))
json.dump(stats, open(C.TAB / 'stats_cross.json','w'), ensure_ascii=False, default=str)
print("ok")
