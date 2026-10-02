# -*- coding: utf-8 -*-
"""
23_painel_ciet_v8.py
--------------------
Painel publicado no GitHub Pages (estetica CIET) atualizado para o v8.

A base `saidas/painel_ciet_base_v6.html` e o index.html publicado no
commit ef51b7d deste repositorio: os mesmos dados do v6
(DB e LISA identicos), com paleta e logo do CIET, filtro "Periodo de destaque"
e estoque final no tooltip do mapa. Esta etapa preserva tudo isso e aplica as
mudancas dos scripts 21 e 22:

  - LISA do v8 (2.022 mapas do v6 + 239 dos escopos todest/todganho/todperda);
  - seletor de escopo em grade com os tres escopos "Todos";
  - botao Bivariado desativado nos escopos sem bivariado;
  - texto de introducao e contagem de subclasses do cabecalho;
  - abertura na aba Clusters Espaciais, escopo "Todos · Estoques".

Depende de: saidas/painel_ciet_base_v6.html, saidas/painel_potencialidades_v8.html (22).
Produz: index.html (raiz do repositorio, publicado pelo GitHub Pages)
"""
import sys

import comum as C

sys.stdout.reconfigure(encoding='utf-8')

BASE = C.SAIDAS / 'painel_ciet_base_v6.html'
V6 = C.SAIDAS / 'painel_potencialidades_v6.html'
V8 = C.SAIDAS / 'painel_potencialidades_v8.html'
SAIDA = C.INDEX_PAGES
ESC_INICIAL = 'todest'


def substituir(h, velho, novo):
    assert h.count(velho) == 1, f'trecho esperado 1 vez, achado {h.count(velho)}: {velho[:70]}'
    return h.replace(velho, novo)


