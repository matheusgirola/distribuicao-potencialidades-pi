# Análise de Agrupamentos Espaciais das Subclasses T1 e T2 — Piauí (magnitude do Estoque)

*LISA municipal e autocorrelação espacial multivariada (Moran bivariado) das
subclasses T1/T2 do arquivo `potencialidades_consolidado.csv`, usando o **valor de
`Estoque_mun_ano_final`** de cada variável em vez de presença/ausência binária.*

*Malha: **Malha Municipal Digital 2025 do IBGE** (`PI_Municipios_2025`), todos os
**224** municípios do Piauí.*

> Complemento do estudo de presença/ausência em `report.md`. Todos os arquivos desta
> versão levam o sufixo `_estoque` e ficam em `data_estoque/` e `figures_estoque/`.

> **Convenção de quadrantes.** Alto-Alto (AA), Baixo-Baixo (BB), Baixo-Alto (BA) e
> Alto-Baixo (AB). As legendas dos mapas usam os rótulos em inglês
> High-High / Low-Low / Low-High / High-Low.

---

## 1. O que muda em relação à análise binária

A variável analisada é a **magnitude do estoque** (`Estoque_mun_ano_final`), e não um
indicador 0/1. Um agrupamento **Alto-Alto** passa, então, a significar *"estoque alto
cercado por estoque alto"* — um verdadeiro *hotspot* de intensidade — e não apenas
presença conjunta.

Observações metodológicas específicas do uso da magnitude:

* **Linhas duplicadas** (2.664 dos 5.895 pares município×subclasse) nunca divergem no
  Estoque, então são consolidadas com `max()` (≡ primeiro ≡ média, neste caso).
* **Ausência → 0.** Uma subclasse nunca registrada em um município é um zero
  verdadeiro.
* **Transformação log.** O Estoque bruto é extremamente assimétrico à direita (p.ex.
  53.442 cabeças de aves ao lado de contagens de 4–16) e mistura unidades (*pessoas*,
  *mil reais*, *cabeças*). Aplica-se `log1p(x) = ln(1 + x)` antes de todas as
  estatísticas espaciais, para que uns poucos municípios grandes não dominem todos os
  agrupamentos.
* **Unidades mistas não são problema para as estatísticas.** O Moran Local e o Moran
  Bivariado padronizam cada variável internamente, então cada subclasse é analisada
  em sua própria escala; magnitudes nunca são comparadas entre subclasses diferentes.

---

## 2. Dados e métodos (resumo)

Mesmo *pipeline* do estudo binário: filtro T1/T2 (9.466 registros, 224 municípios,
710 subclasses); contiguidade **Queen padronizada por linha** sobre a **malha oficial
do IBGE 2025** (`data/piaui_shp_2025/PI_Municipios_2025.shp`, todos os 224 municípios,
SRC EPSG:4674); 999 permutações, semente 42, *p* < 0,05; filtro de prevalência de
5–219 presentes (**217** subclasses analisadas).

* **Matrizes:** `data_estoque/estoque_matrix_raw.csv` (bruta) e
  `estoque_matrix_log.csv` (log, usada nas etapas seguintes).
* **Univariada:** `esda.Moran` / `esda.Moran_Local` sobre o log-Estoque.
* **Multivariada:** `esda.Moran_BV` / `esda.Moran_Local_BV`; pares candidatos
  pré-selecionados pela correlação de Pearson dos vetores log-Estoque (|r| ≥ 0,30).

---

## 3. Resultados da LISA univariada (log-Estoque)

**58 subclasses** apresentam autocorrelação espacial global positiva significativa
(ante 52 na versão binária) — usar a magnitude revela *mais* estrutura. Entre elas,
**764** registros municipais caem em agrupamentos **Alto-Alto** significativos,
abrangendo **196** municípios distintos.

### 3.1 Subclasses com agrupamento mais forte

| # | Subclasse | Municípios | I Global | p | AA | BB |
|---|---|---:|---:|---:|---:|---:|
| 1 | Mel de abelha | 112 | 0,720 | 0,001 | 62 | 67 |
| 2 | Galináceos total | 32 | 0,572 | 0,001 | 22 | 120 |
| 3 | Babaçu amêndoa | 43 | 0,458 | 0,001 | 17 | 0 |
| 4 | Ovino | 137 | 0,457 | 0,001 | 45 | 39 |
| 5 | Cultivo de milho | 9 | 0,438 | 0,001 | 6 | 47 |
| 6 | Outros | 5 | 0,416 | 0,001 | 3 | 184 |
| 7 | Soja em grão | 23 | 0,415 | 0,001 | 14 | 36 |
| 8 | Arroz em casca | 103 | 0,394 | 0,001 | 30 | 35 |
| 9 | Tucum amêndoa | 14 | 0,355 | 0,001 | 12 | 2 |
| 10 | Serviço de preparação de terreno, cultivo e colheita | 6 | 0,309 | 0,001 | 4 | 15 |
| 11 | Castanha de caju | 74 | 0,304 | 0,001 | 20 | 43 |
| 12 | Condomínios prediais | 7 | 0,297 | 0,001 | 3 | 114 |

