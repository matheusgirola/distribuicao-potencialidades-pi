# NOTA METODOLÓGICA: IDENTIFICAÇÃO DE CLUSTERS ESPACIAIS DE POTENCIALIDADES ECONÔMICAS NOS MUNICÍPIOS DO PIAUÍ

**Resumo** — Este documento descreve o arcabouço teórico, as definições operacionais e as formulações matemáticas empregadas na identificação de aglomerações (*clusters*) espaciais de potencialidades econômicas nos 224 municípios do estado do Piauí. A abordagem combina a análise estrutural-diferencial (*shift-share*) — utilizada para mensurar a intensidade da potencialidade de cada subclasse produtiva em cada município — com instrumentos de Análise Exploratória de Dados Espaciais (AEDE), notadamente o I de Moran global, os Indicadores Locais de Associação Espacial (LISA) e sua extensão bivariada. Descrevem-se a construção da matriz de vizinhança, as transformações das variáveis, o procedimento de inferência por permutações condicionais e os critérios de corte adotados.

**Palavras-chave:** Autocorrelação espacial. LISA. I de Moran. *Shift-share*. Desenvolvimento regional. Piauí.

---

## 1 INTRODUÇÃO

A identificação de potencialidades econômicas regionais raramente pode prescindir da dimensão espacial. Atividades produtivas não se distribuem aleatoriamente no território: cadeias produtivas, dotações de recursos naturais, infraestrutura logística e transbordamentos de conhecimento (*spillovers*) produzem padrões de concentração geográfica. Dessa constatação decorre a necessidade de instrumentos capazes de distinguir, estatisticamente, um agrupamento espacial genuíno de um arranjo compatível com a aleatoriedade.

O presente relatório detalha os procedimentos adotados para a construção dos mapas de *clusters* espaciais que integram o painel de potencialidades. O objetivo não é descrever o *software*, mas explicitar as decisões teóricas e formais que sustentam os resultados, de modo a permitir sua replicação e crítica.

---

## 2 FUNDAMENTAÇÃO TEÓRICA

### 2.1 Dependência espacial e a Primeira Lei da Geografia

O ponto de partida é a formulação de Tobler (1970, p. 236), segundo a qual tudo está relacionado a tudo o mais, mas coisas próximas estão mais relacionadas do que coisas distantes. Essa proposição, aparentemente trivial, tem consequências estatísticas severas: viola o pressuposto de independência das observações que sustenta grande parte da inferência clássica.

Anselin (1988) distingue dois efeitos espaciais:

a) **dependência espacial** (ou autocorrelação espacial): o valor de uma variável em uma unidade *i* é sistematicamente associado ao valor da mesma variável nas unidades vizinhas de *i*;

b) **heterogeneidade espacial**: instabilidade dos parâmetros e das formas funcionais ao longo do espaço, de modo que relações estimadas globalmente não valem uniformemente em todas as sub-regiões.

A análise de *clusters* aqui empregada explora justamente o primeiro efeito, tratando a segunda como motivação para o uso de estatísticas *locais* em vez de exclusivamente globais.

### 2.2 Do global ao local

Estatísticas globais, como o I de Moran (MORAN, 1950; CLIFF; ORD, 1973), respondem a uma única pergunta: *existe* autocorrelação espacial no conjunto do território? Elas não informam *onde* ela ocorre. Como a média global pode mascarar padrões locais divergentes — inclusive compensações entre aglomerações positivas e negativas —, Anselin (1995) propôs a classe dos Indicadores Locais de Associação Espacial (LISA), que decompõem a estatística global em contribuições municipais individuais e permitem inferência específica para cada unidade.

É essa decomposição que fundamenta os mapas de *clusters* apresentados no painel.

---

## 3 BASE DE DADOS E VARIÁVEIS

### 3.1 Unidades de análise e malha territorial

