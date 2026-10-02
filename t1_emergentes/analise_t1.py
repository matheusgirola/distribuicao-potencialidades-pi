import pandas as pd, numpy as np, json, os
from cnae_map import secao, SECOES

import os as _os
AQUI = _os.path.dirname(_os.path.abspath(__file__)).replace(chr(92), '/')   # t1_emergentes/
RAIZ = _os.path.dirname(AQUI)
OUT = AQUI + '/tabelas'
os.makedirs(OUT, exist_ok=True)

df = pd.read_csv(RAIZ + '/dados/potencialidades_consolidado_v2.csv', sep=';', encoding='utf-8-sig')
df.columns = ['subclasse','classificacao_regiao','NM_MUN','estoque','unidade','fonte','ano_inicial','ano_final']

t = df[df.classificacao_regiao == 'T-1'].copy()
key = ['NM_MUN','subclasse','fonte']

# ---- coorte de emergência: em quais janelas T0 o par foi classificado como T-1 ----
jan = t.groupby(key)['ano_inicial'].apply(lambda s: tuple(sorted(s.unique()))).rename('janelas')
t1 = t.drop_duplicates(key + ['estoque','unidade']).merge(jan.reset_index(), on=key)
assert t1.duplicated(key).sum() == 0

def coorte(j):
    if 2022 in j and 2018 in j and 2013 in j: return '1. Emergência recente (ausente até 2022)'
    if 2022 in j: return '2. Reemergência/intermitente (ausente em 2022, presente antes)'
    if 2018 in j: return '3. Emergência 2019-2022 (presente em 2022)'
    return '4. Emergência 2014-2018 (presente desde ~2018)'

t1['coorte'] = t1.janelas.map(coorte)
t1['recente_2022'] = t1.janelas.map(lambda j: 2022 in j)
t1['secao'] = t1.subclasse.map(secao)
t1['secao_nome'] = t1.secao.map(SECOES)

# ---- estratos RAIS ----
def faixa(v):
    if v == 0: return '0 - Sem vínculo ativo (estoque = 0)'
    if v < 5: return 'A - 1 a 4 vínculos'
    if v < 10: return 'B - 5 a 9 vínculos'
    if v < 50: return 'C - 10 a 49 vínculos'
    return 'D - 50 ou mais vínculos'

rais = t1[t1.fonte == 'RAIS'].copy()
rais['faixa'] = rais.estoque.map(faixa)
rais['faixa_agg'] = np.where(rais.estoque >= 10, 'C+D - 10 ou mais', rais.faixa)

ibge = t1[t1.fonte != 'RAIS'].copy()

rep = {}
rep['universo'] = dict(
    pares_totais=len(t1), municipios=t1.NM_MUN.nunique(), subclasses=t1.subclasse.nunique(),
    por_fonte=t1.fonte.value_counts().to_dict(),
    coorte=t1.coorte.value_counts().to_dict(),
    coorte_rais=rais.coorte.value_counts().to_dict(),
)

# ---- RAIS: estratos ----
fx = rais.groupby('faixa').agg(pares=('estoque','size'), vinculos=('estoque','sum'),
                               municipios=('NM_MUN','nunique'), subclasses=('subclasse','nunique'),
                               mediana=('estoque','median')).reset_index()
fx['pct_pares'] = 100*fx.pares/fx.pares.sum()
fx['pct_vinculos'] = 100*fx.vinculos/fx.vinculos.sum()
rep['rais_faixas'] = fx.to_dict('records')
rep['rais_total_vinculos'] = int(rais.estoque.sum())
fx.to_csv(f'{OUT}/tab_faixas_rais.csv', index=False, sep=';', decimal=',')

# ---- RAIS: seção CNAE x faixa ----
piv = pd.crosstab(rais.secao_nome, rais.faixa)
piv.to_csv(f'{OUT}/tab_secao_x_faixa.csv', sep=';')

sec = rais.groupby('secao_nome').agg(pares=('estoque','size'), vinculos=('estoque','sum'),
                                     municipios=('NM_MUN','nunique'), subclasses=('subclasse','nunique')).reset_index()
sec['vinc_por_par'] = (sec.vinculos/sec.pares).round(1)
sec = sec.sort_values('vinculos', ascending=False)
sec.to_csv(f'{OUT}/tab_secao_rais.csv', index=False, sep=';', decimal=',')
rep['rais_secao'] = sec.to_dict('records')

# seções nas faixas pequenas (A e 0) - onde a agregação CNAE é a leitura útil
peq = rais[rais.estoque < 5]
sec_peq = peq.groupby('secao_nome').agg(pares=('estoque','size'), vinculos=('estoque','sum'),
                                        municipios=('NM_MUN','nunique')).sort_values('pares', ascending=False)
sec_peq.to_csv(f'{OUT}/tab_secao_faixaA.csv', sep=';', decimal=',')
rep['rais_secao_faixaA'] = sec_peq.reset_index().to_dict('records')

