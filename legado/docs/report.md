# Análise de Agrupamentos Espaciais das Subclasses de Potencialidade T1 e T2 — Piauí

*LISA municipal e autocorrelação espacial multivariada (Moran bivariado) das
subclasses T1/T2 do arquivo `potencialidades_consolidado.csv`.*

*Malha: **Malha Municipal Digital 2025 do IBGE** (`PI_Municipios_2025`), todos os
**224** municípios do Piauí.*

---

## 1. Objetivo

Identificar onde as **subclasses de potencialidade** econômica classificadas como
**T1** e **T2** se agrupam no espaço entre os municípios do Piauí, e quais
subclasses tendem a **co-localizar-se**. Especificamente:

1. Construir uma matriz binária de presença *município × subclasse* (presença em
   **qualquer** ano de referência conta como 1).
2. Rodar uma **LISA univariada** (I de Moran Local) por subclasse e isolar os
   agrupamentos **Alto-Alto** estatisticamente significativos.
3. Rodar uma **autocorrelação espacial multivariada / bivariada** e reportar apenas
   os agrupamentos significativos **Alto-Alto** e **Baixo-Baixo**.
4. Mapear os **20 pares** de subclasses mais fortemente co-localizados.

> **Convenção de quadrantes.** Alto-Alto (AA), Baixo-Baixo (BB), Baixo-Alto (BA) e
> Alto-Baixo (AB). As legendas dos mapas usam os rótulos em inglês
> High-High / Low-Low / Low-High / High-Low.

---

## 2. Dados e métodos

### 2.1 Dados de origem
`potencialidades_consolidado.csv` — 51.179 registros, 8 campos, separados por `;`.
Filtrando `classificacao_regiao` para **T1 e T2** obtém-se:

| Métrica | Valor |
|---|---|
| Registros T1/T2 | 9.466 |
| Municípios cobertos | 224 (todo o Piauí) |
| Subclasses T1/T2 distintas | 710 |

### 2.2 Matriz binária de presença
Um par `(município × subclasse)` recebe **1** quando a subclasse ocorre ali com
classe T1 **ou** T2 em **qualquer** ano, e 0 caso contrário.

* Dimensões da matriz: **224 × 710**
* Total de células de presença (1s): **5.895**
* Mais disseminadas: *Ovos de galinha* (90%), *Milho em grão* (77%), *Mandioca*
  (72%), *Comércio varejista de produtos farmacêuticos* (70%), *Ovino* (61%).

Arquivo: `data/binary_matrix_municipios_subclasses.csv`

### 2.3 Matriz de vizinhança (pesos espaciais)
Limites municipais: o **shapefile oficial do IBGE 2025** fornecido nesta tarefa
(`data/piaui_shp_2025/PI_Municipios_2025.shp`, SRC EPSG:4674 / SIRGAS 2000), que
contém **todos os 224** municípios (`CD_MUN` = código do IBGE; `NM_MUN` coincide
exatamente com o CSV — 224/224, sem divergências de nome). Pesos de **contiguidade
Queen padronizados por linha**; a malha é totalmente conectada (sem ilhas, média de
5,4 vizinhos).

> Isto substitui a malha de terceiros usada antes (223 municípios; faltava Nazária).
> A malha oficial completa é usada em toda a análise; **Nazária agora está incluída**.

### 2.4 Estatísticas
* **LISA univariada** — I de Moran Local (`esda.Moran_Local`), 999 permutações,
  semente = 42, *p* < 0,05. O I de Moran Global ordena a força do agrupamento.
  Quadrantes: AA / BA / BB / AB.
* **Autocorrelação espacial multivariada** — **I de Moran Bivariado**
  (`esda.Moran_BV` / `esda.Moran_Local_BV`): a correlação espacial entre uma
  subclasse em um local e a defasagem espacial (spatial lag) de uma segunda
  subclasse nos municípios vizinhos; produz os quadrantes AA / BB solicitados. O I
  global é a média das duas direções; os mapas locais fixam a direção *x → lag(y)*.
* **Filtro de prevalência** — apenas subclasses presentes em **5–219** municípios
  foram analisadas (**217** subclasses). Os pares candidatos da etapa multivariada
  foram pré-selecionados pela correlação φ (Pearson binário) dos vetores de presença
  (|φ| ≥ 0,30, 2.000 melhores pares).

---

## 3. Resultados da LISA univariada

Das 217 subclasses analisadas, **52 apresentam autocorrelação espacial global
positiva estatisticamente significativa** (*p* < 0,05). Entre elas, **640**
registros municipais caem em agrupamentos **Alto-Alto** significativos, abrangendo
**192** municípios distintos.

### 3.1 Subclasses com agrupamento mais forte (I de Moran Global)