*O mel fortalece-se bastante em relação à versão binária (I: 0,58 → 0,72), e a
**Castanha de caju** entra no primeiro escalão — a magnitude de seu estoque se agrupa
mesmo com presença relativamente disseminada.*

Classificação completa: `data_estoque/global_moran_by_subclasse_estoque.csv`.

### 3.2 Onde estão os agrupamentos Alto-Alto (de intensidade)

Os municípios de *hotspot* dominantes são as mesmas duas regiões, com o eixo
**Altos–União–José de Freitas–Teresina** agora como o núcleo de intensidade mais
forte, seguido pela **fronteira de grãos do sudoeste** (Baixa Grande do Ribeiro,
Currais):

Altos, União, José de Freitas, Barras, Teresina, Batalha, Baixa Grande do Ribeiro,
Luís Correia.

![Principais mapas LISA univariados — Estoque](figures_estoque/overview_univariate_lisa_estoque.png)

Mapas individuais: `figures_estoque/univariate_lisa/`.
Membros AA: `data_estoque/lisa_hh_clusters_estoque.csv`;
todos os significativos: `data_estoque/lisa_all_significant_estoque.csv`.

---

## 4. Autocorrelação espacial multivariada (bivariada) (log-Estoque)

Dos 2.000 pares candidatos, **605 pares são significativamente co-agrupados no
espaço**. Os quadrantes locais dos pares mais fortes dão **336 registros Alto-Alto**
significativos e **4.169 registros Baixo-Baixo** significativos. Como antes, o
Baixo-Baixo marca zonas de *ausência conjunta*; o sinal informativo é o **Alto-Alto**
— onde **ambas** as subclasses têm estoque alto e seus vizinhos também.

Tabela completa de pares: `data_estoque/bivariate_moran_pairs_estoque.csv`;
membros AA/BB: `data_estoque/multivariate_hh_ll_clusters_estoque.csv`.

Os agrupamentos AA bivariados se concentram no eixo
**Altos–Teresina–José de Freitas–União**, o núcleo de alta intensidade do estado.

---

## 5. Os 20 pares de subclasses mais co-localizados (maior correlação bivariada)

Ordenados por |I de Moran Bivariado| entre os pares significativos; mapas em
`figures_estoque/bivariate_lisa/`.

| # | Subclasse X | Subclasse Y (defasagem espacial) | r | I Biv. | p |
|---|---|---|---:|---:|---:|
| 1 | Cultivo de milho | Serviço de preparação de terreno, cultivo e colheita | 0,75 | 0,390 | 0,001 |
| 2 | Aromáticos medicinais tóxicos e corantes | Outros | 0,75 | 0,324 | 0,001 |
| 3 | Babaçu amêndoa | Oleaginosos | 0,81 | 0,317 | 0,001 |
| 4 | Bares e estab. de bebidas | Condomínios prediais | 0,65 | 0,264 | 0,002 |
| 5 | Cultivo de soja | Soja em grão | 0,63 | 0,253 | 0,001 |
| 6 | Comércio atacadista de soja | Serviço de preparação de terreno, cultivo e colheita | 0,73 | 0,243 | 0,001 |
| 7 | Condomínios prediais | Hotéis | 0,68 | 0,214 | 0,004 |
| 8 | Com. atacadista de máquinas agropecuárias | Serviço de preparação de terreno, cultivo e colheita | 0,76 | 0,189 | 0,001 |
| 9 | Manut./reparação de máquinas agrícolas | Serviço de preparação de terreno, cultivo e colheita | 0,73 | 0,174 | 0,001 |
| 10 | Carnaúba pó | Ceras | 1,00 | 0,167 | 0,001 |
| 11 | Comércio atacadista de soja | Manut./reparação de máquinas agrícolas | 0,68 | 0,149 | 0,001 |
| 12 | Com. atacadista de máquinas agropecuárias | Comércio atacadista de soja | 0,89 | 0,141 | 0,001 |
| 13 | Com. varejista de animais vivos e alimentos p/ pets | Promoção de vendas | 0,62 | 0,128 | 0,003 |
| 14 | Comércio varejista de artigos de papelaria | Promoção de vendas | 0,63 | 0,116 | 0,003 |
| 15 | Restaurantes e similares | Serviços combinados de escritório e apoio administrativo | 0,61 | 0,115 | 0,027 |
| 16 | Com. varejista de animais vivos e alimentos p/ pets | Restaurantes e similares | 0,63 | 0,115 | 0,008 |
| 17 | Com. varejista de animais vivos e alimentos p/ pets | Educação infantil - pré-escola | 0,70 | 0,114 | 0,003 |
| 18 | Com. atacadista de produtos de higiene e limpeza | Promoção de vendas | 0,65 | 0,107 | 0,012 |
| 19 | Construção de rodovias e ferrovias | Educação infantil - pré-escola | 0,65 | 0,106 | 0,001 |
| 20 | Com. varejista de animais vivos e alimentos p/ pets | Lanchonetes, casas de chá, de sucos e similares | 0,67 | 0,102 | 0,010 |