A unidade de análise é o município. Adotou-se a Malha Municipal Digital do Brasil — recorte 2025 (IBGE, 2025), restrita à Unidade da Federação Piauí, contemplando os **224 municípios** do estado. O sistema de referência geodésico é o SIRGAS 2000 (EPSG:4674), padrão oficial do IBGE.

Registra-se, por sua relevância operacional, que espelhos não oficiais da malha municipal disponíveis em repositórios públicos apresentaram-se incompletos, omitindo o município de Nazária (criado em 2009). O uso da malha oficial é, portanto, condição necessária à integridade do conjunto de vizinhanças.

O pareamento entre a base econômica e a malha foi realizado pelo código IBGE do município (`CD_MUN` → `cod_ibge`), com normalização de nomes (remoção de acentuação, caixa e espaços redundantes) apenas como verificação secundária.

### 3.2 A variável de intensidade: o componente estrutural-diferencial

A magnitude da potencialidade de cada par (município, subclasse) foi mensurada a partir da decomposição estrutural-diferencial (*shift-share*), cuja formulação clássica remonta a Dunn (1960) e cujas reinterpretações posteriores — em especial Esteban-Marquillas (1972) — buscaram isolar o efeito competitivo puro do efeito de composição. No Brasil, a técnica é sistematizada em Haddad (1989).

Seguindo a tipologia regional adotada no painel (MONTANÍA *et al.*, 2024), o crescimento do estoque de uma atividade *k* no município *i*, entre *t*₀ e *t*₁, é decomposto em efeitos intrínsecos, entre os quais interessam aqui:

- **CE** — efeito competitivo: mede a vantagem (ou desvantagem) do município na atividade *k* relativamente ao desempenho nacional dessa mesma atividade;
- **RIE** — efeito de reestruturação intra-econômica: mede o peso e a dinâmica da atividade *k* *dentro* da economia do próprio município;
- **RSE** — efeito de reestruturação sistêmica: mede o dinamismo da economia municipal frente à economia nacional.

A variável de intensidade utilizada na análise espacial é a soma dos dois primeiros componentes:

$$
x_{i}^{(k)} \;=\; CE_{i}^{(k)} \;+\; RIE_{i}^{(k)}
\tag{1}
$$

A justificativa é conceitual: CE capta a competitividade da atividade no município frente ao padrão nacional, e RIE capta o quanto essa atividade é estruturalmente relevante na economia municipal. A soma expressa, portanto, uma **potencialidade efetiva**, e não meramente uma vantagem relativa descolada de massa econômica. Deliberadamente exclui-se o RSE, que descreve a economia municipal como um todo e não a atividade específica.

### 3.3 Deduplicação

Como um mesmo par (município, subclasse) pode aparecer em mais de uma janela temporal de comparação (múltiplos valores de `ANO_T0`), adotou-se a seguinte regra: **preserva-se a observação com o maior valor de CE + RIE**, e não a observação mais recente. A opção é coerente com o objetivo do estudo — mapear *potencialidades*, isto é, o melhor desempenho demonstrado pela atividade no município ao longo do período observado, e não sua situação conjuntural mais recente.

### 3.4 Transformação da variável

Distribuições de estoque e de componentes de *shift-share* são fortemente assimétricas à direita, com concentração de valores próximos de zero e cauda longa (tipicamente Teresina e alguns polos regionais). Como o I de Moran é uma estatística baseada em produtos cruzados de desvios padronizados, é sensível a *outliers* extremos, que podem dominar o somatório. Aplicou-se, por isso, a transformação:

$$
y_{i}^{(k)} \;=\; \ln\!\left(1 + x_{i}^{(k)}\right)
\tag{2}
$$

A função *log1p* preserva o zero (municípios sem a atividade permanecem em zero), comprime a cauda superior e é definida em todo o domínio não negativo, dispensando o deslocamento arbitrário exigido pelo logaritmo simples.

Toda a análise subsequente opera sobre a variável padronizada:

$$
z_{i} \;=\; \frac{y_{i} - \bar{y}}{s_{y}}
\tag{3}
$$