sec_med = rais[(rais.estoque>=5)&(rais.estoque<10)].groupby('secao_nome').agg(
    pares=('estoque','size'), vinculos=('estoque','sum'), municipios=('NM_MUN','nunique')).sort_values('pares', ascending=False)
sec_med.to_csv(f'{OUT}/tab_secao_faixaB.csv', sep=';', decimal=',')
rep['rais_secao_faixaB'] = sec_med.reset_index().to_dict('records')

# ---- Faixa >= 10: detalhamento ----
sig = rais[rais.estoque >= 10].copy()
rep['sig'] = dict(pares=len(sig), vinculos=int(sig.estoque.sum()), municipios=int(sig.NM_MUN.nunique()),
                  subclasses=int(sig.subclasse.nunique()),
                  pct_vinculos=round(100*sig.estoque.sum()/rais.estoque.sum(),1))

sub_sig = sig.groupby(['subclasse','secao_nome']).agg(
    municipios=('NM_MUN','nunique'), vinculos=('estoque','sum'), mediana=('estoque','median'),
    maior=('estoque','max')).reset_index().sort_values('vinculos', ascending=False)
sub_sig.to_csv(f'{OUT}/tab_subclasses_sig.csv', index=False, sep=';', decimal=',')
rep['sig_top_subclasses'] = sub_sig.head(25).to_dict('records')

mun_sig = sig.groupby('NM_MUN').agg(setores=('subclasse','nunique'), vinculos=('estoque','sum'),
                                    maior=('estoque','max')).reset_index().sort_values('vinculos', ascending=False)
mun_sig.to_csv(f'{OUT}/tab_municipios_sig.csv', index=False, sep=';', decimal=',')
rep['sig_top_municipios'] = mun_sig.head(25).to_dict('records')

pares_top = sig.sort_values('estoque', ascending=False).head(30)[['NM_MUN','subclasse','secao_nome','estoque','coorte']]
pares_top.to_csv(f'{OUT}/tab_pares_top.csv', index=False, sep=';', decimal=',')
rep['sig_top_pares'] = pares_top.to_dict('records')

# municípios: visão geral RAIS
mun_all = rais.groupby('NM_MUN').agg(setores=('subclasse','nunique'), vinculos=('estoque','sum')).reset_index()
mun_all['setores_sig'] = mun_all.NM_MUN.map(sig.groupby('NM_MUN').subclasse.nunique()).fillna(0).astype(int)
mun_all['pct_sig'] = (100*mun_all.setores_sig/mun_all.setores).round(1)
mun_all = mun_all.sort_values('setores', ascending=False)
mun_all.to_csv(f'{OUT}/tab_municipios_rais.csv', index=False, sep=';', decimal=',')
rep['mun_top_setores'] = mun_all.head(20).to_dict('records')
rep['mun_stats'] = dict(mediana_setores=float(mun_all.setores.median()),
                        media_setores=round(float(mun_all.setores.mean()),1),
                        municipios_sem_sig=int((mun_all.setores_sig==0).sum()))

# ---- Fontes IBGE ----
ib = ibge.groupby(['fonte','unidade']).agg(pares=('estoque','size'), municipios=('NM_MUN','nunique'),
                                           subclasses=('subclasse','nunique'), total=('estoque','sum')).reset_index()
rep['ibge_resumo'] = ib.to_dict('records')

for f in ['PPM','PAM','PEVS']:
    s = ibge[ibge.fonte==f]
    g = s.groupby('subclasse').agg(municipios=('NM_MUN','nunique'), total=('estoque','sum'),
                                   mediana=('estoque','median'), maior=('estoque','max')).reset_index().sort_values('total', ascending=False)
    g.to_csv(f'{OUT}/tab_{f.lower()}.csv', index=False, sep=';', decimal=',')
    rep[f'ibge_{f}'] = g.to_dict('records')
    tp = s.sort_values('estoque', ascending=False).head(12)[['NM_MUN','subclasse','estoque','unidade','coorte']]
    rep[f'ibge_{f}_top'] = tp.to_dict('records')

# quartis de magnitude para fontes IBGE (dentro de cada subclasse)
ibge['q'] = ibge.groupby('subclasse').estoque.transform(lambda s: s.rank(pct=True))
rep['ibge_alta_magnitude'] = ibge[(ibge.q>=0.9)].sort_values('estoque', ascending=False).head(20)[
    ['NM_MUN','subclasse','estoque','unidade','fonte']].to_dict('records')

t1.to_csv(f'{OUT}/t1_pares_com_cnae.csv', index=False, sep=';', decimal=',')
json.dump(rep, open(f'{OUT}/resumo.json','w'), ensure_ascii=False, indent=1, default=str)
print(json.dumps({k:v for k,v in rep.items() if k in ['universo','rais_total_vinculos','sig','mun_stats','ibge_resumo']}, ensure_ascii=False, indent=1, default=str))
print(fx)
