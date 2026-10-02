# Análise de clusters espaciais das potencialidades T1/T2 do Piauí — versão *shift-share* (CE + RIE)

Terceira variante da análise. Mantém a mesma pergunta e a mesma metodologia
espacial das versões anteriores (binária e de *Estoque*), trocando apenas a
variável de intensidade: agora cada potencialidade é medida pela **soma do
Efeito Competitivo (CE) com o Efeito Regional Industrial (RIE)** do
`shift-share-consolidado-Brasil.csv`.

Todos os resultados são gravados em arquivos próprios (`data_shiftshare/`,
`figures_shiftshare/`), sem sobrescrever nada das análises anteriores.

---

## 1. Dados e regras de construção

| Item | Valor |
|---|---|
| Fonte | `shift-share-consolidado-Brasil.csv` (915.936 linhas, referência geográfica *Brasil*) |
| Filtro de potencialidade | `classificacao_regiao ∈ {T1, T2}` → **6.198 linhas** |
| Variável de intensidade | `valor = CE + RIE` (decimais com vírgula convertidos) |
| Janelas temporais | `ANO_T0 ∈ {2013, 2018, 2022}`, todas com `ANO_T1 = 2025` |
| **Regra de desempate** | quando o par (município, subclasse) aparece em mais de um `ANO_T0`, mantém-se **a janela com o maior CE + RIE** |
| Resultado | **3.920 pares únicos** município × subclasse (2.278 repetições removidas) |
| Composição | 3.138 pares T1 · 782 pares T2 |
| Cobertura | **222 dos 224 municípios** têm ao menos uma potencialidade T1/T2; **650 subclasses** distintas |
| Malha | IBGE, 224 municípios do Piauí, EPSG:4674 (SIRGAS 2000) — inclui **Nazária** |

Quando a mesma potencialidade muda de classe entre janelas (271 casos de T1↔T2),
prevalece a classificação da linha vencedora, ou seja, a da janela de maior CE + RIE.

Distribuição das janelas vencedoras: 2013 → 1.304 pares · 2018 → 1.161 · 2022 → 1.455.

### 1.1 Transformação

Diferentemente do que se poderia esperar de um *shift-share*, **nenhum valor de
CE + RIE é negativo nesta amostra** (mínimo = 0,055; mediana = 11,1; máximo =
85.652). Isso é coerente com a própria definição de T1/T2 como potencialidades
com efeitos positivos. A distribuição é fortemente assimétrica à direita, então
aplicou-se **log1p(CE + RIE)**, exatamente como na versão de *Estoque*. Ausência
do par (município, subclasse) = 0 na matriz.

Matriz resultante: **224 × 650**.

### 1.2 Parâmetros espaciais

Contiguidade **Queen** padronizada por linha · **999 permutações** · semente **42**
· significância **p < 0,05**. Subclasses avaliadas: as **87** presentes em ao menos
10 municípios.

---

## 2. Resultados

### 2.1 Concentração da massa de CE + RIE

A soma total de CE + RIE das potencialidades T1/T2 é de **428.944**, e é
extremamente concentrada:

| Município | Soma CE + RIE |
|---|---|
| Teresina | 283.970 |
| Picos | 17.264 |
| Parnaíba | 15.985 |
| Floriano | 8.800 |
| São Raimundo Nonato | 4.702 |
| Corrente | 4.437 |

Teresina responde sozinha por ~66% de toda a massa. Isso é um argumento
adicional a favor da transformação logarítmica: sem ela, a estatística espacial
seria praticamente uma função da capital.

As subclasses de maior massa são serviços públicos e urbanos (Ensino
fundamental, 89.353; Administração pública em geral, 72.629; Segurança e ordem
pública, 17.339), o que reflete o peso do emprego público na base RAIS.

### 2.2 Moran global (univariado)

**28 das 87 subclasses** apresentam autocorrelação espacial global significativa
(p < 0,05). O I médio entre as significativas é de **0,057**, com máximo de
**0,230**.

| # | Subclasse | Municípios | I de Moran | p | Alto-Alto |
|---|---|---|---|---|---|
| 1 | Cultivo de arroz | 10 | 0,230 | 0,002 | 6 |
| 2 | Hotéis | 22 | 0,216 | 0,001 | 5 |
| 3 | Criação de frangos para corte | 10 | 0,156 | 0,004 | 4 |
| 4 | Criação de bovinos para corte | 30 | 0,148 | 0,002 | 6 |
| 5 | Cultivo de soja | 21 | 0,147 | 0,005 | 5 |
| 6 | Com. varejista de animais vivos e artigos p/ pets | 22 | 0,136 | 0,002 | 4 |
| 7 | Restaurantes e similares | 37 | 0,113 | 0,010 | 7 |
| 8 | Com. varejista de artigos de papelaria | 14 | 0,111 | 0,012 | 4 |
| 9 | Comércio varejista de bebidas | 27 | 0,106 | 0,009 | 6 |
| 10 | Com. varejista de artigos do vestuário | 46 | 0,105 | 0,012 | 6 |

