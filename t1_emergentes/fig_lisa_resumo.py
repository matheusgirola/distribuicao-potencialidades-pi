import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os as _os
AQUI = _os.path.dirname(_os.path.abspath(__file__)).replace(chr(92), '/')   # t1_emergentes/
RAIZ = _os.path.dirname(AQUI)
OUT=AQUI + '/out_lisa'; FIG=f'{OUT}/mapas'
plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,
 'figure.dpi':150,'savefig.dpi':150,'savefig.bbox':'tight','axes.grid':True,'grid.alpha':.25})
AZ='#1f4e79'; VD='#2e7d32'; LR='#c0392b'

gl=pd.read_csv(f'{OUT}/moran_global_univariado.csv',sep=';',decimal=',')
sig=gl[gl.p_sim<0.05].copy()

fig,axs=plt.subplots(1,2,figsize=(13,5.6))
# painel A: I global das subclasses significativas (top 18)
top=sig.sort_values('I',ascending=False).head(18).iloc[::-1]
lab=lambda s:(s[:46]+'…') if len(s)>46 else s
cor=['#2e7d32' if 'IBGE' in str(x) or x.startswith('A') else AZ for x in top.secao]
axs[0].barh([lab(s) for s in top.subclasse], top.I, color=cor, height=.74)
axs[0].set_xlabel("I de Moran global (log1p da intensidade)")
axs[0].set_title('A) Autocorrelação espacial por subclasse emergente\n(52 de 177 com I significativo, p<0,05)', fontsize=11, fontweight='bold')
axs[0].axvline(0, color='#888', lw=.6)
from matplotlib.patches import Patch
axs[0].legend(handles=[Patch(color=VD,label='Agropecuária / IBGE'),Patch(color=AZ,label='Demais setores (RAIS)')],
              fontsize=8, loc='lower right', frameon=True)

# painel B: municípios-hub (recorrência em Alto-Alto)
l=pd.read_csv(f'{OUT}/lisa_univariado_clusters.csv',sep=';',decimal=',')
aa=l[l.quadrante=='Alto-Alto'].NM_MUN.value_counts().head(14).iloc[::-1]
axs[1].barh(aa.index, aa.values, color=LR, height=.74)
for i,v in enumerate(aa.values): axs[1].text(v+.15,i,str(v),va='center',fontsize=9)
axs[1].set_xlabel('Nº de subclasses em que o município é núcleo Alto-Alto')
axs[1].set_title('B) Municípios-núcleo da emergência\n(hubs recorrentes de clusters Alto-Alto)', fontsize=11, fontweight='bold')
axs[1].grid(axis='y',visible=False)
fig.suptitle('Figura 10 — Análise LISA univariada das potencialidades T-1 (base depurada, malha IBGE 224 municípios)',
             fontsize=13, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(f'{FIG}/fig10_lisa_resumo.png', facecolor='white'); plt.close(fig)
print('ok')
