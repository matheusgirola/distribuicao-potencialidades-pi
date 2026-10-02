# -*- coding: utf-8 -*-
"""
21_painel_v7.py
---------------
Painel v7 a partir do v6: acrescenta tres escopos univariados com TODAS as
subclasses (qualquer tipologia) na aba Clusters Espaciais:

  todest   : Todos · Estoques        (robustez/todos_uni_estoque.pkl)
  todganho : Todos · Ganhos CE+RIE   (robustez/todos_uni_ce_rie_ganhos.pkl)
  todperda : Todos · Perdas CE+RIE   (robustez/todos_uni_ce_rie_perdas.pkl)

Ganhos e perdas sao separados porque, com CE+RIE de sinal misto, o ausente (0)
fica acima da media e vira falso Alto-Alto (ver script 20).

Entram as subclasses com I global significativo ou >= 3 nucleos Alto-Alto
robustos as 4 matrizes alternativas (coluna `entra_painel` do script 20).
Os mapas do v6 ficam intactos. Tambem: botao Bivariado desativado nos escopos
sem bivariado, seletor de escopo em grade e contagem de subclasses do
cabecalho calculada a partir de DB (antes era "622" fixo).

Depende de: saidas/painel_potencialidades_v6.html, robustez/todos_uni_*.pkl (20).
Produz: saidas/painel_potencialidades_v7.html
"""
import sys

import comum as C

sys.stdout.reconfigure(encoding='utf-8')

ENTRADA = C.SAIDAS / 'painel_potencialidades_v6.html'
SAIDA = C.SAIDAS / 'painel_potencialidades_v7.html'
ESCOPOS = {'todest': ('estoque', 'Estoque'),
           'todganho': ('ce_rie_ganhos', 'Ganhos de CE+RIE (Alto = ganho maior)'),
           'todperda': ('ce_rie_perdas', 'Perdas de CE+RIE (Alto = perda maior, em módulo)')}


def substituir(h, velho, novo):
    assert h.count(velho) == 1, f'trecho esperado 1 vez, achado {h.count(velho)}: {velho[:70]}'
    return h.replace(velho, novo)


def mapas_do_escopo(esc, pipe, prefixo, reorder):
    S = C.carregar_pickle(C.ROBUSTEZ / f'todos_uni_{pipe}.pkl')
    r = S['resumo']
    r = r[r['entra_painel']].sort_values('I', ascending=False)
    mapas = []
    for _, x in r.iterrows():
        s = x['subclasse']
        unidade = f" ({x['unidade']})" if pipe == 'estoque' else ''
        crit = ('I global signif.' if x['I_global_signif']
                else 'I global n.s. · hotspots locais robustos')
        subt = (f"{prefixo}{unidade} · I de Moran = {C.fbr(x['I'])} (p = {C.fbr(x['p_sim'])}) "
                f"· {x['AA']} núcleos Alto-Alto · {x['municipios_presentes']} municípios presentes "
                f"({x['presentes_em_T1T2']} em T1/T2) · {crit} · pós-FDR: {x['n_pos_FDR']} sig. "
                f"· robustos às 4 W alt. (incl. rede e tempo): {x['robustos_4W']}")
        mapas.append(dict(tipo='uni', esc=esc, rotulo=s, secao=x['secao'],
                          I=round(float(x['I']), 4), n_aa=int(x['AA']),
                          npres=int(x['municipios_presentes']), subt=subt,
                          cats=C.para_cats(S['labs'][(s, 'queen')], reorder)))
    return mapas