**Diferença relevante em relação à versão de *Estoque*:** os valores de I são
sistematicamente **mais baixos**. A medida CE + RIE é uma taxa de desempenho
relativo (quanto o município cresceu além do esperado pela dinâmica nacional do
setor), não um estoque físico. Desempenho relativo é mais idiossincrático que
volume: municípios vizinhos compartilham a base produtiva, mas não
necessariamente a mesma trajetória competitiva. O sinal espacial existe, mas é
mais fraco — e isso é um achado, não um defeito do pipeline.

### 2.3 LISA univariado — onde estão os clusters

Foram encontrados **264 pares (município, subclasse) Alto-Alto significativos**,
distribuídos em **69 municípios distintos**. Distribuição dos quadrantes
significativos: Baixo-Baixo 2.775 · Baixo-Alto 1.325 · Alto-Baixo 525 ·
Alto-Alto 264.

Municípios que mais aparecem em clusters Alto-Alto:

| Município | Nº de subclasses AA |
|---|---|
| União | 30 |
| Altos | 28 |
| José de Freitas | 24 |
| Teresina | 13 |
| Batalha | 12 |
| Barras | 11 |
| Luís Correia | 10 |
| Baixa Grande do Ribeiro | 9 |
| Demerval Lobão | 9 |
| Cajueiro da Praia | 7 |

Emergem **três aglomerações geográficas nítidas** — as duas primeiras já
conhecidas das versões anteriores, a terceira mais visível aqui:

**(a) Eixo norte Teresina–Cocais.** Teresina, Altos, União, José de Freitas,
Demerval Lobão, Nazária, Batalha, Barras, Lagoa Alegre, Miguel Alves, Piripiri.
Concentra o comércio varejista diversificado, serviços urbanos, educação e a
avicultura periurbana (*Criação de frangos para corte*: Altos, José de Freitas,
Nazária, Teresina — o cinturão avícola da região metropolitana).

**(b) Fronteira agrícola do sudoeste (Cerrado / MATOPIBA).** Baixa Grande do
Ribeiro, Ribeiro Gonçalves, Uruçuí, Bom Jesus, Currais, Palmeira do Piauí,
Santa Filomena, Gilbués, Monte Alegre do Piauí, Redenção do Gurguéia, Sebastião
Leal, Alvorada do Gurguéia. É o cluster dos grãos e da pecuária:

* *Cultivo de soja* AA → Alvorada do Gurguéia, Antônio Almeida, Palmeira do Piauí, Sebastião Leal, Uruçuí
* *Cultivo de arroz* AA → Bom Jesus, Currais, Gilbués, Monte Alegre do Piauí, Palmeira do Piauí, Redenção do Gurguéia
* *Criação de bovinos para corte* AA → Baixa Grande do Ribeiro, Bom Jesus, Currais, Monte Alegre do Piauí, Redenção do Gurguéia, Ribeiro Gonçalves

**(c) Litoral / Delta do Parnaíba.** Parnaíba, Luís Correia, Cajueiro da Praia.
Aparece com força na subclasse *Hotéis* (2º maior I de Moran de toda a análise) e
em *Restaurantes e similares* — um cluster turístico que o CE + RIE identifica
melhor que o *Estoque*, porque capta a **dinâmica** de crescimento do setor, não
seu tamanho absoluto.

### 2.4 Moran bivariado — co-localização

Foram avaliados **2.657 pares** de subclasses (co-presentes em ≥ 5 municípios),
nos dois sentidos. **488 pares** são significativos em ambos os sentidos.
O I bivariado é direcional — I(A, B) mede a associação entre A no município e a
média de B nos vizinhos — por isso reportamos `I_AB`, `I_BA` e o `I_medio`, que
é o critério de ordenação.

| # | Subclasse A | Subclasse B | Munic. em comum | I médio |
|---|---|---|---|---|
| 1 | Criação de bovinos para corte | Cultivo de arroz | 7 | 0,196 |
| 2 | Criação de bovinos para corte | Cultivo de soja | 5 | 0,179 |
| 3 | Com. de equipamentos de informática | Criação de bovinos para corte | 7 | 0,155 |
| 4 | Formação de condutores | Serviços de escritório e apoio adm. | 5 | 0,150 |
| 5 | Comércio varejista de GLP | Criação de frangos para corte | 6 | 0,148 |
| 6 | Atividades de contabilidade | Criação de bovinos para corte | 10 | 0,146 |
| 7 | Cerâmica e barro cozido p/ construção | Restaurantes e similares | 5 | 0,144 |
| 8 | Com. de animais vivos e pet shop | Obras de urbanização | 6 | 0,142 |
| 9 | Supermercados | Cerâmica e barro cozido p/ construção | 5 | 0,141 |
| 10 | Apoio à agricultura | Criação de bovinos para corte | 10 | 0,141 |