def main():
    hb = BASE.read_text(encoding='utf-8')
    h8 = V8.read_text(encoding='utf-8')

    # --- dados: a base tem de ter exatamente os dados do v6 ---
    Lb, ini, fim = C.ler_lisa_painel(hb)
    L6 = C.ler_lisa_painel(V6.read_text(encoding='utf-8'))[0]
    L8 = C.ler_lisa_painel(h8)[0]
    DB = C.ler_db_painel(hb)[0]
    assert Lb == L6, 'LISA da base CIET difere do v6'
    assert DB == C.ler_db_painel(h8)[0], 'DB da base CIET difere do v8'
    assert L8['mapas'][:len(L6['mapas'])] == L6['mapas']
    h = C.gravar_lisa_painel(hb, L8, ini, fim)

    # --- seletor de escopo (na base CIET o escopo marcado era T1+T2) ---
    h = substituir(h,
        '<div class="seg"> <button data-esc="tm1">Emergentes (T-1)</button> '
        '<button class="on" data-esc="t1t2">T1+T2 · Estoques</button> '
        '<button data-esc="cerie">T1+T2 · CE+RIE</button> </div>',
        '<div class="seg seg-esc"> <button data-esc="tm1">Emergentes (T-1)</button> '
        '<button data-esc="t1t2">T1+T2 · Estoques</button> '
        '<button data-esc="cerie">T1+T2 · CE+RIE</button> '
        '<button class="on" data-esc="todest">Todos · Estoques</button> '
        '<button data-esc="todganho" title="Univariado de CE+RIE positivo">Todos · Ganhos CE+RIE</button> '
        '<button data-esc="todperda" title="Univariado de |CE+RIE| negativo">Todos · Perdas CE+RIE</button> </div>')
    h = substituir(h,
        '.seg button.on{background:var(--paper);color:var(--primary-ink);box-shadow:0 1px 3px rgba(0,0,0,.08)}',
        '.seg button.on{background:var(--paper);color:var(--primary-ink);box-shadow:0 1px 3px rgba(0,0,0,.08)}\n'
        '.seg.seg-esc{display:grid;grid-template-columns:1fr 1fr}\n'
        '.seg.seg-esc button[data-esc="tm1"],.seg.seg-esc button[data-esc="todest"]{grid-column:1 / -1}\n'
        '.seg button:disabled{opacity:.4;cursor:not-allowed}')
    h = substituir(h, "let seg='uni', esc='t1t2', sel=null;",
                   f"let seg='uni', esc='{ESC_INICIAL}', sel=null;")

    # --- Bivariado desativado quando o escopo nao tem mapas bivariados ---
    h = substituir(h,
        "b.classList.add('on'); esc=b.dataset.esc;",
        "b.classList.add('on'); esc=b.dataset.esc;\n"
        "      const temBiv=LISA.mapas.some(m=>m.tipo==='biv'&&(m.esc||'tm1')===esc);\n"
        "      const bBiv=document.querySelector('.seg button[data-seg=\"biv\"]');\n"
        "      bBiv.disabled=!temBiv; bBiv.title=temBiv?'':'Bivariado não calculado para este escopo';\n"
        "      if(!temBiv&&seg==='biv'){seg='uni';document.querySelectorAll('.seg button[data-seg]')"
        ".forEach(x=>x.classList.toggle('on',x.dataset.seg==='uni'));}")
    h = substituir(h,
        "    document.getElementById('lisa-q').addEventListener('input',render);\n",
        "    document.getElementById('lisa-q').addEventListener('input',render);\n"
        "    if(!LISA.mapas.some(m=>m.tipo==='biv'&&(m.esc||'tm1')===esc)){\n"
        "      const bBiv=document.querySelector('.seg button[data-seg=\"biv\"]');\n"
        "      bBiv.disabled=true; bBiv.title='Bivariado não calculado para este escopo';}\n")

    # --- aba inicial: Clusters Espaciais ---
    h = substituir(h, '<button class="tab active" data-view="shiftshare">',
                   '<button class="tab" data-view="shiftshare">')
    h = substituir(h, '<button class="tab" data-view="clusters">',
                   '<button class="tab active" data-view="clusters">')
    h = substituir(h, '<div class="view active" id="view-shiftshare">',
                   '<div class="view" id="view-shiftshare">')
    h = substituir(h, '<div class="view" id="view-clusters">',
                   '<div class="view active" id="view-clusters">')
    h = substituir(h,
        "    sel=LISA.mapas.indexOf(first); render(); drawMap(first);\n  }\n})();",
        "    sel=LISA.mapas.indexOf(first); render(); drawMap(first);\n  }\n"
        "  if(document.querySelector('.tab.active').dataset.view==='clusters'"
        "&&!window.__lisaInit){window.__lisaInit=1;initLisa();}\n})();")

    # --- introducao (mesmo texto do v7) ---
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
    nsub = f"{len(DB['subclasses']):,}".replace(',', '.')
    h = substituir(h, '<div><b>224</b> municípios · <b>622</b> subclasses</div>',
                   f'<div><b>224</b> municípios · <b>{nsub}</b> subclasses</div>')

    # --- validacoes antes de gravar ---
    Ls = C.ler_lisa_painel(h)[0]
    assert Ls == L8, 'LISA diferente do v8'
    assert C.ler_db_painel(h)[0] == DB, 'DB alterado'
    assert [C.norm(x) for x in DB['municipios']] == [C.norm(x) for x in Ls['names']]
    # o tooltip de estoque da base CIET procura o rotulo em DB.subclasses
    subs = set(DB['subclasses'])
    falta = [m['rotulo'] for m in Ls['mapas'] if m['tipo'] == 'uni' and m['rotulo'] not in subs]
    assert not falta, f'rotulos fora de DB.subclasses: {falta[:3]}'
    for marca in ('brand-logo', 'f-periodo', 'stockIndex', '--azul-royal'):
        assert marca in h, f'customizacao CIET perdida: {marca}'
    SAIDA.write_text(h, encoding='utf-8')
    print(f'CIET v8: {SAIDA.stat().st_size / 1e6:.2f} MB | mapas: {len(Ls["mapas"])} '
          f'| subclasses: {nsub} | abre em Clusters, escopo {ESC_INICIAL}')


if __name__ == '__main__':
    main()
