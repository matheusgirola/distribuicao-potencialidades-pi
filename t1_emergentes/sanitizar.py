import pandas as pd, numpy as np, json
from cnae_map import secao, SECOES

import os as _os
AQUI = _os.path.dirname(_os.path.abspath(__file__)).replace(chr(92), '/')   # t1_emergentes/
RAIZ = _os.path.dirname(AQUI)
OUT = AQUI + '/tabelas'
df = pd.read_csv(RAIZ + '/dados/potencialidades_consolidado_v2.csv', sep=';', encoding='utf-8-sig')
df.columns = ['subclasse','cls','NM_MUN','estoque','unidade','fonte','ai','af']

# mapa código desativado -> sucessor(es) plausível(is)
SUC = {
 'Lojas de departamentos ou magazines (Desativado)': ['Lojas de departamentos ou magazines, exceto lojas francas (Duty free)'],
 'Comércio a varejo de peças e acessórios para motocicletas e motonetas (Desativado)': [
     'Comércio a varejo de peças e acessórios novos para motocicletas e motonetas',
     'Comércio a varejo de peças e acessórios usados para motocicletas e motonetas'],
 'Bares e outros estabelecimentos especializados em servir bebidas (Desativado)': [
     'Bares e outros estabelecimentos especializados em servir bebidas, sem entretenimento',
     'Bares e outros estabelecimentos especializados em servir bebidas, com entretenimento'],
 'Serrarias com desdobramento de madeira (Desativado)': ['Serrarias com desdobramento de madeira em bruto'],
 'Serrarias sem desdobramento de madeira (Desativado)': ['Serrarias sem desdobramento de madeira em bruto Resserragem'],
 'Atividades de organizações associativas profissionais (Desativado)': ['Outras atividades associativas profissionais'],
 'Atividades auxiliares dos transportes aquaviários não especificadas anteriormente(Desativado)': [
     'Atividades auxiliares dos transportes aquaviários não especificadas anteriormente'],
 'Desenvolvimento de programas de computador sob encomenda (Desativado)': ['Desenvolvimento de programas de computador sob encomenda'],
 'Atividades de monitoramento de sistemas de segurança (Desativado)': ['Atividades de monitoramento de sistemas de segurança eletronico'],
 'Edição de jornais (Desativado)': ['Edição de jornais diarios','Edição de jornais nao diarios'],
 'Edição integrada à impressão de jornais (Desativado)': ['Edição integrada à impressão de jornais diarios'],
 'Fabricação de adubos e fertilizantes (Desativado)': ['Fabricação de adubos e fertilizantes, exceto organominerais','Fabricação de adubos e fertilizantes organominerais'],
 'Padaria e confeitaria com predominância de produção própria (Desativado)': ['Fabricação de produtos de padaria e confeitaria com predominância de produção própria'],
}
# município x código antigo presente na base (qualquer classificação)
antigo = {}
for old in SUC:
    antigo[old] = set(df[df.subclasse == old].NM_MUN)

t1 = pd.read_csv(f'{OUT}/t1_pares_com_cnae.csv', sep=';', decimal=',')
t1['flag'] = 'Emergência efetiva (candidata)'
t1.loc[t1.subclasse.str.contains(r'\(Desativado\)', regex=True), 'flag'] = 'Artefato: código CNAE desativado'
for old, news in SUC.items():
    m = antigo[old]
    sel = t1.subclasse.isin(news) & t1.NM_MUN.isin(m) & (t1.flag == 'Emergência efetiva (candidata)')
    t1.loc[sel, 'flag'] = 'Artefato: migração de código CNAE'
t1.loc[(t1.fonte == 'PPM') & (t1.subclasse == 'Codornas'), 'flag'] = 'Artefato: quebra de série (PPM Codornas)'

rais = t1[t1.fonte == 'RAIS']
print(rais.groupby('flag').agg(pares=('estoque','size'), vinculos=('estoque','sum'), mun=('NM_MUN','nunique')).to_string())
print()
lim = rais[rais.flag == 'Emergência efetiva (candidata)']
sig = lim[lim.estoque >= 10]
print('RAIS limpa:', len(lim), 'pares |', int(lim.estoque.sum()), 'vínculos')
print('>=10 limpa:', len(sig), 'pares |', int(sig.estoque.sum()), 'vínculos |', sig.NM_MUN.nunique(), 'mun |', sig.subclasse.nunique(), 'subclasses')
merc = sig[~sig.secao_nome.str.startswith('O')]
print('>=10 mercado:', len(merc), int(merc.estoque.sum()), merc.NM_MUN.nunique(), merc.subclasse.nunique())

sub = sig.groupby(['subclasse','secao_nome']).agg(mun=('NM_MUN','nunique'), vinc=('estoque','sum'),
        med=('estoque','median'), max_=('estoque','max')).reset_index().sort_values('vinc', ascending=False)
sub.to_csv(f'{OUT}/tab_subclasses_sig_limpa.csv', index=False, sep=';', decimal=',')
print(); print(sub.head(22).to_string())

subm = merc.groupby(['subclasse','secao_nome']).agg(mun=('NM_MUN','nunique'), vinc=('estoque','sum'),
        med=('estoque','median'), max_=('estoque','max')).reset_index().sort_values('vinc', ascending=False)
subm.to_csv(f'{OUT}/tab_subclasses_mercado.csv', index=False, sep=';', decimal=',')
print(); print('=== TOP MERCADO ==='); print(subm.head(20).to_string())

munt = sig.groupby('NM_MUN').agg(setores=('subclasse','nunique'), vinc=('estoque','sum')).sort_values('vinc', ascending=False)
munt.to_csv(f'{OUT}/tab_municipios_sig_limpa.csv', sep=';', decimal=',')
print(); print(munt.head(15).to_string())

t1.to_csv(f'{OUT}/t1_pares_final.csv', index=False, sep=';', decimal=',')
sec = lim.groupby('secao_nome').agg(pares=('estoque','size'), vinc=('estoque','sum'), mun=('NM_MUN','nunique')).sort_values('vinc', ascending=False)
sec.to_csv(f'{OUT}/tab_secao_limpa.csv', sep=';', decimal=',')
print(); print(sec.to_string())