O padrão dominante é claro: **o agronegócio do sudoeste puxa seus serviços de
apoio**. Bovinos aparece emparelhado com arroz, soja, atividades de apoio à
agricultura, medicamentos veterinários, contabilidade, informática e construção
de rodovias — a assinatura clássica de um complexo agroindustrial em que o setor
produtivo e sua cadeia de serviços crescem juntos e em municípios vizinhos.

O segundo padrão é a **cadeia avícola periurbana** de Teresina: *Criação de
frangos para corte* co-localiza com GLP, bebidas, pet shop e lanchonetes.

Os municípios mais frequentes em clusters bivariados Alto-Alto são José de
Freitas (11), Teresina (8), Altos (8), Baixa Grande do Ribeiro (7) e Demerval
Lobão (7) — a mesma dupla de polos.

---

## 3. Comparação com as versões anteriores

| | Binária | *Estoque* | **CE + RIE (esta)** |
|---|---|---|---|
| Variável | presença/ausência | `Estoque_mun_ano_final` (log1p) | `CE + RIE` (log1p) |
| O que mede | existência da potencialidade | magnitude física / de emprego | **desempenho competitivo relativo** |
| Força do sinal espacial | baixa | alta | **intermediária/baixa** |
| Hotspots | Teresina, sudoeste | Teresina, sudoeste | Teresina, sudoeste, **+ litoral** |

As três leituras convergem nos dois eixos estruturais (norte metropolitano e
fronteira do Cerrado), o que reforça a robustez do achado. A contribuição
específica desta versão é (i) o **litoral turístico** aparecer como cluster
próprio, e (ii) a evidência de que a **dinâmica competitiva é menos
espacialmente correlacionada que o estoque** — vizinhos compartilham vocação,
mas não necessariamente sucesso.

---

## 4. Ressalvas

* CE + RIE mede variação relativa entre `ANO_T0` e 2025, não nível. Um município
  pequeno com base minúscula pode exibir CE + RIE alto.
* A regra do máximo entre janelas seleciona, por construção, a janela mais
  favorável de cada potencialidade — é uma leitura de **potencial máximo
  observado**, não de desempenho médio.
* A massa de CE + RIE é dominada por subclasses de emprego público (RAIS), que
  não são potencialidades de mercado no sentido estrito.
* O I de Moran bivariado é direcional; ver §2.4.
* Pares com poucos municípios em comum (5–7) produzem I bivariados instáveis;
  trate o ranking do topo como indicativo, não como estimativa pontual.

---

## 5. Arquivos gerados

```
data_shiftshare/
  shiftshare_long_ce_rie.csv            3.920 pares vencedores (com CE, RIE, ANO_T0)
  ce_rie_matrix_raw.csv                 matriz 224 × 650 (CE + RIE bruto)
  ce_rie_matrix_log.csv                 matriz log1p, usada nas estatísticas
  subclasse_summary_ss.csv              cobertura e valores por subclasse
  global_moran_by_subclasse_ss.csv      Moran global + contagem de quadrantes
  lisa_hh_clusters_ss.csv               municípios Alto-Alto significativos
  lisa_all_significant_ss.csv           todos os LISA significativos
  bivariate_moran_pairs_ss.csv          2.657 pares + I bivariado nos dois sentidos
  multivariate_hh_ll_clusters_ss.csv    clusters AA/BB dos 20 pares mapeados
  top20_pairs_ss.csv                    os 20 pares mapeados
  pi_municipios_ibge.gpkg               malha IBGE, 224 municípios
figures_shiftshare/
  sintese_hotspots_ss.png               nº de subclasses AA por município
  overview_univariate_lisa_ss.png       montagem dos 6 maiores I
  overview_bivariate_lisa_ss.png        montagem dos 6 maiores pares
  univariate_lisa/uni_01..12_*_ss.png
  bivariate_lisa/biv_01..20_*_ss.png
scripts/
  spatial_utils_ss.py                   malha, pesos Queen, normalização de nomes
  S01_build_shiftshare_matrix.py        filtro T1/T2, CE+RIE, regra do máximo
  S02_univariate_lisa_ss.py             Moran global + LISA
  S03_multivariate_spatial_ss.py        Moran bivariado + LISA bivariado
  S04_generate_maps_ss.py               mapas
```
