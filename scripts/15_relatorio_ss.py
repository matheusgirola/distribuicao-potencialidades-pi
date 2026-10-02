# -*- coding: utf-8 -*-
"""Detalhe completo do pipeline CE+RIE (T1+T2): labs 5W, Moran global, FDR 9.999
univariado e bivariado, nucleo robusto, tabelas e figuras do relatorio paralelo."""
import sys, os, json, pickle, numpy as np, pandas as pd, unicodedata, re, warnings, time
warnings.filterwarnings('ignore')
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import figuras as F
import geopandas as gpd
from esda.moran import Moran, Moran_Local, Moran_Local_BV
from esda import fdr
import comum as C
from comum import norm

os.makedirs(C.TAB, exist_ok=True); os.makedirs(C.FIG, exist_ok=True)
fint = lambda x: F.fmt(x,0); fmt = F.fmt

base = C.carregar_base()
R5 = C.carregar_pickle(C.ROBUSTEZ / 'resumo_5w.pkl')
idx = base['gdf_index']; n=len(idx); pos={m:i for i,m in enumerate(idx)}
Ws = C.carregar_ws(base)
ALTS = ['knn5','invdist','rede','tempo']
slog = C.slog

ss = pd.read_csv(C.CSV_SHIFTSHARE,
                 sep=';', decimal=',', quotechar='"', encoding='latin-1')
n_reg_total = len(ss)
t12 = ss[ss['classificacao_regiao'].isin(['T1','T2'])].dropna(subset=['CE','RIE']).copy()
t12['mun_norm'] = t12['NM_MUN_RAIS'].str.replace('PI.','',regex=False).map(norm)
t12['ce_rie'] = t12['CE'] + t12['RIE']
ded = t12.sort_values('ce_rie', ascending=False).drop_duplicates(['mun_norm','subclasse'])
M, pres = {}, {}
for sub,g in ded.groupby('subclasse'):
    v=np.zeros(n); ii=[pos[m] for m in g['mun_norm']]
    v[ii]=slog(g['ce_rie'].values); M[sub]=v
    p=np.zeros(n,bool); p[ii]=True; pres[sub]=p
elig = sorted([s for s in M if pres[s].sum()>=10])
stats = dict(n_reg_total=n_reg_total, n_reg_t12=int(len(t12)), n_pares=int(len(ded)),
             n_sub=int(ded['subclasse'].nunique()), n_mun=int(ded['mun_norm'].nunique()),
             n_elig=len(elig), neg_share=float((ded['ce_rie']<0).mean()))

# ---- univariado: global + labs 5W + FDR 9999 ----
uni, labs, fdr_lab = {}, {}, {}
n05=nfdr=0
for sub in elig:
    mg = Moran(M[sub], Ws['queen'], permutations=999)
    uni[sub] = dict(I=float(mg.I), pI=float(mg.p_sim))
    for wn,w in Ws.items():
        ml = Moran_Local(M[sub], w, permutations=999, seed=42, n_jobs=-1)
        labs[(sub,wn)] = np.where(ml.p_sim<0.05, ml.q, 0)
    ml9 = Moran_Local(M[sub], Ws['queen'], permutations=9999, seed=42, n_jobs=-1)
    cut = fdr(ml9.p_sim, 0.05)
    fdr_lab[sub] = np.where(ml9.p_sim<=cut, ml9.q, 0)
    n05 += int((ml9.p_sim<0.05).sum()); nfdr += int((ml9.p_sim<=cut).sum())
stats['fdr_uni'] = (n05, nfdr)

sig_uni = sorted([s for s in elig if uni[s]['pI']<0.05], key=lambda s:-uni[s]['I'])
stats['n_sig_uni'] = len(sig_uni)
aa_count = np.zeros(n,int); tot_aa=0; muns=set()
for s in sig_uni:
    aa = labs[(s,'queen')]==1
    aa_count += aa.astype(int); tot_aa+=int(aa.sum()); muns |= set(np.where(aa)[0])
stats['tot_aa']=tot_aa; stats['muns_aa']=len(muns)
stats['I_max_sub']=sig_uni[0]; stats['I_max']=uni[sig_uni[0]]['I']