---

## 4 A MATRIZ DE PESOS ESPACIAIS

### 4.1 Definição

Toda estatística de autocorrelação espacial exige uma definição prévia e explícita de "vizinhança", formalizada na matriz **W**, de dimensão *n* × *n* (*n* = 224), cujo elemento genérico *w*ᵢⱼ expressa a intensidade da conexão entre as unidades *i* e *j*, com *w*ᵢᵢ = 0 por convenção.

### 4.2 Critério de contiguidade *Queen*

Adotou-se o critério de contiguidade **Queen** (rainha), pelo qual dois municípios são vizinhos se compartilham **qualquer** ponto de fronteira — seja um segmento de aresta, seja um único vértice:

$$
w_{ij}^{*} =
\begin{cases}
1, & \text{se } \partial A_i \cap \partial A_j \neq \varnothing \text{ e } i \neq j\\[4pt]
0, & \text{caso contrário}
\end{cases}
\tag{4}
$$

onde ∂A denota a fronteira do polígono municipal. A escolha da contiguidade *Queen* (em detrimento da *Rook*, que exige aresta comum) é a convenção usual em malhas municipais irregulares, nas quais imprecisões de digitalização podem transformar arestas curtas em vértices, gerando exclusões arbitrárias de vizinhança (ANSELIN; SYABRI; KHO, 2006).

### 4.3 Padronização por linha

A matriz binária é normalizada por linha:

$$
w_{ij} \;=\; \frac{w_{ij}^{*}}{\sum_{j=1}^{n} w_{ij}^{*}}
\tag{5}
$$

de modo que $\sum_j w_{ij} = 1$ para todo *i*. A padronização torna o **defasado espacial** (*spatial lag*)

$$
\left(\mathbf{W}\mathbf{z}\right)_{i} \;=\; \sum_{j=1}^{n} w_{ij}\, z_{j}
\tag{6}
$$

interpretável como a **média dos valores padronizados dos vizinhos** de *i*, o que confere comparabilidade entre municípios com números distintos de fronteiriços — atributo essencial em um estado com forte heterogeneidade no formato e na área dos polígonos municipais.

---

## 5 AUTOCORRELAÇÃO ESPACIAL GLOBAL

### 5.1 O I de Moran

Para cada subclasse produtiva, calcula-se:

$$
I \;=\; \frac{n}{S_{0}} \cdot \frac{\displaystyle\sum_{i=1}^{n}\sum_{j=1}^{n} w_{ij}\,(y_i - \bar{y})(y_j - \bar{y})}{\displaystyle\sum_{i=1}^{n} (y_i - \bar{y})^{2}},
\qquad S_{0} = \sum_{i}\sum_{j} w_{ij}
\tag{7}
$$

Com **W** padronizada por linha, *S*₀ = *n*, e a expressão reduz-se à forma matricial compacta:

$$
I \;=\; \frac{\mathbf{z}^{\top}\mathbf{W}\mathbf{z}}{\mathbf{z}^{\top}\mathbf{z}}
\tag{8}
$$

Sob a hipótese nula de aleatoriedade espacial, o valor esperado é:

$$
E[I] \;=\; -\frac{1}{n-1}
\tag{9}
$$

que, para *n* = 224, equivale a aproximadamente −0,0045. Valores de *I* significativamente **superiores** a *E*[*I*] indicam autocorrelação espacial **positiva** (municípios com valores altos tendem a ser vizinhos de municípios com valores altos, e o mesmo para valores baixos — isto é, agrupamento); valores significativamente **inferiores** indicam autocorrelação **negativa** (padrão de xadrez, dispersão).

### 5.2 O diagrama de dispersão de Moran

O I de Moran, sob padronização por linha, é o coeficiente angular da regressão de **Wz** sobre **z**. O diagrama de dispersão correspondente, com **z** no eixo horizontal e **Wz** no vertical, particiona o espaço em quatro quadrantes que dão nome às tipologias de *cluster*:

| Quadrante | *z*ᵢ | (**Wz**)ᵢ | Rótulo | Interpretação |
|---|---|---|---|---|
| I | > 0 | > 0 | **Alto-Alto (AA)** | Município forte cercado de vizinhos fortes |
| II | < 0 | > 0 | **Baixo-Alto (BA)** | Município fraco cercado de vizinhos fortes (*outlier* espacial) |
| III | < 0 | < 0 | **Baixo-Baixo (BB)** | Município fraco cercado de vizinhos fracos |
| IV | > 0 | < 0 | **Alto-Baixo (AB)** | Município forte cercado de vizinhos fracos (*outlier* espacial) |

Os quadrantes I e III correspondem a associação espacial **positiva** (aglomerações); os quadrantes II e IV, a associação **negativa** (*outliers* espaciais, ou "ilhas").

---

## 6 INDICADORES LOCAIS DE ASSOCIAÇÃO ESPACIAL (LISA)

### 6.1 O I de Moran local

Anselin (1995) define, para cada município *i*:

$$
I_{i} \;=\; z_{i} \sum_{j=1}^{n} w_{ij}\, z_{j} \;=\; z_{i}\cdot(\mathbf{W}\mathbf{z})_{i}
\tag{10}
$$

O indicador satisfaz a propriedade de decomposição que caracteriza a classe LISA: a soma dos indicadores locais é proporcional ao indicador global,

$$
I \;=\; \frac{1}{n}\sum_{i=1}^{n} I_{i}
\tag{11}
$$

O sinal de *I*ᵢ identifica o tipo de associação: *I*ᵢ > 0 sinaliza similaridade com a vizinhança (quadrantes AA ou BB); *I*ᵢ < 0 sinaliza dissimilaridade (AB ou BA). O quadrante específico é determinado pelos sinais de *z*ᵢ e de (**Wz**)ᵢ, conforme o Quadro da seção 5.2.

### 6.2 Inferência por permutações condicionais

A distribuição amostral de *I*ᵢ sob a hipótese nula não é conhecida em forma fechada de maneira confiável para amostras finitas e distribuições assimétricas. Adota-se, portanto, a **aleatorização condicional**: fixa-se o valor *z*ᵢ observado no município *i* e permutam-se aleatoriamente os *n* − 1 valores restantes entre as demais unidades, recalculando-se *I*ᵢ a cada permutação. Repetindo-se o procedimento *M* vezes, obtém-se uma distribuição de referência empírica.

O pseudo-valor-p é calculado como:

$$
p_{i} \;=\; \frac{R_{i} + 1}{M + 1}
\tag{12}
$$

onde *R*ᵢ é o número de estatísticas simuladas tão ou mais extremas que a observada. Adotou-se **M = 999 permutações** e **semente aleatória fixada em 42**, o que assegura reprodutibilidade exata dos resultados. O menor pseudo-valor-p alcançável é, portanto, 1/1000 = 0,001.

### 6.3 Critério de significância e classificação

Considerou-se significativo o *cluster* local com **p < 0,05**. Municípios não significativos são representados como "não significativos" nos mapas, independentemente do quadrante em que se situem no diagrama de dispersão.

Cabe registrar a ressalva usual: como o teste é aplicado a cada um dos 224 municípios, o número esperado de falsos positivos sob a hipótese nula é da ordem de 0,05 × 224 ≈ 11 unidades. A literatura discute correções para comparações múltiplas, como o controle da taxa de falsas descobertas (BENJAMINI; HOCHBERG, 1995) ou a correção de Bonferroni. Optou-se pelo limiar convencional não corrigido, em coerência com o caráter **exploratório** da AEDE (ANSELIN, 1995), no qual os *clusters* identificados são tratados como **hipóteses a investigar**, e não como resultados confirmatórios. A interpretação substantiva prioriza, consequentemente, aglomerações contíguas e economicamente plausíveis, e não municípios isolados marginalmente significativos.