![Principais mapas LISA bivariados — Estoque](figures_estoque/overview_bivariate_lisa_estoque.png)

### 5.1 Interpretação

* **Complexo agro de grãos (sudoeste).** Cultivo de milho/soja ↔ serviços de
  preparação de terreno ↔ atacado de soja ↔ atacado/reparação de máquinas agrícolas
  se co-agrupam por intensidade de estoque (pares 1, 5, 6, 8, 9, 11, 12) — uma
  fronteira de *commodities* fortemente integrada.
* **Cadeias de valor extrativas (norte).** Babaçu–oleaginosos (par 3) e, visível pela
  magnitude, **Carnaúba pó ↔ Ceras** (par 10, r = 1,00) — a cadeia de processamento
  da cera de carnaúba, cujo *volume* se agrupa mesmo que a presença binária não a
  destacasse entre as primeiras posições.
* **Núcleo de serviços urbanos (RM de Teresina).** Bares–condomínios,
  condomínios–hotéis, pet shop–(promoção de vendas / restaurantes / pré-escola /
  lanchonetes), papelaria–promoção de vendas, obras rodoviárias–pré-escola (pares 4,
  7, 13–20) — serviços cuja escala se concentra na região metropolitana.

---

## 6. Binário vs. Estoque — o que a magnitude acrescenta

| | Binário (presença) | Estoque (magnitude log) |
|---|---|---|
| Agrupamentos univariados significativos | 52 | **58** |
| Registros AA significativos (univariado) | 640 | 764 |
| Pares bivariados significativos | 617 | 605 |
| Subclasse líder (I Global) | Mel de abelha (0,58) | Mel de abelha (**0,72**) |
| Novos sinais revelados | — | Castanha de caju; cadeia Carnaúba pó–Ceras |

**Conclusão.** Usar a magnitude do estoque *fortalece* o sinal espacial para a
maioria das subclasses e expõe *hotspots* de intensidade e cadeias de valor (cera de
carnaúba, caju) que a presença binária achata. A geografia geral não muda — um núcleo
**Teresina/Cocais** ao norte e uma **fronteira de grãos do Cerrado** no sudoeste — mas
a visão de magnitude identifica *onde o volume está concentrado*, e não apenas onde a
atividade existe.

---

## 7. Arquivos e reprodutibilidade

Execute em ordem a partir de `scripts/`:

| Etapa | Script | Produz (em `data_estoque/` ou `figures_estoque/`) |
|---|---|---|
| 1 | `E01_build_estoque_matrix.py` | matrizes bruta e log do Estoque, resumo |
| 2 | `E02_univariate_lisa_estoque.py` | Moran global, AA, todos os significativos |
| 3 | `E03_multivariate_spatial_estoque.py` | pares bivariados, AA/BB, top-20 |
| 4 | `E04_generate_maps_estoque.py` | mapas LISA univariados e bivariados |
| 5 | `E05_overview_montage_estoque.py` | figuras-resumo (montagem) |

### Limitações
* **A transformação log** comprime as diferenças de magnitude; os *hotspots* refletem
  intensidade relativa em escala logarítmica, e não totais brutos.
* **Magnitudes entre subclasses não são comparáveis** (unidades mistas); isso é
  tratado pela padronização por variável dentro das estatísticas.
* **O Moran bivariado é direcional**; o I reportado é a média simétrica e os mapas
  locais fixam a direção *x → lag(y)*.
* **Testes múltiplos** valem como no estudo binário.