lin_t1 = [["Subclasse","Municípios\npresentes","I de Moran\nglobal","p","Núcleos\nAA","Pós-FDR\n(sig.)","Robustos às\n4 W alt."]]
for s in sig_uni[:12]:
    lab = labs[(s,'queen')]; m_ = lab!=0
    q4 = m_.copy()
    for alt in ALTS: q4 &= (labs[(s,alt)]==lab)
    lin_t1.append([s if len(s)<=52 else s[:50]+'…', fint(int(pres[s].sum())),
                   fmt(uni[s]['I'],3), fmt(uni[s]['pI'],3),
                   fint(int((lab==1).sum())), fint(int((fdr_lab[s]!=0).sum())), fint(int(q4.sum()))])

# ---- bivariado: rec 5W (999) + queen 9999 ----
def z(v): return (v-v.mean())/v.std(ddof=1)
pairs = [(a,b) for a in elig for b in M if b!=a and (pres[a]&pres[b]).sum()>=5]
ZX = np.column_stack([z(M[a]) for a in elig]); fpos={a:i for i,a in enumerate(elig)}
pbp={}
for a,b in pairs: pbp.setdefault(b,[]).append(a)
den=n-1.0
def grid(NP, wnames):
    rng=np.random.default_rng(42); P=np.array([rng.permutation(n) for _ in range(NP)])
    rec={}
    for wn in wnames:
        U=Ws[wn].sparse.T@ZX
        for b,fs in pbp.items():
            zy=z(M[b]); G=zy[P]; cols=np.array([fpos[a] for a in fs]); Ub=U[:,cols]
            obs=(Ub.T@zy)/den; sims=(G@Ub)/den
            larger=(sims>=obs[None,:]).sum(axis=0); larger=np.minimum(larger,NP-larger)
            for a,o,q_ in zip(fs,obs,(larger+1)/(NP+1)): rec[(a,b,wn)]=(float(o),float(q_))
    return rec
rec = grid(999, list(Ws))
bq_rows = grid(9999, ['queen'])
bq = pd.DataFrame([(a,b,o,p_) for (a,b,wn),(o,p_) in bq_rows.items()],
                  columns=['focal','parceira','I','p'])
cutb = fdr(bq['p'].values, 0.05)
stats['fdr_biv'] = (int((bq['p']<0.05).sum()), int((bq['p']<=cutb).sum()),
                    int(((bq['p']<=cutb)&(bq['I']>0)).sum()), float(cutb))
stats['n_pairs'] = len(pairs)

sig_set = set(sig_uni)
sigq = [(a,b) for a,b in pairs if rec[(a,b,'queen')][1]<0.05]
posit = [(a,b) for a,b in sigq if rec[(a,b,'queen')][0]>0 and a in sig_set]
svp = set(map(tuple, bq[(bq['p']<=cutb)&(bq['I']>0)][['focal','parceira']].values))
def conf4(ab):
    oq = rec[(*ab,'queen')][0]
    return all(rec[(*ab,alt)][1]<0.05 and np.sign(rec[(*ab,alt)][0])==np.sign(oq) for alt in ALTS)
core = sorted([ab for ab in posit if ab in svp and conf4(ab)],
              key=lambda ab: -rec[(*ab,'queen')][0])
stats['n_sigq']=len(sigq); stats['n_posit']=len(posit)
stats['n_fdr_focal']=sum(1 for ab in posit if ab in svp)
stats['n_conf4']=sum(1 for ab in posit if conf4(ab)); stats['n_core']=len(core)

pmap = dict(zip(map(tuple, bq[['focal','parceira']].values), bq['p'].values))
gdf = gpd.read_file(C.SHP)
gdf['mun_norm']=gdf['NM_MUN'].map(norm); gdf=gdf.sort_values('mun_norm').reset_index(drop=True)
disp = dict(zip(gdf['mun_norm'], gdf['NM_MUN']))
aa_biv = np.zeros(n,int); core_rows=[]
lin_t3 = [["#","Subclasse focal (x)","Subclasse parceira (lag y)","I biv.","p (9.999\nperm.)","Núcleos\nAA","Copre-\nsentes"]]
for k,(a,b) in enumerate(core,1):
    mlb = Moran_Local_BV(M[a], M[b], Ws['queen'], permutations=999, seed=42)
    lab = np.where(mlb.p_sim<0.05, mlb.q, 0)
    aa_biv += (lab==1).astype(int)
    core_rows.append(dict(rank=k, focal=a, parceira=b, I=round(rec[(a,b,'queen')][0],4),
                          p=pmap[(a,b)], n_aa=int((lab==1).sum()),
                          copresentes=int((pres[a]&pres[b]).sum())))
    if k<=20:
        lin_t3.append([str(k), a if len(a)<=40 else a[:38]+'…', b if len(b)<=40 else b[:38]+'…',
                       fmt(rec[(a,b,'queen')][0],3), fmt(pmap[(a,b)],4),
                       fint(int((lab==1).sum())), fint(int((pres[a]&pres[b]).sum()))])
