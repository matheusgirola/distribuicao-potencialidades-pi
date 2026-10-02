# -*- coding: utf-8 -*-
"""Regressao do pipeline contra os resultados ja publicados.

Confere que o modulo `comum` (leitura, deduplicacao, matriz, LISA) reproduz
exatamente o que esta gravado em robustez/t1t2_5w_estoque.pkl e nos mapas do
painel v6. Rode com `uv run pytest` depois de qualquer refatoracao ou troca
de versao de pacote.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import comum as C  # noqa: E402

PKL_5W = C.ROBUSTEZ / 't1t2_5w_estoque.pkl'
PAINEL_V6 = C.SAIDAS / 'painel_potencialidades_v6.html'

# Dois mapas CE+RIE do v6 nao se reproduzem com o CSV local de shift-share
# (p recalculado 0,12-0,49 onde o painel marca significancia): foram gerados
# com uma versao ligeiramente diferente do consolidado. Ver CONTEXTO_PROJETO.md.
CERIE_V6_NAO_REPRODUZ = {
    'Comércio varejista de artigos do vestuário e acessórios',
    'Padaria e confeitaria com predominância de revenda',
}


@pytest.fixture(scope='module')
def base():
    return C.carregar_base()


@pytest.fixture(scope='module')
def ws(base):
    return C.carregar_ws(base)


@pytest.fixture(scope='module')
def t5():
    if not PKL_5W.exists():
        pytest.skip(f'{PKL_5W.name} ausente')
    return pd.read_pickle(PKL_5W)


@pytest.fixture(scope='module')
def lisa_v6():
    if not PAINEL_V6.exists():
        pytest.skip(f'{PAINEL_V6.name} ausente')
    return C.ler_lisa_painel(PAINEL_V6.read_text(encoding='utf-8'))[0]


def test_versao_esda():
    """As permutacoes do LISA mudam entre versoes do esda (2.8.1 x 2.10.0 divergem
    em ~9% dos municipios na margem de p = 0,05). O painel publicado e da 2.10.0."""
    import esda
    assert esda.__version__ == '2.10.0'


def test_base_ordem_canonica(base):
    idx = base['gdf_index']
    assert len(idx) == C.N_MUN == len(set(idx))
    assert idx == sorted(idx)
    for nome in ('w_queen', 'w_knn5', 'w_inv'):
        assert base[nome].n == C.N_MUN and not base[nome].islands


def test_matriz_estoque_t1t2_igual_ao_pickle(base, t5):
    est = C.deduplicar(C.ler_estoque(), 'Estoque_mun_ano_final')
    M, pres = C.montar_matriz(est, 'Estoque_mun_ano_final', np.log1p, base['gdf_index'])
    assert C.elegiveis(pres) == t5['elig']
    assert set(M) == set(t5['M'])
    for s in M:
        np.testing.assert_array_equal(M[s], t5['M'][s])
        np.testing.assert_array_equal(pres[s], t5['pres'][s])


def test_lisa_5w_igual_ao_pickle(t5, ws):
    """Todos os LISA (5 matrizes x subclasses elegiveis) com seed 42."""
    diverg = []
    for s in t5['elig']:
        for wn, w in ws.items():
            lab, _ = C.lisa_rotulos(t5['M'][s], w)
            if not np.array_equal(lab, t5['labs'][(s, wn)]):
                diverg.append((s, wn, int((lab != t5['labs'][(s, wn)]).sum())))
    assert not diverg, f'{len(diverg)} LISA divergentes: {diverg[:5]}'


def test_painel_v6_t1t2_uni(base, t5, ws, lisa_v6):
    """Recalcula (nao le do pickle) e compara com os mapas publicados."""
    reorder = C.reordenacao_painel(lisa_v6, base['gdf_index'])
    mapas = [m for m in lisa_v6['mapas'] if m.get('esc') == 't1t2' and m['tipo'] == 'uni']
    assert len(mapas) == 54
    for m in mapas:
        lab, _ = C.lisa_rotulos(t5['M'][m['rotulo']], ws['queen'])
        assert m['cats'] == C.para_cats(lab, reorder), m['rotulo']


def test_painel_v6_cerie_uni(base, ws, lisa_v6):
    ss = C.deduplicar(C.ler_shiftshare(), 'ce_rie')
    M, pres = C.montar_matriz(ss, 'ce_rie', C.slog, base['gdf_index'])
    reorder = C.reordenacao_painel(lisa_v6, base['gdf_index'])
    mapas = [m for m in lisa_v6['mapas'] if m.get('esc') == 'cerie' and m['tipo'] == 'uni']
    assert len(mapas) == 28
    for m in mapas:
        s = m['rotulo']
        lab, _ = C.lisa_rotulos(M[s], ws['queen'])
        assert m['npres'] == int(pres[s].sum())
        assert m['n_aa'] == int((lab == 1).sum())
        if s in CERIE_V6_NAO_REPRODUZ:
            continue
        assert m['cats'] == C.para_cats(lab, reorder), s


def test_moran_global_reprodutivel(t5, ws):
    s = t5['elig'][0]
    a = C.moran_global(t5['M'][s], ws['queen'])
    b = C.moran_global(t5['M'][s], ws['queen'])
    assert a.I == b.I and a.p_sim == b.p_sim


# ------------------------------------------------ escopos "todos" (20 e 21)
PAINEL_V7 = C.SAIDAS / 'painel_potencialidades_v7.html'
PAINEL_V8 = C.SAIDAS / 'painel_potencialidades_v8.html'
PAINEL_CIET = C.INDEX_PAGES


@pytest.fixture(scope='module')
def todos():
    arqs = {p: C.ROBUSTEZ / f'todos_uni_{p}.pkl' for p in ('estoque', 'ce_rie_ganhos', 'ce_rie_perdas')}
    if not all(a.exists() for a in arqs.values()):
        pytest.skip('rode scripts/20_univariado_todos.py')
    return {p: C.carregar_pickle(a) for p, a in arqs.items()}


def test_todos_contem_t1t2_como_subconjunto(t5, todos):
    """Onde a subclasse T1+T2 tem estoque > 0 em todos os seus municipios, o
    vetor do escopo 'todos' tem de conter o do escopo T1+T2."""
    S = todos['estoque']
    for s in t5['elig']:
        if s in S['M']:
            assert (S['pres'][s] | ~t5['pres'][s]).all() or (t5['M'][s][~S['pres'][s]] == 0).all(), s


def test_todos_rotulos_reprodutiveis(todos, ws):
    for p, S in todos.items():
        for s in S['elig'][:25]:
            lab, _ = C.lisa_rotulos(S['M'][s], ws['queen'])
            np.testing.assert_array_equal(lab, S['labs'][(s, 'queen')])


def test_painel_v7(base, lisa_v6, todos):
    if not PAINEL_V7.exists():
        pytest.skip('rode scripts/21_painel_v7.py')
    L7 = C.ler_lisa_painel(PAINEL_V7.read_text(encoding='utf-8'))[0]
    n6 = len(lisa_v6['mapas'])
    assert L7['names'] == lisa_v6['names'] and L7['mapas'][:n6] == lisa_v6['mapas']
    reorder = C.reordenacao_painel(L7, base['gdf_index'])
    for esc, p in (('todest', 'estoque'), ('todganho', 'ce_rie_ganhos'), ('todperda', 'ce_rie_perdas')):
        mapas = [m for m in L7['mapas'] if m.get('esc') == esc]
        r = todos[p]['resumo']
        assert len(mapas) == int(r['entra_painel'].sum())
        assert all(m['tipo'] == 'uni' for m in mapas)
        for m in mapas:
            assert m['cats'] == C.para_cats(todos[p]['labs'][(m['rotulo'], 'queen')], reorder)


def test_painel_v8():
    """v8 = v7 com outra abertura: mesmos dados, aba Clusters e escopo todest."""
    if not (PAINEL_V7.exists() and PAINEL_V8.exists()):
        pytest.skip('rode scripts/21_painel_v7.py e 22_painel_v8.py')
    h7 = PAINEL_V7.read_text(encoding='utf-8')
    h8 = PAINEL_V8.read_text(encoding='utf-8')
    assert C.ler_lisa_painel(h8)[0] == C.ler_lisa_painel(h7)[0]
    assert C.ler_db_painel(h8)[0] == C.ler_db_painel(h7)[0]
    assert '<button class="tab active" data-view="clusters">' in h8
    assert "esc='todest'" in h8 and '<button class="on" data-esc="todest">' in h8


def test_painel_ciet_v8():
    """Painel publicado (CIET) = dados do v8 + customizacoes do CIET."""
    if not (PAINEL_V8.exists() and PAINEL_CIET.exists()):
        pytest.skip('rode scripts/22_painel_v8.py e 23_painel_ciet_v8.py')
    h8 = PAINEL_V8.read_text(encoding='utf-8')
    hc = PAINEL_CIET.read_text(encoding='utf-8')
    assert C.ler_lisa_painel(hc)[0] == C.ler_lisa_painel(h8)[0]
    assert C.ler_db_painel(hc)[0] == C.ler_db_painel(h8)[0]
    for marca in ('brand-logo', 'f-periodo', 'stockIndex', "esc='todest'",
                  '<button class="tab active" data-view="clusters">'):
        assert marca in hc, marca


def test_todos_sem_alto_em_ausentes(todos):
    """Nos escopos 'todos' o ausente (0) e o minimo: nenhum Alto-Alto/Alto-Baixo
    pode cair num municipio sem o setor (era o artefato do CE+RIE com sinal)."""
    for p, S in todos.items():
        for s in S['elig']:
            lab = S['labs'][(s, 'queen')]
            assert not ((lab == 1) | (lab == 4))[~S['pres'][s]].any(), (p, s)


def test_ganhos_perdas_particionam(todos):
    g, p = todos['ce_rie_ganhos'], todos['ce_rie_perdas']
    for s in set(g['pres']) & set(p['pres']):
        assert not (g['pres'][s] & p['pres'][s]).any(), s
