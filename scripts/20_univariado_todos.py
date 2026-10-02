# -*- coding: utf-8 -*-
"""
20_univariado_todos.py
----------------------
Moran global e LISA univariado para TODAS as subclasses, sem o recorte T1+T2,
em tres variaveis:

  estoque       : log1p(Estoque_mun_ano_final), todas as tipologias (T1...T8,
                  T-1). Presenca = estoque final > 0 (5.951 linhas do
                  consolidado tem estoque final 0: setores que desapareceram).
  ce_rie_ganhos : log1p(CE+RIE) onde CE+RIE > 0 (emprego formal RAIS).
  ce_rie_perdas : log1p(|CE+RIE|) onde CE+RIE < 0.

Por que ganhos e perdas separados: com todas as tipologias o CE+RIE tem os dois
sinais, e o ausente (valor 0) fica ACIMA da media sempre que o setor perde
competitividade na maior parte dos municipios -- 183 de 290 subclasses. Num
LISA sobre CE+RIE com sinal, 91,5% dos Alto-Alto eram municipios sem o setor.
Separando por sinal, o ausente volta a ser o minimo e Alto-Alto passa a
significar aglomerado de ganho (ou de perda) competitivo. Cada par
(municipio, subclasse) tem um unico CE+RIE -- o maior entre os tres anos-base,
convencao dos escopos T1+T2 -- e cai em exatamente uma das duas variaveis.

Para cada subclasse com >= MIN_UNI municipios presentes: I global (999 perm.,
pseudo p com semente), LISA sob as 5 matrizes (999 perm., seed 42), LISA Queen
a 9.999 perm. com FDR (Benjamini-Hochberg) e robustez as 4 matrizes
alternativas. Entra no painel quem tem I global significativo ou pelo menos
MIN_AA_HOTSPOT nucleos Alto-Alto robustos as 4 matrizes alternativas. So
univariado: o bivariado de todas as subclasses fica de fora por custo (ordem
de 10^5 pares).

Depende de: robustez/base.pkl (00), rede.pkl (08), tempo.pkl (00b).
Produz:
  robustez/todos_uni_<variavel>.pkl            estado completo (painel v7)
  saidas/todos_moran_global_<variavel>.csv       uma linha por subclasse
  saidas/todos_lisa_municipios_<variavel>.csv    municipios significativos
"""
import pickle
import sys
import time
import warnings

import numpy as np
import pandas as pd
from esda import fdr

import comum as C
from cnae_map import SECOES, secao as secao_cnae

warnings.filterwarnings('ignore', category=DeprecationWarning)

VARIAVEIS = ('estoque', 'ce_rie_ganhos', 'ce_rie_perdas')
sys.stdout.reconfigure(encoding='utf-8')


def rotulo_secao(fonte, sub):
    if fonte in ('PAM', 'PEVS', 'PPM'):
        return f'IBGE/{fonte}'
    sec = secao_cnae(sub)
    return 'MTE/RAIS' if sec == 'Z' else SECOES[sec]


def preparar(pipe):
    """Retorna (df deduplicado, coluna de valor, transformacao, metadados, tipologias)."""
    if pipe == 'estoque':
        bruto = C.ler_estoque(tipos=None)
        bruto = bruto[bruto['Estoque_mun_ano_final'] > 0]
        valcol, tf = 'Estoque_mun_ano_final', np.log1p
        uni_fu = bruto.groupby('subclasse')[['Fonte', 'Unidade_de_medida']].nunique()
        assert (uni_fu == 1).all().all(), 'subclasse com mais de uma fonte/unidade'
        meta = bruto.drop_duplicates('subclasse').set_index('subclasse')[['Fonte', 'Unidade_de_medida']]
        meta.columns = ['fonte', 'unidade']
        ded = C.deduplicar(bruto, valcol)
    else:
        bruto = C.ler_shiftshare(tipos=None)
        ded = C.deduplicar(bruto, 'ce_rie')          # um CE+RIE por par, antes de separar o sinal
        if pipe == 'ce_rie_ganhos':
            ded = ded[ded['ce_rie'] > 0].copy()
            ded['valor'], unidade = ded['ce_rie'], 'CE+RIE positivo (empregos)'
        else:
            ded = ded[ded['ce_rie'] < 0].copy()
            ded['valor'], unidade = -ded['ce_rie'], '|CE+RIE| negativo (empregos)'
        valcol, tf = 'valor', np.log1p
        meta = pd.DataFrame({'fonte': 'RAIS', 'unidade': unidade},
                            index=sorted(bruto['subclasse'].unique()))
    # tipologias observadas por (municipio, subclasse) nos tres anos-base
    tip = (bruto.groupby(['subclasse', 'mun_norm'])['classificacao_regiao']
           .agg(lambda x: ','.join(sorted(set(x)))))
    return ded, valcol, tf, meta, tip


