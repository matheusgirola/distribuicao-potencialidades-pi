# -*- coding: utf-8 -*-
"""Concordancia T1+T2 sob CINCO matrizes: Queen (base), KNN-5, dist. inversa,
rede rodoviaria (malha oficial) e TEMPO DE VIAGEM (ORS). Estoque (v2) e CE+RIE."""

import pickle, numpy as np, pandas as pd, warnings, unicodedata, re
from esda.moran import Moran_Local
import comum as C
from comum import norm

warnings.filterwarnings('ignore')


# Carrega todas as matrizes de vizinhança
base = C.carregar_base()

# pos, dicionario em ordem alfabetica com o nome do municipio e com um indice
idx = base['gdf_index']; n=len(idx); pos={m:i for i,m in enumerate(idx)}
# função de transformação log sinalizada
slog = C.slog
# dicionário com as matrizes de vizinhaça
# As matrizes de vizinhança já vêm normalizadas por linha
Ws = C.carregar_ws(base)

ALTS = ['knn5','invdist','rede','tempo']

# Carregar dados de estoque
est_d = C.deduplicar(C.ler_estoque(), 'Estoque_mun_ano_final')

# Carregar dados de CI+RIE
ss_d = C.deduplicar(C.ler_shiftshare(), 'ce_rie')

def build(df, valcol, tf):
    # TO-DO: ajeitar essa descrição horrivel
    '''
    df -> pandas dataframe
    valcol -> nome da coluna
    tf -> função que transforma

    Retorna dois dicionarios onde em ambos as chaves são as subclasses e os itens são numpy arrays de dimensão n=224. Cada index
    é uma posição desse array repesenta um dos municipios do piaui, conforme o dicionario pos

    No dicionário M, a posição no array é um float que mostra o valor da produção da subclasse dentro do município
    No dicionário p, a posição no array é um bool que mostra se a produção existe ou não no município
    '''
    # utiliza as variaveis globais n=len(idx); pos={m:i for i,m in enumerate(idx)}
    # definida na linha 19
    M, pres = {}, {}
    for sub,g in df.groupby('subclasse'):
        v=np.zeros(n); ii=[pos[m] for m in g['mun_norm']]
        v[ii]=tf(g[valcol].values); M[sub]=v
        p=np.zeros(n,bool); p[ii]=True; pres[sub]=p
    return M, pres

saida = {}
det = []

