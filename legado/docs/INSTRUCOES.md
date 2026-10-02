# Pacote de arquivos faltantes — instruções de uso

Este pacote completa a sua pasta local com os arquivos que faltavam para reproduzir
os resultados mais recentes (relatório integrado, planilha, mapas/tabelas e painel v6).
Os caminhos internos dos scripts **já foram reescritos para a sua estrutura de pastas**
— diferentemente das cópias anteriores, que usavam caminhos do ambiente de análise.

## 1. Onde colocar cada arquivo

Extraia o zip na RAIZ da sua pasta de trabalho (a mesma que contém `dados/`,
`robustez/`, `scripts/` etc.):

- `scripts/` recebe dez arquivos novos: `10_v2_extra.py`, `14_relatorio_dados.py`,
  `15_relatorio_ss.py`, `16_ss_state.py`, `17_cruzamento.py`, `18_painel_v6.py`,
  `gerar_planilha.py`, `gerar_relatorio_unificado.js`, e as duas bibliotecas
  `docx_lib.js` e `figuras.py` (da skill de relatórios, das quais os scripts 14/15/17
  e o gerador de docx dependem);
- `painel_potencialidades_v5.html` vai para a raiz (é o insumo do script 18).

## 2. Dois ajustes na sua pasta antes de rodar

1. Copie o **`shift-share-consolidado-Brasil.csv`** (o consolidado bruto da RAIS que
   você me enviou; ele não aparece na sua árvore — o `shiftshare_long_ce_rie.csv` da
   raiz é um derivado, não serve) para `dados/`.
2. Crie a pasta de saídas: `mkdir saidas`.

Observação: os scripts que você já tinha (`00`, `00b`, `08`, `12` etc.) ainda apontam
para caminhos do ambiente de análise. Se for reexecutá-los, aplique o mesmo mapeamento:
`/mnt/user-data/uploads/PI_Municipios_2025.shp` → `PI_limites_municipais_2025/PI_Municipios_2025.shp`;
`/mnt/user-data/uploads/<arquivo>.csv` → `dados/<arquivo>.csv`;
`/mnt/user-data/uploads/RODOVIAS_*.gpkg` → `RODOVIAS/…` (no 08, a constante aponta para
a subpasta `rodovias/` — troque para `RODOVIAS/`);
`/mnt/project/…` → raiz; `/mnt/user-data/outputs/` → `saidas/`.
Como sua pasta `robustez/` já contém `base.pkl`, `rede.pkl` e `tempo.pkl`, você só
precisa reexecutar 00/00b/08 se quiser regenerá-los do zero.

## 3. Ordem de execução (a partir da raiz)

```
python scripts/12_t1t2_5w.py          # t1t2_5w_estoque.pkl (ajuste caminhos, ver §2)
python scripts/10_v2_extra.py         # t1t2_v2_extra.pkl + CSV de pares pós-FDR
python scripts/16_ss_state.py         # ss_state.pkl (estado completo CE+RIE)
python scripts/19_dados_planilha.py   # xls_*.pkl (ajuste caminhos, ver §2)
python scripts/14_relatorio_dados.py  # tab/tabelas.json + fig/f1,f2 (estoques)
python scripts/15_relatorio_ss.py     # tab/tabelas_ss.json + fig/f1ss,f2ss (CE+RIE)
python scripts/17_cruzamento.py       # duplo núcleo + fig/f5conv + tab/tabelas_unif.json
node scripts/gerar_relatorio_unificado.js   # saidas/Analise_espacial_integrada_potencialidades.docx
python scripts/gerar_planilha.py      # saidas/Base_analise_espacial_potencialidades.xlsx
python scripts/18_painel_v6.py        # saidas/painel_potencialidades_v6.html
```

## 4. Dependências e observações

- Python 3.12 com `esda`, `libpysal`, `geopandas`, `matplotlib`, `openpyxl`; Node com o
  pacote `docx` (`npm install docx` na raiz).
- A planilha é gravada com as fórmulas ainda não avaliadas; abra no Excel/LibreOffice e
  salve uma vez para recalcular (no ambiente de análise isso era feito por um utilitário
  do LibreOffice).
- No docx, o sumário nasce vazio: clique com o botão direito nele no Word e escolha
  "Atualizar campo".
- Reprodutibilidade: LISA locais e bivariados usam semente 42 (exatos); apenas o pseudo
  p do I de Moran global univariado (999 permutações, sem semente no `esda.Moran`)
  flutua ±0,01 entre execuções, sem efeito em nenhuma classificação ou número citado.