def rodar(pipe, base, ws, disp):
    t0 = time.time()
    idx = base['gdf_index']
    df, valcol, tf, meta, tip = preparar(pipe)
    M, pres = C.montar_matriz(df, valcol, tf, idx)
    bruto, _ = C.montar_matriz(df, valcol, lambda v: v, idx)
    elig = C.elegiveis(pres)
    print(f'[{pipe}] subclasses: {len(M)} | elegiveis (>= {C.MIN_UNI} municipios): {len(elig)}')

    wq = ws['queen']
    uni, labs, fdr_lab, linhas, locais = {}, {}, {}, [], []
    for s in elig:
        y = M[s]
        mg = C.moran_global(y, wq)
        for wn, w in ws.items():
            labs[(s, wn)], ml = C.lisa_rotulos(y, w)
            if wn == 'queen':
                ml_q = ml
        _, ml9 = C.lisa_rotulos(y, wq, permutations=C.PERM_FDR)
        corte = fdr(ml9.p_sim, C.PVAL)
        fdr_lab[s] = np.where(ml9.p_sim <= corte, ml9.q, 0)

        lab = labs[(s, 'queen')]
        sig = lab != 0
        rob = sig.copy()
        for alt in C.ALTS:
            rob &= labs[(s, alt)] == lab
        tips = [tip.get((s, m), '') for m in idx]
        t12 = np.array([any(t in C.TIPOS_T1T2 for t in x.split(',')) for x in tips])
        n = {q: int((lab == q).sum()) for q in (1, 2, 3, 4)}
        uni[s] = dict(I=float(mg.I), EI=float(mg.EI), pI=float(mg.p_sim), z=float(mg.z_sim))
        # entra no painel: I global signif. OU >= 3 nucleos AA robustos as 4 W alt.
        # (AA nominal e ruidoso: ~5% de 224 municipios dao significancia por acaso)
        aa_rob = int((rob & (lab == 1)).sum())
        entra = (mg.p_sim < C.PVAL) or (aa_rob >= C.MIN_AA_HOTSPOT)
        linhas.append(dict(
            subclasse=s, fonte=meta.loc[s, 'fonte'], unidade=meta.loc[s, 'unidade'],
            secao=rotulo_secao(meta.loc[s, 'fonte'], s),
            municipios_presentes=int(pres[s].sum()),
            presentes_em_T1T2=int((pres[s] & t12).sum()),
            I=round(float(mg.I), 4), E_I=round(float(mg.EI), 4),
            p_sim=round(float(mg.p_sim), 4), z_sim=round(float(mg.z_sim), 3),
            I_global_signif=bool(mg.p_sim < C.PVAL),
            AA=n[1], AB=n[4], BA=n[2], BB=n[3], n_sig=int(sig.sum()),
            n_pos_FDR=int((fdr_lab[s] != 0).sum()), AA_pos_FDR=int((fdr_lab[s] == 1).sum()),
            corte_FDR=float(corte),
            robustos_4W=int(rob.sum()), AA_robustos_4W=int((rob & (lab == 1)).sum()),
            entra_painel=bool(entra),
            criterio_painel=('I global signif.' if mg.p_sim < C.PVAL
                             else ('hotspots locais' if entra else ''))))
        for i in np.where(sig)[0]:
            locais.append(dict(
                subclasse=s, secao=linhas[-1]['secao'], municipio=disp[idx[i]],
                quadrante=C.QUAD_PT[lab[i]], p_sim=round(float(ml_q.p_sim[i]), 4),
                presente=bool(pres[s][i]), valor=round(float(bruto[s][i]), 4),
                tipologias=tips[i], sig_pos_FDR=bool(fdr_lab[s][i] == lab[i]),
                robusto_4W=bool(rob[i])))

    glob_df = pd.DataFrame(linhas).sort_values('I', ascending=False)
    loc_df = pd.DataFrame(locais)
    glob_df.to_csv(C.SAIDAS / f'todos_moran_global_{pipe}.csv', **C.CSV_OUT)
    loc_df.to_csv(C.SAIDAS / f'todos_lisa_municipios_{pipe}.csv', **C.CSV_OUT)
    with open(C.ROBUSTEZ / f'todos_uni_{pipe}.pkl', 'wb') as f:
        pickle.dump(dict(M=M, bruto=bruto, pres=pres, elig=elig, uni=uni, labs=labs,
                         fdr_lab=fdr_lab, resumo=glob_df), f)

    sigq = int(glob_df['n_sig'].sum())
    print(f'[{pipe}] I global signif.: {int(glob_df.I_global_signif.sum())} | '
          f'entram no painel: {int(glob_df.entra_painel.sum())} '
          f'(so por hotspots: {int((glob_df.criterio_painel == "hotspots locais").sum())})')
    print(f'[{pipe}] LISA sig. Queen: {sigq} municipios-subclasse | pos-FDR: '
          f'{int(glob_df.n_pos_FDR.sum())} | robustos as 4 W: {int(glob_df.robustos_4W.sum())} '
          f'({glob_df.robustos_4W.sum() / max(sigq, 1):.1%}) | {time.time() - t0:.0f} s')


def main():
    base = C.carregar_base()
    ws = C.carregar_ws(base)
    disp = C.nomes_exibicao(base)
    for pipe in VARIAVEIS:
        rodar(pipe, base, ws, disp)


if __name__ == '__main__':
    main()
