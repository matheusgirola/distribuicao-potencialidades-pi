import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import json, os

import os as _os
AQUI = _os.path.dirname(_os.path.abspath(__file__)).replace(chr(92), '/')   # t1_emergentes/
RAIZ = _os.path.dirname(AQUI)
OUT = AQUI + '/tabelas'
FIG = AQUI + '/figuras'
os.makedirs(FIG, exist_ok=True)

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 10,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'grid.alpha': .25, 'grid.linestyle': '-',
    'axes.axisbelow': True, 'figure.dpi': 150, 'savefig.dpi': 150,
    'savefig.bbox': 'tight', 'axes.titleweight': 'bold', 'axes.titlesize': 12,
})
BR = lambda x, p=None: f'{x:,.0f}'.replace(',', '.')
FMT = FuncFormatter(BR)

AZ = '#1f4e79'; LA = '#5b9bd5'; VD = '#2e7d32'; LR = '#c62828'; CZ = '#9e9e9e'; AM = '#ef8a1f'

d = pd.read_csv(f'{OUT}/t1_pares_com_cnae.csv', sep=';', decimal=',')
rais = d[d.fonte == 'RAIS'].copy()
def faixa(v):
    if v == 0: return 'Estoque 0'
    if v < 5: return '1 a 4'
    if v < 10: return '5 a 9'
    if v < 50: return '10 a 49'
    return '50 ou +'
rais['faixa'] = rais.estoque.map(faixa)
ORD = ['Estoque 0', '1 a 4', '5 a 9', '10 a 49', '50 ou +']
CORES = {'Estoque 0': CZ, '1 a 4': '#bdd7ee', '5 a 9': LA, '10 a 49': AZ, '50 ou +': '#0d2f4b'}

# ---------- Fig 1: faixas -- pares vs vínculos ----------
g = rais.groupby('faixa').agg(pares=('estoque', 'size'), vinculos=('estoque', 'sum')).reindex(ORD)
fig, axs = plt.subplots(1, 2, figsize=(11, 4.4))
for ax, col, tit, cor in zip(axs, ['pares', 'vinculos'],
                             ['Nº de pares município–subclasse', 'Vínculos empregatícios (estoque 2025)'],
                             [LA, AZ]):
    b = ax.bar(g.index, g[col], color=[CORES[i] for i in g.index], edgecolor='white')
    tot = g[col].sum()
    for r, v in zip(b, g[col]):
        ax.text(r.get_x() + r.get_width()/2, v, f'{BR(v)}\n({100*v/tot:.1f}%)'.replace('.', ','),
                ha='center', va='bottom', fontsize=8.5)
    ax.set_title(tit); ax.yaxis.set_major_formatter(FMT)
    ax.set_ylim(0, g[col].max()*1.28); ax.set_xlabel('Faixa de estoque (vínculos)')
fig.suptitle('Figura 1 — Potencialidades T-1 na RAIS: o paradoxo da massa e do peso',
             fontsize=13, fontweight='bold', y=1.03)
fig.text(0.5, -0.05, 'Fonte: elaboração própria a partir de potencialidades_consolidado.csv (RAIS, 6.011 pares emergentes).',
         ha='center', fontsize=8, color='#555')
fig.savefig(f'{FIG}/fig1_faixas.png'); plt.close(fig)

# ---------- Fig 2: composição das faixas por seção ----------
piv = pd.crosstab(rais.secao_nome, rais.faixa).reindex(columns=ORD).fillna(0)
piv['tot'] = piv.sum(1)
piv = piv.sort_values('tot')
pc = piv[ORD].div(piv.tot, axis=0)*100
fig, ax = plt.subplots(figsize=(11, 7))
left = np.zeros(len(pc))
for c in ORD:
    ax.barh(pc.index, pc[c], left=left, color=CORES[c], label=c, edgecolor='white', height=.78)
    left += pc[c].values
for i, (idx, t) in enumerate(zip(piv.index, piv.tot)):
    ax.text(101, i, f'n={BR(t)}', va='center', fontsize=8.5, color='#444')
ax.set_xlim(0, 112); ax.set_xlabel('% dos pares emergentes da seção')
ax.legend(ncol=5, loc='lower center', bbox_to_anchor=(.5, -.13), frameon=False, title='Faixa de estoque')
ax.set_title('Figura 2 — Composição por faixa de tamanho, segundo seção CNAE 2.0\n(seções ordenadas pelo nº de pares emergentes)')
ax.grid(axis='y', visible=False)
fig.text(0.5, -0.09, 'Leitura: seções à esquerda com predomínio de azul-claro são dominadas por emergências de 1 a 4 vínculos (baixa robustez).',
         ha='center', fontsize=8, color='#555')
