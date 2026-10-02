# Mapa de Potencialidades Econômicas do Piauí — Painel Interativo

Painel interativo com o mapeamento de potencialidades produtivas dos 224
municípios e 12 Territórios de Desenvolvimento do Piauí, com base na tipologia
de análise shift-share de Montanía et al. (2024).

## Acesso ao painel

Se você foi direcionado para esta página em vez do painel, use o link abaixo:

```
https://matheusgirola.github.io/distribuicao-potencialidades-pi
```

Fontes de dados: RAIS (MTE) 2025 e pesquisas do IBGE (PAM, PPM, PEVS) de 2025,
com janelas de comparação a partir de 2013, 2018 e 2022. A tipologia T1–T8/T-1
classifica os setores pelos componentes shift-share: **CE** (efeito
competitivo), **RIE** (efeito regional industrial) e **RSE** (efeito de
reestruturação sistêmica).

---

## Análise espacial dos setores produtivos (shift-share)

Clusters espaciais (I de Moran global, LISA univariado e bivariado) dos
resultados da decomposição shift-share dos 224 municípios do Piauí. Cada par
município × subclasse é classificado pela tipologia regional de Montanía et al.
(2024), de T1 a T8 e T-1. O produto principal é o painel HTML autocontido
[`index.html`](index.html), publicado no GitHub Pages com a identidade visual do
CIET. A mesma versão sem a estética CIET fica em `saidas/painel_potencialidades_v8.html`.

- Regras de trabalho e arquitetura: [`CLAUDE.md`](CLAUDE.md)
- Estado, decisões e pendências: [`CONTEXTO_PROJETO.md`](CONTEXTO_PROJETO.md)
- Colunas dos insumos e estrutura do painel: [`docs/REFERENCIA_DADOS_PAINEL.md`](docs/REFERENCIA_DADOS_PAINEL.md)
- Metodologia: [`docs/metodologia_clusters_espaciais.md`](docs/metodologia_clusters_espaciais.md)

## Ambiente

```bash
uv sync
```

Python 3.12, com **esda 2.10.0 fixado**: as permutações do LISA mudam entre
versões do esda, e essa é a versão que reproduz o painel publicado. O
`uv.lock` fixa o restante. O docx do relatório exige Node e o pacote `docx`
(`npm install docx`).

## Rodar

```bash
uv run python scripts/executar_pipeline.py --listar
```

```bash
uv run python scripts/executar_pipeline.py todos testes
```

Grupos: `malha` (00, 08, 00b), `t1t2` (12, 10, 16), `relatorio` (19, 14, 15, 17,
planilha, js), `todos` (20, 21, 22, 23) e `testes`. `tudo` roda todos os grupos, menos a
etapa congelada 18, que regravaria o painel v6 publicado. Cada etapa grava um log
em `logs/`.

Testes de regressão, que comparam com os mapas publicados:

```bash
uv run pytest
```

## Estrutura

```
index.html             painel publicado no GitHub Pages (gerado pelo script 23)
.nojekyll              impede o GitHub Pages de processar o site com Jekyll
dados/                 insumos
  potencialidades_consolidado_v2.csv   estoques por subclasse x município x ano-base (UTF-8 BOM, ;)
  shift-share-consolidado-Brasil.csv   CE, RIE, RSE da RAIS (latin-1, ;) — fora do git (121 MB)
  matriz_ors_*.csv                     tempo/distância entre sedes (OpenRouteService)
  geo/                                 malha IBGE 2025, sedes 2022, rodovias DER-PI/DNIT
scripts/
  comum.py             caminhos, parâmetros e funções compartilhadas
  00, 08, 00b          base.pkl, rede.pkl, tempo.pkl (matrizes W)
  12, 10, 16           escopos T1+T2 (estoque e CE+RIE): LISA 5 W, FDR, bivariado
  19, 14, 15, 17, gerar_planilha.py, gerar_relatorio_unificado.js   relatório e planilha
  18                   painel v6 (congelado)
  20                   univariado de TODAS as subclasses: estoque, ganhos e perdas de CE+RIE
  21                   painel v7 = v6 + escopos "Todos"
  22                   painel v8 = v7 abrindo em Clusters, Todos · Estoques
  23                   index.html (painel publicado, estética CIET) com os dados do v8
  executar_pipeline.py executor com logs
  cnae_map.py          subclasse CNAE -> seção (heurístico)
  legado/              scripts históricos (caminhos antigos)
robustez/              pickles intermediários (regeneráveis, fora do git)
saidas/                painéis, CSVs, planilha, docx; tab/ e fig/ do relatório
docs/                  metodologia, adendos e relatórios editados
testes/                regressão e diagnósticos
t1_emergentes/         subprojeto das emergentes T-1
legado/                arquivos substituídos (mantidos para rastreio)
```

## Escopos do painel (aba Clusters Espaciais)

| Escopo | Variável | Univariado | Bivariado |
|---|---|---|---|
| Emergentes (T-1) | estoque das emergentes | 50 | 24 |
| T1+T2 · Estoques | log1p(estoque), só pares T1/T2 | 54 | 1.298 |
| T1+T2 · CE+RIE | log sinalizado de CE+RIE, só T1/T2 | 28 | 568 |
| Todos · Estoques | log1p(estoque > 0), qualquer tipologia | 143 | — |
| Todos · Ganhos CE+RIE | log1p(CE+RIE) onde CE+RIE > 0 | 35 | — |
| Todos · Perdas CE+RIE | log1p(\|CE+RIE\|) onde CE+RIE < 0 | 61 | — |

Parâmetros: contiguidade Queen padronizada por linha, 999 permutações, seed 42,
p < 0,05; FDR de Benjamini–Hochberg com 9.999 permutações; robustez sob KNN-5,
distância inversa, rede rodoviária e tempo de viagem. Nos escopos "Todos" entram
as subclasses presentes em pelo menos 10 municípios que tenham I global
significativo ou ao menos 3 núcleos Alto-Alto robustos às 4 matrizes
alternativas. O motivo de separar ganhos e perdas está no `CONTEXTO_PROJETO.md`,
§2.

## Publicar o painel

O `index.html` não é editado à mão. A base com a estética CIET fica em
`saidas/painel_ciet_base_v6.html`; o script 23 aplica a ela os dados do v8:

```bash
uv run python scripts/executar_pipeline.py 22 23 testes
```

Depois, `git add index.html`, `git commit` e `git push`. O GitHub Pages
republica em 1–2 minutos.

## Insumos fora do git

`dados/shift-share-consolidado-Brasil.csv` (121 MB) e os pickles de `robustez/`
ficam fora do repositório. Os pickles são regenerados pelo pipeline. Para
regerar as matrizes do ORS, `scripts/extrair_matriz_ors.py` exige a variável de
ambiente `ORS_API_KEY`.