### 6.4 Critério de elegibilidade da subclasse

A estatística LISA perde sentido quando a variável é quase integralmente nula. Por isso, **somente subclasses presentes em pelo menos 10 municípios** foram submetidas à avaliação univariada. Abaixo desse limiar, a variância amostral é dominada pelo padrão de ausência, e os quadrantes tornam-se artefatos da esparsidade.

---

## 7 ASSOCIAÇÃO ESPACIAL BIVARIADA

### 7.1 Motivação

O interesse analítico não se esgota em saber onde uma subclasse se aglomera. Interessa saber quais atividades **se atraem espacialmente** — isto é, se a presença intensa de uma subclasse *k* em um município está associada à presença intensa de outra subclasse *l* em seus **vizinhos**. Essa é a assinatura estatística de complementaridades produtivas, encadeamentos de cadeia e economias de aglomeração de escopo regional.

### 7.2 Formulação

O I de Moran local bivariado (ANSELIN; SYABRI; SMIRNOV, 2002) é definido como:

$$
I_{i}^{kl} \;=\; z_{i}^{k} \sum_{j=1}^{n} w_{ij}\, z_{j}^{l} \;=\; z_{i}^{k}\cdot(\mathbf{W}\mathbf{z}^{l})_{i}
\tag{13}
$$

e sua contrapartida global:

$$
I^{kl} \;=\; \frac{(\mathbf{z}^{k})^{\top}\,\mathbf{W}\,\mathbf{z}^{l}}{(\mathbf{z}^{k})^{\top}\mathbf{z}^{k}}
\tag{14}
$$

onde **z**ᵏ e **z**ˡ são os vetores padronizados (log-transformados) da intensidade das subclasses *k* e *l*.

Duas observações são essenciais à interpretação correta:

a) **A medida não é simétrica**: *I*ᵏˡ ≠ *I*ˡᵏ em geral. A leitura é sempre "subclasse *k* em *i* versus subclasse *l* nos vizinhos de *i*". A ordenação do par importa;

b) **A medida não é uma correlação espacializada no sentido de Pearson**. Ela mede exclusivamente a componente *cruzada e defasada* da associação, ignorando a correlação *in situ* entre *k* e *l* no mesmo município. Lee (2001) discute limitações dessa formulação e propõe medidas alternativas que integram explicitamente a correlação local e a suavização espacial. Como o objetivo aqui é justamente identificar **transbordamentos de vizinhança**, e não coexistência intramunicipal, a formulação de Anselin é a adequada ao propósito.

### 7.3 Quadrantes bivariados

A classificação em quadrantes é análoga à do caso univariado, agora combinando o valor da subclasse *k* no município com o valor médio da subclasse *l* nos vizinhos:

- **Alto-Alto**: *k* intensa em *i*, *l* intensa no entorno → **complementaridade espacial positiva**;
- **Baixo-Baixo**: *k* fraca em *i*, *l* fraca no entorno → vazio produtivo conjunto;
- **Alto-Baixo** e **Baixo-Alto**: descompassos espaciais entre as duas atividades.

Os *clusters* Alto-Alto bivariados constituem o principal insumo para a leitura de **arranjos produtivos potenciais**.

### 7.4 Critérios operacionais

- Inferência idêntica à do caso univariado: **999 permutações**, semente **42**, limiar **p < 0,05**;
- Exigiu-se um mínimo de **5 municípios com copresença** das duas subclasses do par para que este fosse avaliado. Pares com sobreposição inferior produzem estatísticas instáveis e altamente sensíveis a observações individuais;
- Todos os pares que atenderam a esses critérios e resultaram significativos foram retidos — totalizando **1.544 mapas de *cluster* bivariados**, integralmente incorporados ao painel. A decisão de incorporar o conjunto completo, em vez de uma seleção dos pares mais fortes por subclasse, foi tomada após a mensuração do custo marginal de armazenamento, considerado desprezível frente ao ganho de completude analítica.