fig.savefig(f'{FIG}/fig2_secao_faixa.png'); plt.close(fig)

# ---------- Fig 3: top subclasses >= 10 ----------
sig = rais[rais.estoque >= 10]
sub = sig.groupby(['subclasse', 'secao_nome']).estoque.sum().reset_index().sort_values('estoque', ascending=False).head(20)
sub['sec'] = sub.secao_nome.str[0]
pal = {'O': LR, 'G': AZ, 'Q': VD, 'P': AM, 'J': LA, 'N': '#7e57c2', 'F': '#8d6e63', 'C': '#00838f',
       'D': '#c0a000', 'I': '#ad1457', 'A': '#558b2f', 'H': '#455a64', 'M': '#6d4c41', 'S': CZ,
       'E': '#26a69a', 'B': '#795548', 'R': '#ec407a', 'K': '#5d4037', 'L': '#9e9d24'}
lab = lambda s: (s[:66] + '…') if len(s) > 66 else s
fig, ax = plt.subplots(figsize=(11.5, 7.5))
sub = sub.iloc[::-1]
ax.barh([lab(s) for s in sub.subclasse], sub.estoque, color=[pal[s] for s in sub.sec], height=.75)
for i, v in enumerate(sub.estoque):
    ax.text(v + 60, i, BR(v), va='center', fontsize=8.5)
ax.set_xlabel('Vínculos emergentes (soma do estoque, ano final)')
ax.xaxis.set_major_formatter(FMT); ax.grid(axis='y', visible=False)
ax.set_title('Figura 3 — As 20 subclasses emergentes mais relevantes (faixa ≥ 10 vínculos)')
h = [plt.Rectangle((0, 0), 1, 1, color=pal[s]) for s in ['O', 'G', 'Q', 'P', 'J', 'N', 'F', 'D', 'C', 'I', 'A']]
ax.legend(h, ['O–Adm. pública', 'G–Comércio', 'Q–Saúde', 'P–Educação', 'J–Info/Com.', 'N–Adm./serviços',
              'F–Construção', 'D–Energia', 'C–Indústria', 'I–Aloj./alim.', 'A–Agropecuária'],
          ncol=4, loc='lower right', fontsize=8, frameon=True, framealpha=.9)
fig.text(0.5, -0.03, 'Atenção: as barras da seção O (e parte de P/Q) refletem majoritariamente reclassificação de CNAE de entes públicos, não nova base econômica.',
         ha='center', fontsize=8, color=LR)
fig.savefig(f'{FIG}/fig3_top_subclasses.png'); plt.close(fig)

# ---------- Fig 4: top municípios, mercado vs administração pública ----------
sig2 = sig.copy()
sig2['grupo'] = np.where(sig2.secao_nome.str.startswith('O'), 'Administração pública (seção O)', 'Atividades de mercado')
m = sig2.pivot_table(index='NM_MUN', columns='grupo', values='estoque', aggfunc='sum').fillna(0)
m['tot'] = m.sum(1)
m = m.sort_values('tot', ascending=False).head(20).iloc[::-1]
fig, ax = plt.subplots(figsize=(10.5, 7))
ax.barh(m.index, m['Atividades de mercado'], color=AZ, label='Atividades de mercado', height=.75)
ax.barh(m.index, m.get('Administração pública (seção O)', 0), left=m['Atividades de mercado'],
        color=LR, label='Administração pública (seção O)', height=.75)
for i, v in enumerate(m.tot):
    ax.text(v + 60, i, BR(v), va='center', fontsize=8.5)
ax.set_xlabel('Vínculos emergentes (faixa ≥ 10)')
ax.xaxis.set_major_formatter(FMT); ax.grid(axis='y', visible=False)
ax.legend(frameon=False, loc='lower right')
ax.set_title('Figura 4 — 20 municípios com maior emprego emergente robusto (≥ 10 vínculos)')
fig.savefig(f'{FIG}/fig4_top_municipios.png'); plt.close(fig)

# ---------- Fig 5: coortes por fonte ----------
c = pd.crosstab(d.fonte, d.coorte)
c = c[sorted(c.columns)]
cores = [VD, AM, LA, CZ]
fig, ax = plt.subplots(figsize=(10, 4.2))
left = np.zeros(len(c))
for col, cor in zip(c.columns, cores):
    ax.barh(c.index, c[col], left=left, color=cor, label=col, height=.7)
    left += c[col].values
ax.set_xlabel('Nº de pares município–subclasse classificados como T-1')
ax.xaxis.set_major_formatter(FMT); ax.grid(axis='y', visible=False)
ax.legend(fontsize=8, loc='center left', bbox_to_anchor=(1.01, .5), frameon=False)
ax.set_title('Figura 5 — Coorte de emergência: em que janela o setor apareceu')
fig.savefig(f'{FIG}/fig5_coortes.png'); plt.close(fig)

