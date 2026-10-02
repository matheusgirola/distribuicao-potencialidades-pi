"""
figuras.py — padrão visual das figuras dos relatórios.

Uso:
    import figuras as F
    F.aplicar_estilo()
    fig, ax = plt.subplots(figsize=(8.2, 3.2))
    ...
    F.salvar(fig, 'f1')
    F.salvar_dimensoes()          # grava fig/sizes.json para o gerador do docx
"""

import json
import os
import glob
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

DIR = str(Path(__file__).resolve().parents[1] / 'saidas' / 'fig')

# Paleta sóbria de três tons. A ideia é que a unidade analisada (PI) se destaque
# das duas referências de comparação, sem cores saturadas.
C = {
    'BR':  '#4C4C4C',   # referência nacional — cinza escuro
    'NE':  '#8C8C8C',   # referência regional — cinza médio
    'PI':  '#1F6F8B',   # unidade analisada — azul-petróleo
    'ALT': '#C0552B',   # destaque / valores negativos — terracota
    'ACC': '#3D8F6B',   # quarta série, quando inevitável — verde acinzentado
}


def aplicar_estilo():
    """Sem moldura completa, grade discreta, fonte pequena. Um gráfico dentro
    de um relatório impresso compete com o texto; discrição é o objetivo."""
    plt.rcParams.update({
        'font.size': 9,
        'font.family': 'DejaVu Sans',
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.grid': True,
        'grid.alpha': 0.25,
        'grid.linestyle': '-',
        'axes.axisbelow': True,
        'figure.dpi': 200,
    })


def fmt(x, d=1):
    """Número no padrão brasileiro: milhar com '.', decimal com ','."""
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return '–'
    return f'{x:,.{d}f}'.replace(',', '@').replace('.', ',').replace('@', '.')


def rotular(ax, barras, casas=1, tamanho=7):
    """Rótulos numéricos nas barras, já formatados em português."""
    ax.bar_label(barras, fmt=lambda v: fmt(v, casas), fontsize=tamanho, padding=1.5)


def destacar_rotulo(ax, nome, cor=None):
    """Deixa em negrito e colorido o rótulo do eixo y correspondente à unidade
    em foco — útil em rankings onde ela precisa ser localizada de imediato."""
    for lbl in ax.get_yticklabels():
        if lbl.get_text() == nome:
            lbl.set_color(cor or C['ALT'])
            lbl.set_fontweight('bold')


def cores_por_sinal(valores):
    """Terracota para negativos, azul para positivos. Em gráficos de variação,
    o sinal precisa ser legível antes de o leitor ler o eixo."""
    return [C['ALT'] if v < 0 else C['PI'] for v in valores]


def salvar(fig, nome, dir_=DIR):
    os.makedirs(dir_, exist_ok=True)
    fig.tight_layout()
    fig.savefig(f'{dir_}/{nome}.png', bbox_inches='tight')
    plt.close(fig)


def salvar_dimensoes(dir_=DIR, largura=600):
    """Calcula altura proporcional para largura fixa e grava sizes.json.

    O gerador do docx lê esse arquivo para inserir cada figura na proporção
    correta. 600 px é a largura que ocupa quase toda a área útil da página A4
    com margens ABNT sem estourar.
    """
    from PIL import Image
    d = {}
    for f in sorted(glob.glob(f'{dir_}/*.png')):
        w, h = Image.open(f).size
        nome = os.path.basename(f).replace('.png', '')
        d[nome] = {'w': largura, 'h': round(h * largura / w)}
    with open(f'{dir_}/sizes.json', 'w') as fp:
        json.dump(d, fp, indent=1)
    return d


# ----------------------------------------------------------- gráficos prontos

def barras_comparadas(categorias, series, ylabel, figsize=(8.2, 3.2), casas=1):
    """Barras agrupadas comparando áreas.

    series: lista de (rotulo, valores, cor) — normalmente Brasil, Nordeste e a
    unidade analisada, nesta ordem, para que a leitura vá do geral ao particular.
    """
    x = np.arange(len(categorias))
    w = 0.8 / len(series)
    fig, ax = plt.subplots(figsize=figsize)
    for i, (rot, vals, cor) in enumerate(series):
        desloc = (i - (len(series) - 1) / 2) * w
        b = ax.bar(x + desloc, vals, w, label=rot, color=cor)
        rotular(ax, b, casas)
    ax.set_xticks(x)
    ax.set_xticklabels(categorias, fontsize=8)
    ax.set_ylabel(ylabel)
    ax.legend(frameon=False, ncol=len(series), fontsize=8)
    ax.axhline(0, color='k', lw=0.8)
    return fig, ax


def ranking_horizontal(rotulos, valores, xlabel, figsize=(8.2, 4.4), casas=1):
    """Barras horizontais ordenadas, com cor por sinal e rótulos numéricos.
    Ordene os dados antes de chamar — a função não reordena."""
    fig, ax = plt.subplots(figsize=figsize)
    b = ax.barh(np.arange(len(rotulos)), valores, color=cores_por_sinal(valores))
    ax.set_yticks(np.arange(len(rotulos)))
    ax.set_yticklabels([str(t)[:52] for t in rotulos], fontsize=7.5)
    rotular(ax, b, casas, 6.5)
    ax.set_xlabel(xlabel)
    ax.axvline(0, color='k', lw=0.8)
    return fig, ax


def indice_base100(anos, series, titulos, figsize=(9.2, 3.1)):
    """Painel de linhas em número-índice, um subplot por indicador.

    series: lista de dicts {rotulo: valores} na mesma ordem de `titulos`.
    Converte para base 100 no primeiro ano — o que permite comparar
    trajetórias de grandezas de magnitudes muito diferentes.
    """
    marcadores = ['o', 's', '^', 'D']
    fig, axes = plt.subplots(1, len(series), figsize=figsize)
    if len(series) == 1:
        axes = [axes]
    for ax, dados, tit in zip(axes, series, titulos):
        for i, (rot, (vals, cor)) in enumerate(dados.items()):
            base = np.array(vals) / vals[0] * 100
            ax.plot(anos, base, marker=marcadores[i % 4], color=cor,
                    label=rot, lw=1.8, ms=4.5)
        ax.set_title(tit, fontsize=9.5)
        ax.set_xticks(anos)
    axes[0].set_ylabel(f'Índice ({anos[0]} = 100)')
    axes[0].legend(frameon=False, fontsize=8)
    return fig, axes