---

## 8 CLUSTERS ESPACIAIS MULTIVARIADOS

O mapa de *clusters* multivariados sintetiza, para cada município, a **multiplicidade de pertencimentos** a aglomerações Alto-Alto significativas ao longo do conjunto de subclasses avaliadas. Formalmente, define-se para o município *i* o indicador:

$$
M_{i} \;=\; \sum_{k \in \mathcal{K}} \mathbb{1}\!\left[\, q_{i}^{k} = \text{AA} \;\wedge\; p_{i}^{k} < 0{,}05 \,\right]
\tag{15}
$$

onde 𝒦 é o conjunto de subclasses elegíveis, *q*ᵢᵏ o quadrante LISA do município *i* na subclasse *k*, e 𝟙[·] a função indicadora.

*M*ᵢ mede, portanto, a **densidade de vocações espacialmente consolidadas** do município: valores elevados identificam territórios que integram simultaneamente diversas aglomerações produtivas — candidatos naturais a nós de polarização regional. Valores nulos identificam municípios que, ainda que possuam atividades, não participam de nenhuma aglomeração estatisticamente significativa, sinalizando isolamento produtivo relativo.

---

## 9 PARÂMETROS CONSOLIDADOS

| Parâmetro | Valor adotado |
|---|---|
| Unidades espaciais | 224 municípios do Piauí |
| Malha territorial | IBGE, Malha Municipal Digital 2025 |
| Sistema de referência | SIRGAS 2000 (EPSG:4674) |
| Variável de intensidade | CE + RIE (*shift-share*) |
| Regra de deduplicação | máximo de CE + RIE entre janelas `ANO_T0` |
| Transformação | log1p, seguida de padronização (escore-z) |
| Matriz de pesos | contiguidade *Queen*, padronizada por linha |
| Permutações | 999 |
| Semente aleatória | 42 |
| Nível de significância | p < 0,05 |
| Mínimo — LISA univariado | 10 municípios com presença da subclasse |
| Mínimo — LISA bivariado | 5 municípios com copresença do par |

---

## 10 LIMITAÇÕES

**Problema da Unidade de Área Modificável (MAUP).** Os resultados são condicionados ao recorte municipal. Agregações alternativas (microrregiões, territórios de desenvolvimento) poderiam produzir padrões distintos (OPENSHAW, 1984).

**Sensibilidade à especificação de W.** A definição de vizinhança não é neutra. A contiguidade *Queen* pressupõe que a interação econômica se dá por adjacência física, ignorando conectividade rodoviária, distância a mercados e vínculos funcionais não contíguos. Análises de robustez com matrizes alternativas (*k* vizinhos mais próximos, distância inversa) são recomendáveis.

**Comparações múltiplas.** Conforme a seção 6.3, o número esperado de falsos positivos não é desprezível, e o volume de pares bivariados avaliados amplifica essa preocupação. Reitera-se o caráter exploratório, e não confirmatório, dos resultados.

**Natureza dos dados de origem.** As fontes primárias (PAM, PPM e PEVS do IBGE; RAIS do MTE) têm coberturas, unidades de medida e regimes de sigilo distintos. A comparabilidade entre subclasses oriundas de fontes diferentes deve ser interpretada com cautela — especialmente entre atividades agropecuárias (medidas em volume ou valor da produção) e atividades formais urbanas (medidas em vínculos empregatícios).

**Ausência ≠ zero.** O tratamento de subclasses não observadas como valor zero confunde, potencialmente, ausência real de atividade com ausência de registro (por sigilo estatístico ou por informalidade), o que tende a subestimar a presença de atividades em municípios de pequeno porte.

---

## REFERÊNCIAS

ALMEIDA, Eduardo. **Econometria espacial aplicada**. Campinas: Alínea, 2012.