| # | Subclasse | Municípios | I Global | p | AA | BB |
|---|---|---:|---:|---:|---:|---:|
| 1 | Mel de abelha | 112 | 0,582 | 0,001 | 44 | 29 |
| 2 | Galináceos total | 32 | 0,550 | 0,001 | 20 | 41 |
| 3 | Tucum amêndoa | 14 | 0,476 | 0,001 | 11 | 6 |
| 4 | Ovino | 137 | 0,418 | 0,001 | 20 | 32 |
| 5 | Soja em grão | 23 | 0,349 | 0,001 | 11 | 1 |
| 6 | Outros | 5 | 0,346 | 0,001 | 4 | 5 |
| 7 | Cultivo de milho | 9 | 0,343 | 0,001 | 6 | 193 |
| 8 | Arroz em casca | 103 | 0,313 | 0,001 | 33 | 29 |
| 9 | Carvão vegetal | 38 | 0,310 | 0,001 | 13 | 0 |
| 10 | Babaçu amêndoa | 43 | 0,299 | 0,001 | 22 | 36 |
| 11 | Aromáticos medicinais tóxicos e corantes | 6 | 0,275 | 0,001 | 4 | 9 |
| 12 | Cultivo de arroz | 10 | 0,257 | 0,001 | 5 | 50 |

Classificação completa: `data/global_moran_by_subclasse.csv`.

### 3.2 Onde estão os agrupamentos Alto-Alto

Os municípios que aparecem com mais frequência dentro de agrupamentos AA
significativos formam **duas regiões coerentes**:

* **Norte / Centro-Norte (Região Metropolitana de Teresina + Vale do Longá /
  Cocais):** Altos, José de Freitas, União, Teresina, Barras, Batalha, Piripiri — a
  faixa mais populosa e diversificada (pecuária, extrativismo, comércio de consumo).
* **Sudoeste — fronteira de grãos do Cerrado / MATOPIBA:** Baixa Grande do Ribeiro,
  Uruçuí, Currais e vizinhos — o cinturão de grãos mecanizado (soja, arroz, milho) e
  seus serviços agropecuários.

![Principais mapas LISA univariados](figures/overview_univariate_lisa.png)

Mapas individuais das 12 principais subclasses: `figures/univariate_lisa/`.
Municípios AA significativos: `data/lisa_hh_clusters.csv`;
todos os quadrantes significativos: `data/lisa_all_significant.csv`.

---

## 4. Autocorrelação espacial multivariada (bivariada)

Dos 2.000 pares candidatos, **617 pares de subclasses são significativamente
co-agrupados no espaço** (*p* < 0,05). Extraindo os quadrantes locais dos pares mais
fortes, obtêm-se **275 registros Alto-Alto** significativos e **5.876 registros
Baixo-Baixo** significativos.

**Como ler os dois quadrantes.** Como a maioria das subclasses T1/T2 é relativamente
rara, o **Baixo-Baixo** domina: grandes zonas contíguas de *ausência conjunta*. O
sinal economicamente informativo é o **Alto-Alto** — municípios onde **ambas** as
subclasses estão presentes e seus vizinhos também. Esses agrupamentos AA se
concentram nas mesmas duas regiões da análise univariada, de forma mais nítida na
**fronteira de grãos do sudoeste** e no eixo **Teresina–Altos–José de Freitas**.

Tabela completa de pares: `data/bivariate_moran_pairs.csv`;
municípios membros AA/BB: `data/multivariate_hh_ll_clusters.csv`.

---

## 5. Os 20 pares de subclasses mais co-localizados (maior correlação bivariada)

Ordenados por |I de Moran Bivariado| entre os pares significativos. Um mapa de cada
par está em `figures/bivariate_lisa/`.