def main():
    base = C.carregar_base()
    h = ENTRADA.read_text(encoding='utf-8')
    L, ini, fim = C.ler_lisa_painel(h)
    reorder = C.reordenacao_painel(L, base['gdf_index'])
    antes = len(L['mapas'])
    assert not any(m.get('esc', 'tm1') in ESCOPOS for m in L['mapas']), \
        'o painel de entrada ja tem escopos "todos"'
    for esc, (pipe, prefixo) in ESCOPOS.items():
        novos = mapas_do_escopo(esc, pipe, prefixo, reorder)
        L['mapas'] += novos
        print(f'{esc}: {len(novos)} mapas univariados')
    h = C.gravar_lisa_painel(h, L, ini, fim)

    # --- seletor de escopo: T-1 e Todos·Estoques em linha cheia; pares lado a lado ---
    h = substituir(h,
        '<div class="seg"> <button class="on" data-esc="tm1">Emergentes (T-1)</button> '
        '<button data-esc="t1t2">T1+T2 · Estoques</button> '
        '<button data-esc="cerie">T1+T2 · CE+RIE</button> </div>',
        '<div class="seg seg-esc"> <button class="on" data-esc="tm1">Emergentes (T-1)</button> '
        '<button data-esc="t1t2">T1+T2 · Estoques</button> '
        '<button data-esc="cerie">T1+T2 · CE+RIE</button> '
        '<button data-esc="todest">Todos · Estoques</button> '
        '<button data-esc="todganho" title="Univariado de CE+RIE positivo">Todos · Ganhos CE+RIE</button> '
        '<button data-esc="todperda" title="Univariado de |CE+RIE| negativo">Todos · Perdas CE+RIE</button> </div>')
    h = substituir(h,
        '.seg button.on{background:var(--paper);color:var(--primary-ink);box-shadow:0 1px 3px rgba(0,0,0,.08)}',
        '.seg button.on{background:var(--paper);color:var(--primary-ink);box-shadow:0 1px 3px rgba(0,0,0,.08)}\n'
        '.seg.seg-esc{display:grid;grid-template-columns:1fr 1fr}\n'
        '.seg.seg-esc button[data-esc="tm1"],.seg.seg-esc button[data-esc="todest"]{grid-column:1 / -1}\n'
        '.seg button:disabled{opacity:.4;cursor:not-allowed}')

    # --- Bivariado desativado quando o escopo nao tem mapas bivariados ---
    h = substituir(h,
        "b.classList.add('on'); esc=b.dataset.esc;",
        "b.classList.add('on'); esc=b.dataset.esc;\n"
        "      const temBiv=LISA.mapas.some(m=>m.tipo==='biv'&&(m.esc||'tm1')===esc);\n"
        "      const bBiv=document.querySelector('.seg button[data-seg=\"biv\"]');\n"
        "      bBiv.disabled=!temBiv; bBiv.title=temBiv?'':'Bivariado não calculado para este escopo';\n"
        "      if(!temBiv&&seg==='biv'){seg='uni';document.querySelectorAll('.seg button[data-seg]')"
        ".forEach(x=>x.classList.toggle('on',x.dataset.seg==='uni'));}")

    # --- introducao ---
    h = substituir(h, 'em dois escopos:', 'em seis escopos:')
    h = substituir(h,
        'soma dos componentes CE e RIE do emprego formal RAIS).',
        'soma dos componentes CE e RIE do emprego formal RAIS). Os escopos <b>Todos</b> repetem a '
        'análise univariada para todas as subclasses, de qualquer tipologia (T1 a T8 e T-1), presentes '
        'em pelo menos 10 municípios: <b>Todos · Estoques</b> (estoque final) e, para o emprego formal, '
        '<b>Todos · Ganhos CE+RIE</b> (onde CE+RIE é positivo) e <b>Todos · Perdas CE+RIE</b> (onde é '
        'negativo, em módulo; Alto-Alto = aglomerado de perda competitiva). Ganhos e perdas são mapeados '
        'separadamente para que municípios sem o setor não apareçam como Alto. Entram as subclasses com I '
        'de Moran global significativo ou ao menos 3 núcleos Alto-Alto robustos às 4 matrizes '
        'alternativas. Nesses escopos o bivariado não foi calculado.')

    # --- cabecalho: contagem real de subclasses ---
    DB = C.ler_db_painel(h)[0]
    nsub = f"{len(DB['subclasses']):,}".replace(',', '.')
    h = substituir(h, '<div><b>224</b> municípios · <b>622</b> subclasses</div>',
                   f'<div><b>224</b> municípios · <b>{nsub}</b> subclasses</div>')

    # --- validacoes antes de gravar ---
    L6 = C.ler_lisa_painel(ENTRADA.read_text(encoding='utf-8'))[0]
    L7 = C.ler_lisa_painel(h)[0]
    assert L7['names'] == L6['names'] and L7['paths'] == L6['paths']
    assert L7['mapas'][:antes] == L6['mapas'], 'mapas do v6 alterados'
    assert all(len(m['cats']) == C.N_MUN for m in L7['mapas'])
    assert [C.norm(x) for x in DB['municipios']] == [C.norm(x) for x in L7['names']], \
        'DB.municipios fora da ordem de LISA.names'
    SAIDA.write_text(h, encoding='utf-8')
    print(f'v7: {SAIDA.stat().st_size / 1e6:.2f} MB | mapas: {len(L7["mapas"])} (v6: {antes}) '
          f'| subclasses no cabecalho: {nsub}')


if __name__ == '__main__':
    main()