# Loop pra construir os indice para os dois tipos de dados: estoque e ce+rie
for pipe,(df,valcol,tf) in {'estoque':(est_d,'Estoque_mun_ano_final',np.log1p),
                            'ce_rie':(ss_d,'ce_rie',slog)}.items():
    M, pres = build(df, valcol, tf)

     #------ Moran Local sob 10 W
    # Filtra pras subclasses presentes em ao menos 10 municipios
    elig = sorted([s for s in M if pres[s].sum()>=10])
    print(f'Número de subclasses elegiveis I de Moran Local para o pipeline {pipe}: {len(elig)}')

    # Para cada subclasse e o método, salvamos em labs o quadrante a qual pertence o Moran Local do municipio: 
    # 1 HH, 2 LH, 3 LL, 4 HL se for significativo, e não for recebe 0
    labs = {}
    for sub in elig:
        for wn,w in Ws.items():
            labs[(sub,wn)], _ = C.lisa_rotulos(M[sub], w)

    # Para cada subclasse, mostra em quantas matrizes de vizinhança o resultado se manteve robusto (ml.q !=0 na matriz)
    st = {k:0 for k in ['tot']+ALTS+['quatro','geo2']}
    for sub in elig:
        lq = labs[(sub,'queen')]; m = lq!=0
        st['tot'] += int(m.sum())
        keep = {alt: m & (labs[(sub,alt)]==lq) for alt in ALTS}
        for alt in ALTS: st[alt] += int(keep[alt].sum())
        st['geo2'] += int((keep['knn5']&keep['invdist']).sum())
        q4 = keep['knn5']&keep['invdist']&keep['rede']&keep['tempo']
        st['quatro'] += int(q4.sum())
        det.append(dict(pipeline=pipe, subclasse=sub, n_sig_queen=int(m.sum()),
                        **{f'mantidos_{a}':int(keep[a].sum()) for a in ALTS},
                        nucleo_robusto_4W=int(q4.sum())))
        
    saida[(pipe,'uni')] = st

    print(f"[{pipe} uni] sigQ={st['tot']} | " +
          " | ".join(f"{a}={st[a]}({st[a]/st['tot']:.1%})" for a in ALTS) +
          f" | as 4 alt.={st['quatro']}({st['quatro']/st['tot']:.1%})")

    #------ bivariado global vetorizado sob 5 W
    def z(v): return (v-v.mean())/v.std(ddof=1)

    # Filtra para os pares de subclasses presentes em ao menos 5 municipios
    # Note que utilizamos para a as subclasses eligiveis pro Moran Local, mas não para b
    pairs = [(a,b) for a in elig for b in M if b!=a and (pres[a]&pres[b]).sum()>=5]
    print(f'Número de subclasses elegiveis bivariado global para o pipeline {pipe}: {len(pairs)}')
    # Matriz com os valores normalizados de TODAS as subclasses elegiveis
    ZX = np.column_stack([z(M[a]) for a in elig]); fpos={a:i for i,a in enumerate(elig)}
    
    pbp={}
    # Criamos um dicionario, onde as chaves são cada uma das subclasses e seus itens a lista de subclasses
    # que elas fazem pares
    for a,b in pairs: pbp.setdefault(b,[]).append(a)

    # A normalização foi com n-1, agora os moran locais tbm são normalizados por n-1
    den=n-1.0

    # Criar um array cujos elementos são 999 arrays com numeros de 0 a 223 permutados
    rng = np.random.default_rng(42); 
    P = np.array([rng.permutation(n) for _ in range(999)])
    rec={}

    for wn,w in Ws.items():
        U = w.sparse.T @ ZX # Wz

        # Para cada subclasse e a lista de  subclasse que tem pares
        for b,fs in pbp.items():
            # Normalizamos a subclasse e permutamos os indices
            zy=z(M[b]); G=zy[P]
            # Selecionamos em U = Wz as colunas com que a subclasse tem pares
            cols=np.array([fpos[a] for a in fs]); Ub=U[:,cols]
            
            obs=(Ub.T@zy)/den; sims=(G@Ub)/den
            larger=(sims>=obs[None,:]).sum(axis=0); larger=np.minimum(larger,999-larger)

            for a,o,q_ in zip(fs,obs,(larger+1)/1000.0): rec[(a,b,wn)]=(o,q_)

    sigq = [(a,b) for a,b in pairs if rec[(a,b,'queen')][1]<0.05]

    # kp só é chamada nesta mesma iteração, então usa o rec certo
    def kp(ab, alt):
        o,p = rec[(*ab,alt)]  # noqa: B023
        return p<0.05 and np.sign(o)==np.sign(rec[(*ab,'queen')][0])  # noqa: B023

    stb = {'pares':len(pairs), 'sigq':len(sigq)}
    for alt in ALTS: stb[alt] = sum(kp(ab,alt) for ab in sigq)
    stb['quatro'] = sum(all(kp(ab,alt) for alt in ALTS) for ab in sigq)
    saida[(pipe,'biv')] = stb
    print(f"[{pipe} biv] pares={stb['pares']} sigQ={stb['sigq']} | " +
          " | ".join(f"{a}={stb[a]}({stb[a]/stb['sigq']:.1%})" for a in ALTS) +
          f" | as 4={stb['quatro']}({stb['quatro']/stb['sigq']:.1%})")
    if pipe=='estoque':
        pd.to_pickle(dict(rec=rec, pairs=pairs, sigq=sigq, labs=labs, elig=elig, M=M, pres=pres),
                     C.ROBUSTEZ / 't1t2_5w_estoque.pkl')

pd.DataFrame(det).to_csv(C.SAIDAS / 'concordancia_T1T2_5matrizes.csv', **C.CSV_OUT)
with open(C.ROBUSTEZ / 'resumo_5w.pkl','wb') as f: pickle.dump(saida, f)
print("ok")