ANSELIN, Luc. **Spatial econometrics**: methods and models. Dordrecht: Kluwer Academic Publishers, 1988.

ANSELIN, Luc. Local indicators of spatial association — LISA. **Geographical Analysis**, Columbus, v. 27, n. 2, p. 93-115, 1995.

ANSELIN, Luc; SYABRI, Ibnu; KHO, Youngihn. GeoDa: an introduction to spatial data analysis. **Geographical Analysis**, Columbus, v. 38, n. 1, p. 5-22, 2006.

ANSELIN, Luc; SYABRI, Ibnu; SMIRNOV, Oleg. Visualizing multivariate spatial correlation with dynamically linked windows. In: ANSELIN, L.; REY, S. (org.). **New tools for spatial data analysis**: proceedings of the specialist meeting. Santa Barbara: Center for Spatially Integrated Social Science, University of California, 2002.

BENJAMINI, Yoav; HOCHBERG, Yosef. Controlling the false discovery rate: a practical and powerful approach to multiple testing. **Journal of the Royal Statistical Society**: Series B (Methodological), Londres, v. 57, n. 1, p. 289-300, 1995.

CLIFF, Andrew D.; ORD, J. Keith. **Spatial autocorrelation**. Londres: Pion, 1973.

DUNN, Edgar S. A statistical and analytical technique for regional analysis. **Papers of the Regional Science Association**, v. 6, n. 1, p. 97-112, 1960.

ESTEBAN-MARQUILLAS, José M. A reinterpretation of shift-share analysis. **Regional and Urban Economics**, v. 2, n. 3, p. 249-255, 1972.

GETIS, Arthur; ORD, J. Keith. The analysis of spatial association by use of distance statistics. **Geographical Analysis**, Columbus, v. 24, n. 3, p. 189-206, 1992.

HADDAD, Paulo Roberto (org.). **Economia regional**: teorias e métodos de análise. Fortaleza: BNB/ETENE, 1989.

INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). **Malha municipal digital do Brasil**: 2025. Rio de Janeiro: IBGE, 2025.

INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). **Produção Agrícola Municipal (PAM)**. Rio de Janeiro: IBGE, [s.d.].

INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). **Produção da Pecuária Municipal (PPM)**. Rio de Janeiro: IBGE, [s.d.].

INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). **Produção da Extração Vegetal e da Silvicultura (PEVS)**. Rio de Janeiro: IBGE, [s.d.].

LEE, Sang-Il. Developing a bivariate spatial association measure: an integration of Pearson's r and Moran's I. **Journal of Geographical Systems**, v. 3, n. 4, p. 369-385, 2001.

MONTANÍA, Claudia V. *et al.* [**Título do trabalho**]. [Periódico], [v.], [n.], [p.], 2024. *(referência a ser completada conforme a fonte primária adotada no projeto)*

MORAN, Patrick A. P. Notes on continuous stochastic phenomena. **Biometrika**, Oxford, v. 37, n. 1-2, p. 17-23, 1950.

OPENSHAW, Stan. **The modifiable areal unit problem**. Norwich: Geo Books, 1984. (Concepts and Techniques in Modern Geography, 38).

REY, Sergio J.; ANSELIN, Luc. PySAL: a Python library of spatial analytical methods. **The Review of Regional Studies**, v. 37, n. 1, p. 5-27, 2007.

TOBLER, Waldo R. A computer movie simulating urban growth in the Detroit region. **Economic Geography**, v. 46, p. 234-240, 1970.

---

**Dois pontos que você deve validar antes de circular o documento:**

1. **Seção 8 (clusters multivariados)** — descrevi a métrica como contagem de pertencimentos Alto-Alto significativos por município. Se o script implementa outra coisa (p. ex. K-means sobre os *z* das subclasses, ou SKATER/Max-p), me avise que reescrevo a seção com a formulação correta.
2. **Referência Montanía *et al.* (2024)** — não tenho a citação completa; deixei o campo marcado para você preencher.