| # | Subclasse X | Subclasse Y (defasagem espacial) | φ | I Biv. | p |
|---|---|---|---:|---:|---:|
| 1 | Aromáticos medicinais tóxicos e corantes | Outros | 0,72 | 0,310 | 0,001 |
| 2 | Cultivo de milho | Serviço de preparação de terreno, cultivo e colheita | 0,53 | 0,297 | 0,001 |
| 3 | Cultivo de arroz | Soja em grão | 0,50 | 0,296 | 0,001 |
| 4 | Comércio atacadista de soja | Cultivo de milho | 0,58 | 0,260 | 0,002 |
| 5 | Cultivo de soja | Soja em grão | 0,60 | 0,233 | 0,001 |
| 6 | Babaçu amêndoa | Oleaginosos | 0,79 | 0,232 | 0,001 |
| 7 | Comércio atacadista de soja | Serviço de preparação de terreno, cultivo e colheita | 0,54 | 0,218 | 0,001 |
| 8 | Cultivo de milho | Cultivo de outros cereais n.e. | 0,49 | 0,192 | 0,013 |
| 9 | Bares e estab. de bebidas | Condomínios prediais | 0,66 | 0,188 | 0,006 |
| 10 | Manut./reparação de máquinas agrícolas | Serviço de preparação de terreno, cultivo e colheita | 0,54 | 0,156 | 0,001 |
| 11 | Comércio atacadista de soja | Manut./reparação de máquinas agrícolas | 0,59 | 0,148 | 0,003 |
| 12 | Com. atacadista de outros prod. alimentícios | Condomínios prediais | 0,67 | 0,148 | 0,015 |
| 13 | Com. atacadista de outros prod. alimentícios | Com. varejista de artigos esportivos | 0,59 | 0,142 | 0,038 |
| 14 | Com. atacadista de máquinas agropecuárias | Serviço de preparação de terreno, cultivo e colheita | 0,49 | 0,135 | 0,002 |
| 15 | Bares e estab. de bebidas | Com. atacadista de outros prod. alimentícios | 0,46 | 0,133 | 0,021 |
| 16 | Educação infantil - pré-escola | Obras de urbanização (ruas, praças, calçadas) | 0,46 | 0,132 | 0,001 |
| 17 | Alimentícios | Umbu fruto | 0,53 | 0,132 | 0,002 |
| 18 | Com. atacadista de máquinas agropecuárias | Comércio atacadista de soja | 0,72 | 0,129 | 0,005 |
| 19 | Comércio varejista de artigos esportivos | Limpeza em prédios e domicílios | 0,72 | 0,128 | 0,044 |
| 20 | Compra e venda de imóveis próprios | Limpeza em prédios e domicílios | 0,54 | 0,128 | 0,045 |

![Principais mapas LISA bivariados](figures/overview_bivariate_lisa.png)

### 5.1 O que os pares significam

* **Complexo agroindustrial de grãos (sudoeste, Cerrado).** Arroz–soja, milho–soja,
  comércio atacadista de soja, serviços de preparação de terreno e reparação/atacado
  de máquinas agrícolas se co-agrupam de forma intensa (pares 1–5, 7, 8, 10, 11, 14,
  18) — a assinatura de uma fronteira mecanizada de *commodities*, onde produção,
  comércio e serviços especializados se concentram juntos.
* **Assinaturas extrativista e de serviços urbanos (norte).** Babaçu–oleaginosos
  (par 6) marca o cinturão extrativo dos *Cocais* ao norte; os pares de
  consumo/serviços urbanos (bares–condomínios, atacado de alimentos–artigos
  esportivos, imóveis–limpeza, pré-escola–obras de urbanização: pares 9, 12, 13, 15,
  16, 19, 20) se agrupam na Região Metropolitana de Teresina.

---

## 6. Principais conclusões

1. **O agrupamento é real e forte.** 52 das 217 subclasses T1/T2 analisadas estão
   significativamente agrupadas no espaço; a mais forte é *Mel de abelha*
   (I de Moran Global = 0,58).
2. **Dois macro-hotspots** organizam quase todos os agrupamentos Alto-Alto: o
   **norte Teresina / Cocais** e a **fronteira de grãos do Cerrado no sudoeste**.
3. **A co-localização é economicamente coerente** — um complexo agro de grãos no
   sudoeste e um complexo extrativo-mais-serviços-urbanos no norte.
4. **Baixo-Baixo = ausência conjunta**, refletindo a raridade de muitas subclasses
   T1/T2.

---

## 7. Reprodutibilidade

Execute em ordem a partir de `scripts/`:

| Etapa | Script | Produz |
|---|---|---|
| 1 | `01_build_binary_matrix.py` | matriz binária + prevalência |
| 2 | `02_univariate_lisa.py` | tabela do Moran global, agrupamentos AA, todos os significativos |
| 3 | `03_multivariate_spatial.py` | pares bivariados, agrupamentos AA/BB, top-20 |
| 4 | `04_generate_maps.py` | mapas LISA univariados e bivariados |
| 5 | `05_overview_montage.py` | figuras-resumo (montagem) |

`spatial_utils.py` contém os auxiliares compartilhados de geometria/pesos e aponta
para o shapefile oficial 2025. Dependências: `pandas`, `geopandas`, `libpysal`,
`esda`, `matplotlib`, `mapclassify`. Permutações = 999, semente = 42,
significância = 0,05.

### Limitações
* **Somente presença/ausência** — a magnitude do *Estoque* não é usada aqui (veja
  `report_estoque.md` para a versão com magnitude).
* **O Moran bivariado é direcional**; a média simétrica é um resumo e os mapas
  locais fixam uma direção.
* **Testes múltiplos** — com centenas de testes, alguns resultados "significativos"
  são esperados por acaso; os *p*-valores ordenados e a coerência da narrativa
  regional atenuam esse efeito.
