# -*- coding: utf-8 -*-
"""Cenario T1+T2 sob QUATRO matrizes: Queen, KNN-5, dist. inversa euclidiana e
dist. inversa RODOVIARIA (nova). Univariado (LISA) e bivariado global,
pipelines Estoque e CE+RIE."""
import pickle, numpy as np, pandas as pd, warnings, unicodedata, re, time
warnings.filterwarnings('ignore')
from esda.moran import Moran, Moran_Local

def norm(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii','ignore').decode().upper()
    return re.sub(r'[^A-Z0-9]+',' ', s).strip()

with open('robustez/base.pkl','rb') as f: base = pickle.load(f)
with open('robustez/rede.pkl','rb') as f: rede = pickle.load(f)
idx = base['gdf_index']; n=len(idx); pos={m:i for i,m in enumerate(idx)}
slog = lambda x: np.sign(x)*np.log1p(np.abs(x))

Ws = {'queen':base['w_queen'], 'knn5':base['w_knn5'], 'invdist':base['w_inv'], 'rede':rede['w_rede']}
for w in Ws.values(): w.transform='r'

def build(df, valcol, tf):
    M, pres = {}, {}
    for sub,g in df.groupby('subclasse'):
        v=np.zeros(n); ii=[pos[m] for m in g['mun_norm']]
        v[ii]=tf(g[valcol].values); M[sub]=v
        p=np.zeros(n,bool); p[ii]=True; pres[sub]=p
    return M, pres

est = pd.read_csv('/mnt/project/potencialidades_consolidado_v2.csv', sep=';', decimal=',', encoding='utf-8-sig')
est = est[est['classificacao_regiao'].isin(['T1','T2'])].copy()
est['mun_norm'] = est['NM_MUN'].map(norm)
est_d = est.sort_values('Estoque_mun_ano_final', ascending=False).drop_duplicates(['mun_norm','subclasse'])

ss = pd.read_csv('/mnt/user-data/uploads/shift-share-consolidado-Brasil.csv', sep=';', decimal=',', quotechar='"', encoding='latin-1')
ss = ss[ss['classificacao_regiao'].isin(['T1','T2'])].dropna(subset=['CE','RIE']).copy()
ss['mun_norm'] = ss['NM_MUN_RAIS'].str.replace('PI.','',regex=False).map(norm)
ss['ce_rie'] = ss['CE']+ss['RIE']
ss_d = ss.sort_values('ce_rie', ascending=False).drop_duplicates(['mun_norm','subclasse'])

resumo = {}
detalhe_rows = []
for pipe,(df,valcol,tf) in {'estoque':(est_d,'Estoque_mun_ano_final',np.log1p),
                            'ce_rie':(ss_d,'ce_rie',slog)}.items():
    M, pres = build(df, valcol, tf)
    elig = sorted([s for s in M if pres[s].sum()>=10])
    # ---- univariado sob 4 W ----
    labs = {}
    for sub in elig:
        for wn,w in Ws.items():
            ml = Moran_Local(M[sub], w, permutations=999, seed=42, n_jobs=-1)
            labs[(sub,wn)] = np.where(ml.p_sim<0.05, ml.q, 0)
    st = dict(tot=0, knn5=0, invdist=0, rede=0, tres=0, geo2=0)
    for sub in elig:
        lq = labs[(sub,'queen')]; m = lq!=0
        st['tot'] += int(m.sum())
        keep = {}
        for alt in ['knn5','invdist','rede']:
            keep[alt] = m & (labs[(sub,alt)]==lq)
            st[alt] += int(keep[alt].sum())
        st['geo2'] += int((keep['knn5']&keep['invdist']).sum())
        st['tres'] += int((keep['knn5']&keep['invdist']&keep['rede']).sum())
        detalhe_rows.append(dict(pipeline=pipe, subclasse=sub, n_sig_queen=int(m.sum()),
            mantidos_knn5=int(keep['knn5'].sum()), mantidos_invdist=int(keep['invdist'].sum()),
            mantidos_rede=int(keep['rede'].sum()),
            nucleo_robusto_3W=int((keep['knn5']&keep['invdist']&keep['rede']).sum())))
    resumo[(pipe,'uni')] = st
    print(f"[{pipe} uni] sigQ={st['tot']} | knn5={st['knn5']}({st['knn5']/st['tot']:.1%}) "
          f"| invdist={st['invdist']}({st['invdist']/st['tot']:.1%}) "
          f"| REDE={st['rede']}({st['rede']/st['tot']:.1%}) "
          f"| 2 geom.={st['geo2']}({st['geo2']/st['tot']:.1%}) | as 3 alt.={st['tres']}({st['tres']/st['tot']:.1%})")

    # ---- bivariado global sob 4 W (vetorizado, esquema esda validado) ----
    def z(v): return (v-v.mean())/v.std(ddof=1)
    pairs = [(a,b) for a in elig for b in M if b!=a and (pres[a]&pres[b]).sum()>=5]
    ZX = np.column_stack([z(M[a]) for a in elig]); fpos={a:i for i,a in enumerate(elig)}
    pbp={}
    for a,b in pairs: pbp.setdefault(b,[]).append(a)
    den=n-1.0
    rng = np.random.default_rng(42); P = np.array([rng.permutation(n) for _ in range(999)])
    rec={}
    for wn,w in Ws.items():
        U = w.sparse.T @ ZX
        for b,fs in pbp.items():
            zy=z(M[b]); G=zy[P]
            cols=np.array([fpos[a] for a in fs]); Ub=U[:,cols]
            obs=(Ub.T@zy)/den; sims=(G@Ub)/den
            larger=(sims>=obs[None,:]).sum(axis=0); larger=np.minimum(larger,999-larger)
            for a,o,q_ in zip(fs,obs,(larger+1)/1000.0): rec[(a,b,wn)]=(o,q_)
    sigq = [(a,b) for a,b in pairs if rec[(a,b,'queen')][1]<0.05]
    def kp(ab, alt):
        o,p = rec[(*ab,alt)]
        return p<0.05 and np.sign(o)==np.sign(rec[(*ab,'queen')][0])
    stb = dict(pares=len(pairs), sigq=len(sigq),
               knn5=sum(kp(ab,'knn5') for ab in sigq),
               invdist=sum(kp(ab,'invdist') for ab in sigq),
               rede=sum(kp(ab,'rede') for ab in sigq),
               geo2=sum(kp(ab,'knn5') and kp(ab,'invdist') for ab in sigq),
               tres=sum(kp(ab,'knn5') and kp(ab,'invdist') and kp(ab,'rede') for ab in sigq))
    resumo[(pipe,'biv')] = stb
    print(f"[{pipe} biv] pares={stb['pares']} sigQ={stb['sigq']} | knn5={stb['knn5']}({stb['knn5']/stb['sigq']:.1%}) "
          f"| invdist={stb['invdist']}({stb['invdist']/stb['sigq']:.1%}) | REDE={stb['rede']}({stb['rede']/stb['sigq']:.1%}) "
          f"| as 3={stb['tres']}({stb['tres']/stb['sigq']:.1%})")
    if pipe=='estoque':
        pd.to_pickle(dict(rec=rec, pairs=pairs, sigq=sigq, labs=labs, elig=elig), 'robustez/t1t2_4w_estoque.pkl')

pd.DataFrame(detalhe_rows).to_csv('/mnt/user-data/outputs/concordancia_T1T2_4matrizes.csv',
                                  sep=';', decimal=',', index=False, encoding='utf-8-sig')
with open('robustez/resumo_4w.pkl','wb') as f: pickle.dump(resumo, f)
print("ok")