# ---------- Fig 6: faixa A agregada por seção ----------
pa = rais[rais.estoque < 5].groupby('secao_nome').agg(pares=('estoque', 'size'), mun=('NM_MUN', 'nunique')).sort_values('pares')
fig, ax = plt.subplots(figsize=(10.5, 6.5))
ax.barh(pa.index, pa.pares, color='#bdd7ee', edgecolor=LA, height=.75)
for i, (v, mm) in enumerate(zip(pa.pares, pa.mun)):
    ax.text(v + 12, i, f'{BR(v)}  ({mm} mun.)', va='center', fontsize=8.5)
ax.set_xlabel('Nº de pares emergentes com 1 a 4 vínculos')
ax.set_xlim(0, pa.pares.max()*1.25); ax.xaxis.set_major_formatter(FMT); ax.grid(axis='y', visible=False)
ax.set_title('Figura 6 — Emergências de baixa magnitude (1 a 4 vínculos) agregadas por seção CNAE\n"Onde o tecido produtivo está apenas ensaiando"')
fig.savefig(f'{FIG}/fig6_faixaA_secao.png'); plt.close(fig)

# ---------- Fig 7: fontes IBGE ----------
ib = d[d.fonte != 'RAIS']
pam = ib[ib.fonte == 'PAM'].groupby('subclasse').agg(v=('estoque', 'sum'), m=('NM_MUN', 'nunique')).sort_values('v').tail(12)
pevs = ib[ib.fonte == 'PEVS'].groupby('subclasse').agg(v=('estoque', 'sum'), m=('NM_MUN', 'nunique')).sort_values('v').tail(10)
aq = ib[(ib.fonte == 'PPM') & (ib.unidade == 'mil reais')].groupby('subclasse').agg(v=('estoque', 'sum'), m=('NM_MUN', 'nunique')).sort_values('v').tail(10)
fig, axs = plt.subplots(1, 3, figsize=(15, 5))
for ax, dfx, tit, cor in zip(axs, [pam, aq, pevs],
                             ['PAM — lavouras emergentes', 'PPM — pecuária/aquicultura emergente', 'PEVS — extrativismo emergente'], [VD, LA, '#8d6e63']):
    ax.barh(dfx.index, dfx.v, color=cor, height=.72)
    for i, (v, mm) in enumerate(zip(dfx.v, dfx.m)):
        ax.text(v + dfx.v.max()*.02, i, f'{BR(v)} ({mm})', va='center', fontsize=8)
    ax.set_title(tit, fontsize=11); ax.set_xlabel('Valor da produção (R$ mil)')
    ax.set_xlim(0, dfx.v.max()*1.4); ax.xaxis.set_major_formatter(FMT); ax.grid(axis='y', visible=False)
fig.suptitle('Figura 7 — Potencialidades T-1 nas fontes IBGE (valor da produção; entre parênteses, nº de municípios)',
             fontsize=13, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(f'{FIG}/fig7_ibge.png'); plt.close(fig)

# ---------- Fig 8: dispersão municipal ----------
mun = rais.groupby('NM_MUN').agg(setores=('subclasse', 'nunique'), vinc=('estoque', 'sum')).reset_index()
mun['sig'] = mun.NM_MUN.map(sig.groupby('NM_MUN').subclasse.nunique()).fillna(0)
fig, ax = plt.subplots(figsize=(9.5, 6))
sc = ax.scatter(mun.setores, mun.vinc.clip(lower=1), c=mun.sig, cmap='viridis', s=34, alpha=.85, edgecolor='white', lw=.4)
ax.set_yscale('log'); ax.set_xscale('log')
ax.set_xlabel('Nº de subclasses emergentes (escala log)')
ax.set_ylabel('Vínculos emergentes totais (escala log)')
plt.colorbar(sc, label='Subclasses emergentes com ≥ 10 vínculos')
for _, r in mun.sort_values('vinc', ascending=False).head(9).iterrows():
    ax.annotate(r.NM_MUN, (r.setores, max(r.vinc, 1)), fontsize=8, xytext=(4, 4), textcoords='offset points')
ax.set_title('Figura 8 — Amplitude x profundidade da emergência setorial (224 municípios)')
fig.text(0.5, -0.02, 'Muitos municípios acumulam dezenas de setores novos que somam pouquíssimos vínculos: diversificação nominal sem densidade.',
         ha='center', fontsize=8, color='#555')
fig.savefig(f'{FIG}/fig8_dispersao.png'); plt.close(fig)

print('ok', os.listdir(FIG))
