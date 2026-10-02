# Pipeline de reprodução — análise espacial das potencialidades T1+T2 (Piauí)

Este documento descreve a ordem de execução e as dependências de todos os scripts do
projeto, incluindo os três geradores de pickles que faltavam no pacote entregue
(`00_base_malha_e_matrizes.py`, `00b_matriz_tempo_ors.py` e `19_dados_planilha.py`).
Todos os scripts leem e gravam na pasta `robustez/` relativa ao diretório de trabalho;
ajuste os caminhos de insumo (constantes no topo de cada script) conforme o ambiente.

## Insumos externos

| Arquivo | Origem |
|---|---|
| `PI_Municipios_2025.shp` (+ .shx/.dbf/.prj) | Malha Municipal Digital 2025, IBGE (oficial; mirrors de terceiros omitem Nazária) |
| `potencialidades_consolidado_v2.csv` | Base consolidada de potencialidades do projeto (versão 2) |
| `shift-share-consolidado-Brasil.csv` | Consolidado shift-share RAIS (encoding latin-1) |
| `RODOVIAS_EST_PI.gpkg`, `RODOVIAS_FEDERAIS_PI.gpkg` | Malha viária DER-PI/DNIT (extraídos de RODOVIAS.rar) |
| `matriz_ors_duracao_s.csv`, `matriz_ors_distancia_m.csv` | Gerados localmente por `extrair_matriz_ors.py` (OpenRouteService) |
| `painel_potencialidades_v5.html` | Painel-base para a geração do v6 |

## Ordem de execução e produtos

| # | Script | Depende de | Produz |
|---|---|---|---|
| 1 | `00_base_malha_e_matrizes.py` | shapefile IBGE | `base.pkl` (ordem canônica dos 224 municípios, centroides EPSG:5880, W Queen / KNN-5 / dist. inversa 76,5 km) |
| 2 | `08_rede_rodoviaria.py` | `base.pkl`, GPKGs de rodovias | `rede.pkl` (distâncias rodoviárias Dijkstra e W-rede, banda 107,9 km) |
| 3 | `00b_matriz_tempo_ors.py` | `base.pkl`, `rede.pkl`, CSVs do ORS | `tempo.pkl` (tempos simetrizados, imputação MQO tempo~dist p/ 4 municípios, W-tempo, banda 133 min) |
| 4 | `10_v2_extra.py` | `base.pkl`, `t1t2_5w_estoque.pkl`*, CSV v2 | `t1t2_v2_extra.pkl` (Moran global, FDR 9.999 uni e biv do pipeline de estoques) |
| 5 | `12_t1t2_5w.py` | `base.pkl`, `rede.pkl`, `tempo.pkl`, CSVs | `t1t2_5w_estoque.pkl` + `concordancia_T1T2_5matrizes.csv` (labs e Moran bivariado sob as 5 matrizes, dois pipelines) |
| 6 | `16_ss_state.py` | idem 5 | `ss_state.pkl` (estado completo CE+RIE: labs 5W, Moran global, FDR, bivariado) |
| 7 | `19_dados_planilha.py` | `base.pkl`, `t1t2_5w_estoque.pkl`, `t1t2_v2_extra.pkl`, `ss_state.pkl` | `xls_uni_{est,ss}.pkl`, `xls_core_{est,ss}.pkl`, `xls_mun_{est,ss}.pkl` |
| 8 | `17_cruzamento.py` | pickles xls_core + estados | `xls_cross.pkl`, `duplo_nucleo_32_pares.csv`, `tab/tabelas_unif.json`, figura de convergência |
| 9 | `15_relatorio_ss.py` | estados + shapefile | tabelas/figuras do relatório CE+RIE (`tab/`, `fig/`) |
| 10 | `gerar_relatorio_unificado.js` (Node) | `tab/`, `fig/`, `docx_lib.js` da skill | `Analise_espacial_integrada_potencialidades.docx` |
| 11 | `gerar_planilha.py` | pickles xls_* | `Base_analise_espacial_potencialidades.xlsx` (recalcular fórmulas após gerar) |
| 12 | `18_painel_v6.py` | `ss_state.pkl`, painel v5 | `painel_potencialidades_v6.html` |

\* Observação sobre a ordem 4↔5: `10_v2_extra.py` lê `t1t2_5w_estoque.pkl` apenas para
reaproveitar a lista de subclasses elegíveis e pares; numa reprodução do zero, execute
o passo 5 antes do 4.

Scripts históricos mantidos por documentação (superados pelos acima): `01`–`03`
(universo completo, pré-recorte T1+T2), `09` (versão 4 matrizes), `11`/`13b` (painéis
v4/v5), `14` (tabelas do relatório de estoques).

## Notas de reprodutibilidade

1. **Determinismo.** Todos os LISA locais (`Moran_Local`) e bivariados locais
   (`Moran_Local_BV`) usam `seed=42` e reproduzem exatamente. O Moran bivariado
   global vetorizado usa `numpy.random.default_rng(42)` e também é exato (o esquema
   de permutação replica o do `esda.Moran_BV`, validado contra o pacote com
   divergência do I observado da ordem de 10⁻¹⁷).
2. **Exceção conhecida.** O I de Moran **global univariado** usa `esda.Moran`, que não
   aceita semente; o pseudo p-valor com 999 permutações flutua ±0,01 entre execuções.
   Isso não altera nenhuma classificação de significância nem qualquer número citado
   nos relatórios (verificado em reprodução completa: única divergência observada foi
   p = 0,146 vs 0,155 em uma subclasse não significativa). Para fixar também esse
   valor, chame `numpy.random.seed(42)` imediatamente antes de cada `Moran(...)`.
3. **Encoding.** O consolidado shift-share é latin-1; os demais CSV são utf-8-sig com
   separador `;` e decimal `,`.
4. **Ambiente.** Python 3.12 · esda 2.10.0 · libpysal 4.15.0 · geopandas 1.1.4 ·
   scipy/shapely (rede rodoviária) · Node + biblioteca `docx` (relatórios) ·
   openpyxl + recálculo LibreOffice (planilha).
