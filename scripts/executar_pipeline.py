# -*- coding: utf-8 -*-
"""
executar_pipeline.py
--------------------
Roda as etapas do pipeline na ordem de dependencia, cada uma com log proprio
em logs/<script>.log, e para na primeira falha.

    uv run python scripts/executar_pipeline.py --listar
    uv run python scripts/executar_pipeline.py todos           # grupo
    uv run python scripts/executar_pipeline.py 20 21           # etapas avulsas
    uv run python scripts/executar_pipeline.py tudo            # tudo menos o congelado

Etapas marcadas como CONGELADAS regravam um produto publicado (painel v6) e so
rodam se pedidas pelo numero.
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
LOGS = RAIZ / 'logs'

# (id, grupo, comando, descricao)
ETAPAS = [
    ('00',  'malha',     ['python', 'scripts/00_base_malha_e_matrizes.py'], 'base.pkl: ordem canonica + W Queen/KNN-5/dist. inversa'),
    ('08',  'malha',     ['python', 'scripts/08_rede_rodoviaria.py'],       'rede.pkl: W de distancia rodoviaria'),
    ('00b', 'malha',     ['python', 'scripts/00b_matriz_tempo_ors.py'],     'tempo.pkl: W de tempo de viagem (ORS)'),
    ('12',  't1t2',      ['python', 'scripts/12_t1t2_5w.py'],               'T1+T2: LISA e bivariado sob 5 W (estoque e CE+RIE)'),
    ('10',  't1t2',      ['python', 'scripts/10_v2_extra.py'],              'T1+T2 estoque: Moran global + FDR 9.999'),
    ('16',  't1t2',      ['python', 'scripts/16_ss_state.py'],              'T1+T2 CE+RIE: estado completo (ss_state.pkl)'),
    ('19',  'relatorio', ['python', 'scripts/19_dados_planilha.py'],        'pickles xls_* da planilha'),
    ('14',  'relatorio', ['python', 'scripts/14_relatorio_dados.py'],       'tabelas/figuras do relatorio (estoques)'),
    ('15',  'relatorio', ['python', 'scripts/15_relatorio_ss.py'],          'tabelas/figuras do relatorio (CE+RIE)'),
    ('17',  'relatorio', ['python', 'scripts/17_cruzamento.py'],            'cruzamento dos nucleos robustos'),
    ('pl',  'relatorio', ['python', 'scripts/gerar_planilha.py'],           'Base_analise_espacial_potencialidades.xlsx'),
    ('js',  'relatorio', ['node', 'scripts/gerar_relatorio_unificado.js'],  'docx integrado (requer Node + pacote docx)'),
    ('18',  'congelado', ['python', 'scripts/18_painel_v6.py'],             'painel v6 a partir do v5 (CONGELADO: regrava o v6 publicado)'),
    ('20',  'todos',     ['python', 'scripts/20_univariado_todos.py'],      'univariado de TODAS as subclasses (estoque, ganhos e perdas CE+RIE)'),
    ('21',  'todos',     ['python', 'scripts/21_painel_v7.py'],             'painel v7 = v6 + escopos "Todos"'),
    ('22',  'todos',     ['python', 'scripts/22_painel_v8.py'],             'painel v8 = v7 abrindo em Clusters, Todos · Estoques'),
    ('23',  'todos',     ['python', 'scripts/23_painel_ciet_v8.py'],        'index.html publicado (estetica CIET) com os dados do v8'),
    ('t',   'testes',    ['pytest', '-q', '-p', 'no:cacheprovider'],        'regressao contra os resultados publicados'),
]


def selecionar(pedidos):
    ids = {e[0]: e for e in ETAPAS}
    grupos = {e[1] for e in ETAPAS}
    sel = []
    for p in pedidos:
        if p == 'tudo':
            sel += [e for e in ETAPAS if e[1] != 'congelado']
        elif p in grupos:
            sel += [e for e in ETAPAS if e[1] == p]
        elif p in ids:
            sel.append(ids[p])
        else:
            sys.exit(f'etapa ou grupo desconhecido: {p} (use --listar)')
    vistos, ordem = set(), []
    for e in ETAPAS:                      # sempre na ordem de dependencia
        if e in sel and e[0] not in vistos:
            vistos.add(e[0]); ordem.append(e)
    return ordem


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('etapas', nargs='*', help='ids ou grupos (malha, t1t2, relatorio, todos, testes, tudo)')
    ap.add_argument('--listar', action='store_true')
    a = ap.parse_args()
    if a.listar or not a.etapas:
        for i, g, cmd, d in ETAPAS:
            print(f'{i:>4}  {g:<10} {" ".join(cmd[1:2]) or cmd[0]:<40} {d}')
        return
    LOGS.mkdir(exist_ok=True)
    for i, g, cmd, d in selecionar(a.etapas):
        nome = Path(cmd[1]).stem if len(cmd) > 1 and cmd[1].endswith(('.py', '.js')) else 'testes'
        log = LOGS / f'{nome}.log'
        # python/pytest pelo interpretador atual (o do ambiente uv); node pelo PATH
        exe = [sys.executable, '-X', 'utf8'] + (['-m', 'pytest'] + cmd[1:] if cmd[0] == 'pytest' else cmd[1:]) \
            if cmd[0] in ('python', 'pytest') else cmd
        print(f'[{i}] {d} ... ', end='', flush=True)
        t0 = time.time()
        with open(log, 'w', encoding='utf-8') as f:
            r = subprocess.run(exe, cwd=RAIZ, stdout=f, stderr=subprocess.STDOUT)
        print(f'{"ok" if r.returncode == 0 else "FALHOU"} ({time.time() - t0:.0f} s, log: {log.relative_to(RAIZ)})')
        if r.returncode != 0:
            sys.exit(r.returncode)


if __name__ == '__main__':
    main()
