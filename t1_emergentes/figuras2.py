import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import os as _os
AQUI = _os.path.dirname(_os.path.abspath(__file__)).replace(chr(92), '/')   # t1_emergentes/
RAIZ = _os.path.dirname(AQUI)
OUT = AQUI + '/tabelas'; FIG = AQUI + '/figuras'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,
 'axes.grid':True,'grid.alpha':.25,'axes.axisbelow':True,'figure.dpi':150,'savefig.dpi':150,
 'savefig.bbox':'tight','axes.titleweight':'bold','axes.titlesize':12})
BR = lambda x,p=None: f'{x:,.0f}'.replace(',','.')
FMT = FuncFormatter(BR)
AZ='#1f4e79'; LA='#5b9bd5'; VD='#2e7d32'; LR='#c62828'; CZ='#9e9e9e'; AM='#ef8a1f'

d = pd.read_csv(f'{OUT}/t1_pares_final.csv', sep=';', decimal=',')
rais = d[d.fonte=='RAIS']
lim = rais[rais.flag=='Emergência efetiva (candidata)']
sig = lim[lim.estoque>=10]

pal = {'O':LR,'G':AZ,'Q':VD,'P':AM,'J':LA,'N':'#7e57c2','F':'#8d6e63','C':'#00838f','D':'#c0a000',
       'I':'#ad1457','A':'#558b2f','H':'#455a64','M':'#6d4c41','S':CZ,'E':'#26a69a','B':'#795548',
       'R':'#ec407a','K':'#5d4037','L':'#9e9d24'}
lab = lambda s: (s[:64]+'…') if len(s)>64 else s

# Fig 3 (depurada)
sub = sig.groupby(['subclasse','secao_nome']).estoque.sum().reset_index().sort_values('estoque',ascending=False).head(20)
sub['sec']=sub.secao_nome.str[0]; sub=sub.iloc[::-1]
fig,ax=plt.subplots(figsize=(11.5,7.5))
ax.barh([lab(s) for s in sub.subclasse], sub.estoque, color=[pal[s] for s in sub.sec], height=.75)
for i,v in enumerate(sub.estoque): ax.text(v+60,i,BR(v),va='center',fontsize=8.5)
ax.set_xlabel('Vínculos emergentes (soma do estoque no ano final)')
ax.xaxis.set_major_formatter(FMT); ax.grid(axis='y',visible=False)
ax.set_title('Figura 3 — As 20 subclasses emergentes mais relevantes (≥ 10 vínculos), após depuração')
h=[plt.Rectangle((0,0),1,1,color=pal[s]) for s in ['O','Q','P','J','N','G','F','D','C','A','M']]
ax.legend(h,['O–Adm. pública','Q–Saúde','P–Educação','J–Info./Com.','N–Adm./serviços','G–Comércio',
             'F–Construção','D–Energia','C–Indústria','A–Agropecuária','M–Prof./técnicas'],
          ncol=4,loc='lower right',fontsize=8,framealpha=.92)
fig.text(0.5,-0.03,'As barras vermelhas (seção O) e parte de P/Q correspondem a reclassificação de CNAE de entes públicos — leia-as com reserva.',
         ha='center',fontsize=8,color=LR)
fig.savefig(f'{FIG}/fig3_top_subclasses.png'); plt.close(fig)

# Fig 4 (depurada)
s2=sig.copy(); s2['g']=np.where(s2.secao_nome.str.startswith('O'),'pub','merc')
m=s2.pivot_table(index='NM_MUN',columns='g',values='estoque',aggfunc='sum').fillna(0)
m['tot']=m.sum(axis=1); m=m.sort_values('tot',ascending=False).head(20).iloc[::-1]
fig,ax=plt.subplots(figsize=(10.5,7))
ax.barh(m.index,m['merc'],color=AZ,label='Atividades de mercado',height=.75)
ax.barh(m.index,m.get('pub',0),left=m['merc'],color=LR,label='Administração pública (seção O)',height=.75)
for i,v in enumerate(m.tot): ax.text(v+50,i,BR(v),va='center',fontsize=8.5)
ax.set_xlabel('Vínculos emergentes (≥ 10), após depuração')
ax.xaxis.set_major_formatter(FMT); ax.grid(axis='y',visible=False); ax.legend(frameon=False,loc='lower right')
ax.set_title('Figura 4 — 20 municípios com maior emprego emergente robusto')
fig.savefig(f'{FIG}/fig4_top_municipios.png'); plt.close(fig)

# Fig 9 — funil de depuração
etapas = ['Pares T-1\nna RAIS','(–) código CNAE\ndesativado','(–) migração de\ncódigo CNAE','Emergências\ncandidatas',
          'Com ≥ 10\nvínculos','De mercado\n(exclui seção O)']
vals = [6011, 6011-188, 6011-188-150, 5673, 1131, 1079]
cores = [CZ,'#e8a0a0','#e8a0a0',LA,AZ,VD]
fig,ax=plt.subplots(figsize=(11,4.8))
b=ax.bar(etapas,vals,color=cores,edgecolor='white')
for r,v in zip(b,vals): ax.text(r.get_x()+r.get_width()/2,v+80,BR(v),ha='center',fontsize=9.5,fontweight='bold')
vinc=[76688,76688,70079,70079,57420,45229]
ax2=ax.twinx(); ax2.plot(etapas,vinc,color=LR,marker='o',lw=2,label='Vínculos'); ax2.grid(False)
ax2.set_ylabel('Vínculos empregatícios',color=LR); ax2.tick_params(axis='y',colors=LR)
ax2.yaxis.set_major_formatter(FMT); ax2.set_ylim(0,max(vinc)*1.15)
for x,v in zip(etapas,vinc): ax2.text(x,v+2600,BR(v),ha='center',fontsize=8,color=LR)
ax.set_ylabel('Nº de pares município–subclasse'); ax.yaxis.set_major_formatter(FMT); ax.set_ylim(0,7400)
ax.set_title('Figura 9 — Funil de depuração das potencialidades T-1 (RAIS)')
fig.savefig(f'{FIG}/fig9_funil.png'); plt.close(fig)
print('ok')