stats['top_mun_aa'] = [(disp[idx[i]], int(aa_count[i])) for i in np.argsort(-aa_count)[:14] if aa_count[i]>0]
stats['top_mun_biv'] = [(disp[idx[i]], int(aa_biv[i])) for i in np.argsort(-aa_biv)[:12] if aa_biv[i]>0]

u5 = R5[('ce_rie','uni')]; b5 = R5[('ce_rie','biv')]
def pct(a,b): return fmt(100*a/b,1)+'%'
lin_t2 = [["Análise","Sig. sob\nQueen","KNN-5","Dist.\ninversa","Rede\nrodoviária","Tempo de\nviagem","As 4\nalternativas"],
 ["LISA univariado", fint(u5['tot']), pct(u5['knn5'],u5['tot']), pct(u5['invdist'],u5['tot']),
  pct(u5['rede'],u5['tot']), pct(u5['tempo'],u5['tot']), pct(u5['quatro'],u5['tot'])],
 ["Moran bivariado global", fint(b5['sigq']), pct(b5['knn5'],b5['sigq']), pct(b5['invdist'],b5['sigq']),
  pct(b5['rede'],b5['sigq']), pct(b5['tempo'],b5['sigq']), pct(b5['quatro'],b5['sigq'])]]
stats['u5']={k:int(v) for k,v in u5.items()}; stats['b5']={k:int(v) for k,v in b5.items()}

json.dump({'t1':lin_t1,'t2':lin_t2,'t3':lin_t3}, open(C.TAB / 'tabelas_ss.json','w'), ensure_ascii=False)
json.dump(stats, open(C.TAB / 'stats_ss.json','w'), ensure_ascii=False, default=str)

# figuras
F.aplicar_estilo()
gplot = gdf.to_crs(5880)
for nome, vals, tit in [('f1ss', aa_count, 'Nº de subclasses'), ('f2ss', aa_biv, 'Nº de pares')]:
    fig, ax = plt.subplots(figsize=(6.4, 6.2))
    gplot.assign(v=vals.astype(float)).plot(column='v', cmap='Blues', linewidth=0.3,
        edgecolor='#999999', legend=True, ax=ax, legend_kwds={'label': tit, 'shrink': 0.55})
    top = np.argsort(-vals)[:8]
    gplot.iloc[top].boundary.plot(ax=ax, color=F.C['ALT'], linewidth=1.1)
    ax.set_axis_off(); ax.grid(False)
    F.salvar(fig, nome)
F.salvar_dimensoes()

# dados para a planilha
uni_rows = []
for s in elig:
    lab = labs[(s,'queen')]; m_=lab!=0
    q4 = m_.copy()
    for alt in ALTS: q4 &= (labs[(s,alt)]==lab)
    uni_rows.append(dict(subclasse=s, presentes=int(pres[s].sum()), I=round(uni[s]['I'],4),
                         p=uni[s]['pI'], sig=int(uni[s]['pI']<0.05),
                         n_sig=int(m_.sum()), n_aa=int((lab==1).sum()),
                         pos_fdr=int((fdr_lab[s]!=0).sum()), rob4=int(q4.sum())))
pd.DataFrame(uni_rows).to_pickle(C.ROBUSTEZ / 'xls_uni_ss.pkl')
pd.DataFrame(core_rows).to_pickle(C.ROBUSTEZ / 'xls_core_ss.pkl')
pd.DataFrame(dict(mun=[disp[m] for m in idx], aa_uni=aa_count, aa_biv=aa_biv)).to_pickle(C.ROBUSTEZ / 'xls_mun_ss.pkl')
print(json.dumps({k:v for k,v in stats.items() if k not in ('u5','b5','top_mun_aa','top_mun_biv')},
                 ensure_ascii=False, indent=1, default=str))
print("top_mun_aa:", stats['top_mun_aa'][:8])
print("top_mun_biv:", stats['top_mun_biv'][:8])
