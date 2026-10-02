# -*- coding: utf-8 -*-
"""
22_painel_v8.py
---------------
Painel v8 a partir do v7: muda so a abertura. O painel passa a abrir na aba
Clusters Espaciais (LISA), com o escopo "Todos · Estoques" selecionado (antes
abria em Resultados Shift-Share e, no LISA, em Emergentes T-1). Dados e mapas
ficam identicos aos do v7.

Depende de: saidas/painel_potencialidades_v7.html (21).
Produz: saidas/painel_potencialidades_v8.html
"""
import sys

import comum as C

sys.stdout.reconfigure(encoding='utf-8')

ENTRADA = C.SAIDAS / 'painel_potencialidades_v7.html'
SAIDA = C.SAIDAS / 'painel_potencialidades_v8.html'
ESC_INICIAL = 'todest'


def substituir(h, velho, novo):
    assert h.count(velho) == 1, f'trecho esperado 1 vez, achado {h.count(velho)}: {velho[:70]}'
    return h.replace(velho, novo)


def main():
    h7 = ENTRADA.read_text(encoding='utf-8')
    h = h7

    # --- aba inicial: Clusters Espaciais ---
    h = substituir(h, '<button class="tab active" data-view="shiftshare">',
                   '<button class="tab" data-view="shiftshare">')
    h = substituir(h, '<button class="tab" data-view="clusters">',
                   '<button class="tab active" data-view="clusters">')
    h = substituir(h, '<div class="view active" id="view-shiftshare">',
                   '<div class="view" id="view-shiftshare">')
    h = substituir(h, '<div class="view" id="view-clusters">',
                   '<div class="view active" id="view-clusters">')
    # o LISA so era iniciado no clique da aba; inicia ao carregar se ela ja vem ativa
    h = substituir(h,
        "    sel=LISA.mapas.indexOf(first); render(); drawMap(first);\n  }\n})();",
        "    sel=LISA.mapas.indexOf(first); render(); drawMap(first);\n  }\n"
        "  if(document.querySelector('.tab.active').dataset.view==='clusters'"
        "&&!window.__lisaInit){window.__lisaInit=1;initLisa();}\n})();")

    # --- escopo inicial: Todos · Estoques ---
    h = substituir(h, "let seg='uni', esc='tm1', sel=null;",
                   f"let seg='uni', esc='{ESC_INICIAL}', sel=null;")
    h = substituir(h, '<button class="on" data-esc="tm1">', '<button data-esc="tm1">')
    h = substituir(h, f'<button data-esc="{ESC_INICIAL}">', f'<button class="on" data-esc="{ESC_INICIAL}">')
    # o escopo inicial nao tem bivariado: desativa o botao ja na abertura
    h = substituir(h,
        "    document.getElementById('lisa-q').addEventListener('input',render);\n",
        "    document.getElementById('lisa-q').addEventListener('input',render);\n"
        "    if(!LISA.mapas.some(m=>m.tipo==='biv'&&(m.esc||'tm1')===esc)){\n"
        "      const bBiv=document.querySelector('.seg button[data-seg=\"biv\"]');\n"
        "      bBiv.disabled=true; bBiv.title='Bivariado não calculado para este escopo';}\n")

    # --- validacoes antes de gravar ---
    L7 = C.ler_lisa_painel(h7)[0]
    L8 = C.ler_lisa_painel(h)[0]
    assert L8 == L7, 'dados do LISA alterados'
    assert C.ler_db_painel(h)[0] == C.ler_db_painel(h7)[0], 'DB alterado'
    assert any(m['tipo'] == 'uni' and m.get('esc') == ESC_INICIAL for m in L8['mapas'])
    SAIDA.write_text(h, encoding='utf-8')
    print(f'v8: {SAIDA.stat().st_size / 1e6:.2f} MB | mapas: {len(L8["mapas"])} '
          f'| abre em Clusters, escopo {ESC_INICIAL}')


if __name__ == '__main__':
    main()
