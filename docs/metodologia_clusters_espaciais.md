# MAPA DE POTENCIALIDADES ECONÔMICAS DO PIAUÍ

**Nota metodológica: identificação de aglomerações (*clusters*) espaciais de potencialidades e análises de robustez**

---

## Resumo

Esta nota descreve o arcabouço teórico, as definições operacionais e as formulações matemáticas empregadas na identificação de aglomerações (*clusters*) espaciais de potencialidades econômicas nos 224 municípios do Piauí. A intensidade da potencialidade de cada par município–subclasse é mensurada por componentes da decomposição estrutural-diferencial (*shift-share*), no recorte tipológico T1+T2 de Montanía *et al.* (2024). A dimensão espacial é tratada por Análise Exploratória de Dados Espaciais (AEDE): I de Moran global, Indicadores Locais de Associação Espacial (LISA) e sua extensão bivariada, com inferência por permutações condicionais. Esta versão amplia a nota anterior com (i) a especificação da transformação sinalizada da variável CE + RIE; (ii) a validação da rotina vetorizada do Moran bivariado contra a implementação de referência; (iii) uma análise de robustez do padrão espacial a cinco especificações da matriz de vizinhança — contiguidade *Queen*, k vizinhos mais próximos, distância inversa, rede rodoviária real (Dijkstra) e tempo de viagem (OpenRouteService); e (iv) o controle de comparações múltiplas pela Taxa de Falsas Descobertas (FDR) de Benjamini–Hochberg.

**Palavras-chave:** Autocorrelação espacial. LISA. I de Moran. Matriz de pesos espaciais. Taxa de falsas descobertas. Piauí.

---

## 1 INTRODUÇÃO

A identificação de potencialidades econômicas regionais raramente pode prescindir da dimensão espacial. Atividades produtivas não se distribuem aleatoriamente no território: cadeias produtivas, dotações de recursos naturais, infraestrutura logística e transbordamentos de conhecimento (*spillovers*) produzem padrões de concentração geográfica. Dessa constatação decorre a necessidade de instrumentos capazes de distinguir, estatisticamente, um agrupamento espacial genuíno de um arranjo compatível com a aleatoriedade.

O presente documento detalha os procedimentos adotados para a construção dos mapas de *clusters* espaciais que integram o painel de potencialidades e, adicionalmente, as análises de robustez conduzidas para qualificar a leitura desses resultados. O objetivo não é descrever o *software*, mas explicitar as decisões teóricas e formais que sustentam os achados, de modo a permitir sua replicação e crítica. Em relação à versão anterior desta nota, acrescentam-se três blocos metodológicos: o tratamento formal de variáveis com valores negativos (seção 3.4), a bateria de robustez à especificação da matriz de vizinhança (seção 8) e o controle de multiplicidade por FDR (seção 9).

---

## 2 FUNDAMENTAÇÃO TEÓRICA

### 2.1 Dependência espacial e a Primeira Lei da Geografia

O ponto de partida é a formulação de Tobler (1970, p. 236), segundo a qual tudo está relacionado a tudo o mais, mas coisas próximas estão mais relacionadas do que coisas distantes. Essa proposição tem consequências estatísticas severas: viola o pressuposto de independência das observações que sustenta grande parte da inferência clássica. Anselin (1988) distingue dois efeitos espaciais:

a) **dependência espacial** (ou autocorrelação espacial): o valor de uma variável em uma unidade *i* é sistematicamente associado ao valor da mesma variável nas unidades vizinhas de *i*;

b) **heterogeneidade espacial**: instabilidade dos parâmetros e das formas funcionais ao longo do espaço, de modo que relações estimadas globalmente não valem uniformemente em todas as sub-regiões.

A análise de *clusters* aqui empregada explora o primeiro efeito, tratando o segundo como motivação para o uso de estatísticas *locais* em vez de exclusivamente globais.

### 2.2 Do global ao local

Estatísticas globais, como o I de Moran (MORAN, 1950; CLIFF; ORD, 1973), respondem a uma única pergunta: *existe* autocorrelação espacial no conjunto do território? Elas não informam *onde* ela ocorre. Como a média global pode mascarar padrões locais divergentes — inclusive compensações entre aglomerações positivas e negativas —, Anselin (1995) propôs a classe dos Indicadores Locais de Associação Espacial (LISA), que decompõem a estatística global em contribuições municipais individuais e permitem inferência específica para cada unidade. É essa decomposição que fundamenta os mapas de *clusters* do painel.

---

## 3 BASE DE DADOS E VARIÁVEIS

### 3.1 Unidades de análise e malha territorial

A unidade de análise é o município. Adotou-se a Malha Municipal Digital do Brasil — recorte 2025 (IBGE, 2025), restrita ao Piauí, contemplando os 224 municípios do estado, com sistema de referência SIRGAS 2000 (EPSG:4674), padrão oficial do IBGE. Registra-se, por sua relevância operacional, que espelhos não oficiais da malha apresentaram-se incompletos, omitindo o município de Nazária; o uso da malha oficial é, portanto, condição necessária à integridade do conjunto de vizinhanças. O pareamento entre a base econômica e a malha foi realizado pelo código IBGE do município, com normalização de nomes apenas como verificação secundária.

### 3.2 A variável de intensidade: componentes da decomposição *shift-share*

O painel opera dois *pipelines* paralelos. No *pipeline* de estoques, a intensidade é o estoque produtivo consolidado do par município–subclasse (variável `Estoque_mun_ano_final`), oriundo das pesquisas PAM, PPM e PEVS do IBGE e da RAIS do MTE. No *pipeline* *shift-share*, a intensidade deriva da decomposição estrutural-diferencial, cuja formulação clássica remonta a Dunn (1960), com a reinterpretação de Esteban-Marquillas (1972) e a sistematização brasileira de Haddad (1989). Seguindo a tipologia de Montanía *et al.* (2024), o crescimento do estoque de uma atividade *k* no município *i* é decomposto em efeitos intrínsecos, dos quais interessam aqui o efeito competitivo (**CE**), que mede a vantagem do município na atividade *k* frente ao desempenho nacional dessa atividade, e o efeito de reestruturação intraeconômica (**RIE**), que mede o peso e a dinâmica da atividade *k* dentro da economia do próprio município. A variável de intensidade do *pipeline* *shift-share* é a soma dos dois:

$$x_i^{k} \;=\; CE_i^{k} + RIE_i^{k} \tag{1}$$

A soma expressa uma **potencialidade efetiva** — competitividade da atividade combinada à sua relevância estrutural no município —, e não uma vantagem relativa descolada de massa econômica. Exclui-se deliberadamente o efeito de reestruturação sistêmica (RSE), que descreve a economia municipal como um todo, e não a atividade específica. Todo o mapa físico de potencialidades restringe-se ao recorte tipológico T1+T2 (setores com vantagem competitiva).

### 3.3 Deduplicação

Como um mesmo par município–subclasse pode aparecer em mais de uma janela temporal de comparação (comparações com anos iniciais de 2013, 2018 e 2022), adotou-se a regra: preserva-se a observação com o **maior valor da variável de intensidade** (Estoque no *pipeline* de estoques; CE + RIE no *shift-share*), e não a observação mais recente. A opção é coerente com o objetivo do estudo — mapear *potencialidades*, isto é, o melhor desempenho demonstrado pela atividade ao longo do período, e não sua situação conjuntural mais recente.

### 3.4 Transformações das variáveis de intensidade

Distribuições de estoque e de componentes de *shift-share* são fortemente assimétricas à direita. Como o I de Moran é baseado em produtos cruzados de desvios padronizados, é sensível a *outliers* extremos, que podem dominar o somatório. As transformações diferem conforme o suporte da variável.

Para o estoque, variável estritamente não negativa, aplica-se a transformação *log1p*, que preserva o zero (municípios sem a atividade permanecem em zero), comprime a cauda superior e dispensa o deslocamento arbitrário exigido pelo logaritmo simples:

$$y_i \;=\; \ln(1 + x_i) \tag{2}$$

A variável CE + RIE, por sua vez, assume valores negativos em cerca de 62% das observações — o que inviabiliza o *log1p* direto. Emprega-se, então, a **transformação logarítmica sinalizada**, que preserva o sinal econômico da variação (crescimento *vs.* retração) e comprime magnitudes de forma simétrica em torno de zero:

$$y_i \;=\; \operatorname{sinal}(x_i)\cdot \ln(1 + |x_i|) \tag{3}$$

A função é ímpar, contínua e monótona: mantém a ordenação econômica das observações, atenua as caudas em ambos os lados e fixa o zero em zero. Toda a análise subsequente opera sobre a variável padronizada (escore-z):

$$z_i \;=\; \frac{y_i - \bar{y}}{s_y} \tag{4}$$

---

## 4 AS MATRIZES DE PESOS ESPACIAIS

### 4.1 Definição

Toda estatística de autocorrelação espacial exige uma definição prévia e explícita de vizinhança, formalizada na matriz **W**, de dimensão *n* × *n* (*n* = 224), cujo elemento genérico $w_{ij}$ expressa a intensidade da conexão entre as unidades *i* e *j*, com $w_{ii} = 0$ por convenção. O defasado espacial (*spatial lag*) de uma variável *z* na unidade *i* é a combinação ponderada dos valores dos vizinhos:

$$(\mathbf{W}\mathbf{z})_i \;=\; \sum_j w_{ij}\, z_j \tag{5}$$

Todas as matrizes descritas a seguir são padronizadas por linha, de modo que $\sum_j w_{ij} = 1$ para todo *i*; o defasado espacial passa a ser interpretável como a média (ponderada) dos valores dos vizinhos, conferindo comparabilidade entre municípios com números distintos de vizinhos — atributo essencial em um estado de forte heterogeneidade no formato e na área dos polígonos.

### 4.2 Contiguidade *Queen* (especificação de referência)

A especificação de referência é a contiguidade *Queen* (rainha), pela qual dois municípios são vizinhos se compartilham **qualquer** ponto de fronteira — um segmento de aresta ou um único vértice:

$$w_{ij}^{*} = \begin{cases} 1, & \text{se } \partial A_i \cap \partial A_j \neq \varnothing \text{ e } i \neq j\\ 0, & \text{caso contrário} \end{cases} \tag{6}$$

A escolha da contiguidade *Queen* (em detrimento da *Rook*, que exige aresta comum) é a convenção usual em malhas municipais irregulares, nas quais imprecisões de digitalização podem transformar arestas curtas em vértices, gerando exclusões arbitrárias de vizinhança (ANSELIN; SYABRI; KHO, 2006). A vizinhança média sob *Queen* é de 5,4 municípios.

### 4.3 Padronização por linha

A matriz binária (ou de pesos brutos) é normalizada por linha:

$$w_{ij} \;=\; \frac{w_{ij}^{*}}{\sum_j w_{ij}^{*}} \tag{7}$$

### 4.4 Especificações geométricas alternativas (KNN e distância inversa)

A definição de vizinhança não é neutra. Para dimensionar essa sensibilidade, construíram-se duas matrizes geométricas alternativas, mantidos inalterados os demais parâmetros. A primeira é a de **k vizinhos mais próximos** (k = 5), calculada sobre os centroides municipais em projeção métrica (SIRGAS 2000 / Brazil Polyconic, EPSG:5880), na qual $w_{ij}^{*} = 1$ se *j* está entre os cinco municípios mais próximos de *i*, e 0 caso contrário. Por construção, a relação de vizinhança KNN não é simétrica antes da padronização. A segunda é a de **distância inversa**, com peso proporcional ao inverso da distância euclidiana entre centroides:

$$w_{ij}^{*} = \begin{cases} 1/d(i,j), & \text{se } d(i,j) \leq b\\ 0, & \text{caso contrário} \end{cases} \tag{8}$$

A banda *b* foi fixada em 76,5 km, o menor limiar que assegura ao menos um vizinho a cada município (grafo conexo, sem municípios-ilha), resultando em vizinhança média de 17,3 municípios — mais de três vezes a da contiguidade *Queen*. Vizinhanças mais densas suavizam o defasado espacial e diluem aglomerados pequenos, o que antecipa uma concordância menor com a linha de base.

### 4.5 Matriz de vizinhança rodoviária (rede real, Dijkstra)

As três matrizes anteriores são geométricas: pressupõem que a interação econômica se dá por adjacência ou por proximidade em linha reta. Para converter essa hipótese em medida empírica de acessibilidade, construiu-se uma matriz de vizinhança sobre a malha rodoviária real do estado. A malha foi montada a partir dos arquivos de rodovias estaduais e federais do Piauí, excluídos os trechos federais com situação "Planejada" (não construídos) e mantidos os pavimentados e em leito natural — 733 trechos e 13,9 mil km. A rede foi nodada nas interseções, densificada a cada 2 km e convertida em grafo ponderado (54.605 nós; 62.560 arestas, ponderadas pelo comprimento do segmento); 99,8% dos nós pertencem ao componente conexo gigante, adotado como rede de referência. Cada sede municipal foi conectada ao nó mais próximo por uma "perna de acesso" euclidiana (média de 5,4 km), registrando-se que onze sedes distam mais de 20 km de rodovia mapeada — informação relevante para a agenda de conectividade.

A distância rodoviária entre duas sedes *i* e *j* é o caminho de custo mínimo no grafo, calculado pelo algoritmo de Dijkstra (DIJKSTRA, 1959):

$$d_{\text{rede}}(i,j) \;=\; \min_{\pi \in \Pi(i,j)} \sum_{(u,v)\in\pi} \ell(u,v) \tag{9}$$

em que $\Pi(i,j)$ é o conjunto de caminhos entre *i* e *j* e $\ell(u,v)$ é o comprimento da aresta $(u,v)$. A matriz W-rede usa pesos $1/d_{\text{rede}}$ sobre a banda mínima que garante ao menos um vizinho a cada município (107,9 km de distância rodoviária), com padronização por linha (vizinhança média de 12,8). A razão mediana entre distância rodoviária e euclidiana (circuidade) é de 1,40, com correlação de 0,972 entre as duas métricas: no Piauí, a topologia viária acompanha em larga medida a geografia. As divergências localizadas — municípios de alta circuidade ou acesso precário — são justamente os casos em que *Queen* e a distância euclidiana superestimam a vizinhança efetiva.

### 4.6 Matriz de tempo de viagem (OpenRouteService)

Como quinta especificação, construiu-se uma matriz de tempos de viagem entre as sedes a partir da *Matrix API* do OpenRouteService (perfil *driving-car*, base OpenStreetMap), extraída localmente pelo pesquisador. A matriz retornou tempos válidos para 24.090 dos 24.976 pares. Quatro municípios (Dom Inocêncio, Socorro do Piauí, Valença do Piauí e Passagem Franca do Piauí) tiveram as sedes ancoradas em trechos não roteáveis do OSM e foram imputados pela relação tempo–distância ajustada nos pares válidos sobre a malha rodoviária oficial:

$$t(i,j) \;=\; 2{.}193 + 46{,}4 \cdot d_{\text{rede}}(i,j) \qquad (\text{segundos};\; d \text{ em km};\; R^2 = 0{,}933) \tag{10}$$

A regressão implica velocidade de percurso de aproximadamente 78 km/h. Diagnósticos de validação cruzada: correlação de 0,968 entre as distâncias ORS/OSM e as distâncias da malha oficial DNIT/DER (validação mútua das fontes), circuidade mediana de 1,38 e assimetria direcional desprezível (0,1%), o que permitiu simetrizar a matriz. A W-tempo usa pesos $1/t$ sobre a banda mínima conexa de 133 minutos (vizinhança média de 21,2), padronizada por linha. Ressalva: os tempos do OSM são modelados a partir de atributos viários, não de tráfego observado.

**Quadro 1 — Síntese das cinco especificações da matriz de pesos espaciais**

| Especificação | Critério de vizinhança | Peso $w_{ij}^{*}$ | Vizinhos (média) |
|---|---|:---:|:---:|
| *Queen* (referência) | Fronteira compartilhada (aresta ou vértice) | 1 | 5,4 |
| KNN-5 | 5 centroides mais próximos (EPSG:5880) | 1 | 5,0 |
| Distância inversa | Euclidiana ≤ 76,5 km | 1/d | 17,3 |
| Rede rodoviária | Dijkstra na malha real ≤ 107,9 km | 1/d | 12,8 |
| Tempo de viagem | ORS/OSM ≤ 133 min | 1/t | 21,2 |

Fonte: elaboração própria. Todas as matrizes são padronizadas por linha; nenhuma produz municípios-ilha.

---

## 5 AUTOCORRELAÇÃO ESPACIAL GLOBAL

### 5.1 O I de Moran

Para cada subclasse produtiva, calcula-se o I de Moran global:

$$I \;=\; \frac{n}{S_0} \cdot \frac{\sum_i \sum_j w_{ij}\,(y_i - \bar{y})(y_j - \bar{y})}{\sum_i (y_i - \bar{y})^2}, \qquad S_0 = \sum_i\sum_j w_{ij} \tag{11}$$

Com **W** padronizada por linha, $S_0 = n$ e a expressão reduz-se à forma matricial compacta $I = \dfrac{\mathbf{z}^\top \mathbf{W}\mathbf{z}}{\mathbf{z}^\top\mathbf{z}}$. Sob a hipótese nula de aleatoriedade espacial, o valor esperado é $E[I] = -\dfrac{1}{n-1} \approx -0{,}0045$ para *n* = 224. Valores de *I* significativamente **superiores** a $E[I]$ indicam autocorrelação **positiva** (agrupamento); valores **inferiores** indicam autocorrelação **negativa** (padrão de xadrez, dispersão).

### 5.2 O diagrama de dispersão de Moran

Sob padronização por linha, o I de Moran é o coeficiente angular da regressão de **Wz** sobre **z**. O diagrama de dispersão correspondente, com **z** no eixo horizontal e **Wz** no vertical, particiona o espaço em quatro quadrantes que dão nome às tipologias de *cluster*.

**Quadro 2 — Quadrantes do diagrama de dispersão de Moran**

| Quadrante | $z_i$ | $(\mathbf{W}\mathbf{z})_i$ | Rótulo | Interpretação |
|:---:|:---:|:---:|---|---|
| I | > 0 | > 0 | Alto-Alto (AA) | Município forte cercado de fortes |
| II | < 0 | > 0 | Baixo-Alto (BA) | Fraco cercado de fortes (*outlier*) |
| III | < 0 | < 0 | Baixo-Baixo (BB) | Fraco cercado de fracos |
| IV | > 0 | < 0 | Alto-Baixo (AB) | Forte cercado de fracos (*outlier*) |

Fonte: elaboração própria, a partir de Anselin (1995). AA e BB indicam associação positiva; BA e AB, *outliers* espaciais.

---

## 6 INDICADORES LOCAIS DE ASSOCIAÇÃO ESPACIAL (LISA)

### 6.1 O I de Moran local

Anselin (1995) define, para cada município *i*:

$$I_i \;=\; z_i \sum_j w_{ij}\, z_j \;=\; z_i \cdot (\mathbf{W}\mathbf{z})_i \tag{12}$$

O indicador satisfaz a propriedade de decomposição que caracteriza a classe LISA: a soma dos indicadores locais é proporcional ao global, $I = \dfrac{1}{n}\sum_i I_i$. O sinal de $I_i$ identifica o tipo de associação (positiva nos quadrantes AA/BB; negativa em AB/BA), e o quadrante específico é determinado pelos sinais de $z_i$ e de $(\mathbf{W}\mathbf{z})_i$.

### 6.2 Inferência por permutações condicionais

A distribuição amostral de $I_i$ sob a hipótese nula não é conhecida de forma fechada confiável para amostras finitas e distribuições assimétricas. Adota-se a **aleatorização condicional**: fixa-se o valor $z_i$ observado no município *i* e permutam-se aleatoriamente os *n* − 1 valores restantes entre as demais unidades, recalculando-se $I_i$ a cada permutação. Repetindo-se *M* vezes, obtém-se uma distribuição de referência empírica, e o pseudo-valor-p é:

$$p_i \;=\; \frac{R_i + 1}{M + 1} \tag{13}$$

em que $R_i$ é o número de estatísticas simuladas tão ou mais extremas que a observada. Na produção dos mapas e nas estatísticas de concordância adotou-se **M = 999 permutações** e semente aleatória fixada em **42**, garantindo reprodutibilidade exata; o menor pseudo-valor-p alcançável é 1/1000 = 0,001.

### 6.3 Critérios de significância e de elegibilidade

Considerou-se significativo o *cluster* local com **p < 0,05**; municípios não significativos são representados como tal nos mapas, independentemente do quadrante. A estatística LISA perde sentido quando a variável é quase integralmente nula; por isso, somente subclasses presentes em **pelo menos 10 municípios** foram submetidas à avaliação univariada. Abaixo desse limiar, a variância é dominada pelo padrão de ausência, e os quadrantes tornam-se artefatos da esparsidade. O tratamento formal do risco de falsos positivos decorrente da aplicação do teste aos 224 municípios é objeto da seção 9.

---

## 7 ASSOCIAÇÃO ESPACIAL BIVARIADA

### 7.1 Motivação e formulação

O interesse analítico não se esgota em saber *onde* uma subclasse se aglomera; interessa saber *quais atividades se atraem espacialmente* — se a presença intensa de uma subclasse *k* em um município está associada à presença intensa de outra subclasse *l* em seus **vizinhos**. Essa é a assinatura estatística de complementaridades produtivas e de economias de aglomeração de escopo regional. O I de Moran local bivariado (ANSELIN; SYABRI; SMIRNOV, 2002) é definido como:

$$I_i^{kl} \;=\; z_i^{k} \sum_j w_{ij}\, z_j^{l} \;=\; z_i^{k} \cdot (\mathbf{W}\mathbf{z}^{l})_i \tag{14}$$

e sua contrapartida global, $I^{kl} = \dfrac{(\mathbf{z}^{k})^\top \mathbf{W}\mathbf{z}^{l}}{(\mathbf{z}^{k})^\top \mathbf{z}^{k}}$, em que $\mathbf{z}^{k}$ e $\mathbf{z}^{l}$ são os vetores padronizados (transformados) das subclasses *k* e *l*. Duas observações são essenciais à interpretação:

a) **a medida não é simétrica**: em geral $I^{kl} \neq I^{lk}$. A leitura é sempre "subclasse *k* no município *versus* subclasse *l* nos vizinhos"; a ordenação do par importa (os *tooltips* e textos do painel nomeiam ambas as variáveis e explicitam a direção do quadrante);

b) **a medida não é uma correlação espacializada de Pearson**: ela capta exclusivamente a componente cruzada e defasada, ignorando a correlação *in situ* entre *k* e *l* no mesmo município. Lee (2001) discute essa limitação; como o objetivo aqui é identificar transbordamentos de vizinhança, e não coexistência intramunicipal, a formulação de Anselin é a adequada.

### 7.2 Esquema de permutação e validação da rotina vetorizada

A inferência bivariada replica o esquema de permutação condicional da implementação de referência (`esda.Moran_BV`): a variável focal $\mathbf{z}^{k}$ é mantida fixa e a parceira $\mathbf{z}^{l}$ é permutada, com 999 permutações e semente 42. Dada a escala do problema (dezenas de milhares de pares ordenados), a rotina foi vetorizada para desempenho. Para assegurar que a otimização não introduziu viés, a implementação vetorizada foi **validada contra o pacote `esda`**: a divergência máxima do *I* observado ficou na ordem de $10^{-17}$ (precisão de máquina) e as diferenças de pseudo-valor-p mostraram-se compatíveis com o ruído de Monte Carlo. Essa verificação é registrada por transparência, em coerência com o princípio de usar pacotes consagrados como referência e documentar explicitamente qualquer vetorização própria.

### 7.3 Quadrantes e critérios operacionais

A classificação em quadrantes é análoga à do caso univariado, combinando o valor de *k* no município com o valor médio de *l* nos vizinhos: os *clusters* Alto-Alto bivariados indicam **complementaridade espacial positiva** e constituem o principal insumo para a leitura de arranjos produtivos potenciais. A inferência é idêntica à univariada (999 permutações, semente 42, p < 0,05), e exigiu-se um mínimo de **5 municípios com copresença** das duas subclasses do par para sua avaliação. No universo elegível, isso totaliza 92.020 pares ordenados (focal, parceira).

---

## 8 ROBUSTEZ À ESPECIFICAÇÃO DA MATRIZ DE VIZINHANÇA

### 8.1 Motivação e métrica de concordância

Por ser a definição de vizinhança uma decisão do analista, a estabilidade dos aglomerados frente a especificações alternativas de **W** é condição de credibilidade. Recalcularam-se os indicadores locais e o Moran bivariado global sob as quatro matrizes alternativas descritas nas seções 4.4 a 4.6 (KNN-5, distância inversa, rede rodoviária e tempo de viagem), mantidos inalterados os demais parâmetros (999 permutações condicionais, semente 42, p < 0,05). A concordância é medida sobre as observações significativas sob a linha de base *Queen*, adotando-se como critério de manutenção: no univariado, o mesmo quadrante e a significância sob a matriz alternativa; no bivariado global, a mesma significância e o mesmo sinal de *I*.

Formalmente, para o conjunto *S* das observações significativas sob *Queen*, a taxa de manutenção sob a matriz alternativa *m* é:

$$\tau_m \;=\; \frac{\bigl|\{\, o \in S : \text{classe}_m(o) = \text{classe}_{\text{Queen}}(o) \,\}\bigr|}{|S|} \tag{15}$$

O **núcleo robusto** é definido como a interseção das observações mantidas simultaneamente sob todas as matrizes alternativas consideradas — o critério mais exigente disponível para leitura confirmatória.

### 8.2 Resultados sob cinco especificações

A Tabela 1 consolida as taxas de manutenção do recorte T1+T2 sob as quatro matrizes alternativas e sob a interseção das quatro. A leitura confirma dois pontos. Primeiro, a matriz rodoviária comporta-se de forma muito próxima à distância inversa euclidiana (por exemplo, 46,1% contra 45,5% no univariado de estoques), coerente com a correlação de 0,972 entre as métricas; ela não é redundante, porém, pois converte a hipótese de adjacência em medida empírica de acessibilidade. Segundo, a matriz de tempo é a mais exigente das quatro no univariado, coerente com sua vizinhança mais densa e com o fato de penalizar trechos lentos que a distância pura não captura.

**Tabela 1 — Manutenção das observações significativas sob *Queen*, por especificação de W (recorte T1+T2)**

| Pipeline / análise | Sig. *Queen* | KNN-5 | Dist. inversa | Rede rodov. | Tempo | 4 alt. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Estoque — univariado | 5.991 | 57,7% | 45,5% | 46,1% | 40,7% | 20,9% |
| Estoque — bivariado | 3.857 | 49,8% | 50,1% | 45,1% | 46,3% | 26,9% |
| CE + RIE — univariado | 5.065 | 67,4% | 37,2% | 39,5% | 32,0% | 14,3% |
| CE + RIE — bivariado | 2.061 | 37,8% | 32,1% | 29,3% | 29,7% | 10,1% |

Fonte: elaboração própria. "4 alt." = observações mantidas simultaneamente sob KNN-5, distância inversa, rede rodoviária e tempo de viagem. Concordância medida com 999 permutações e semente 42.

A concordância global média por mapa (incluindo municípios não significativos) situa-se entre 76% e 89%, o que mostra que a divergência se concentra nas bordas dos aglomerados — onde a topologia de vizinhança mais importa. A leitura recomendada é, portanto, **estratificada**: um núcleo robusto, invariante à especificação de **W**, e uma camada sensível à topologia adotada, cuja interpretação exige cautela adicional. Com a incorporação do tempo de viagem, a ressalva estrutural fica restrita a fluxos efetivos de bens e pessoas e a vínculos funcionais não físicos, cuja modelagem demandaria dados de origem–destino.

---

## 9 CONTROLE DE COMPARAÇÕES MÚLTIPLAS (FDR)

### 9.1 O problema da multiplicidade

Como cada mapa LISA aplica 224 testes locais e o universo bivariado avalia 92.020 pares, o número esperado de falsos positivos ao nível nominal de 5% não é desprezível mesmo na ausência completa de estrutura espacial: no universo bivariado, seriam esperados cerca de 4.601 pares espuriamente significativos. Impõe-se, pois, uma correção para multiplicidade.

### 9.2 O procedimento de Benjamini–Hochberg

Adotou-se o controle da **Taxa de Falsas Descobertas** (FDR) — a proporção esperada de falsos positivos entre as descobertas — pelo procedimento de Benjamini e Hochberg (1995), aplicado a estatísticas locais de associação espacial conforme Castro e Singer (2006) e Anselin (2019). Ordenados os *m* pseudo-valores-p em ordem crescente, $p_{(1)} \leq p_{(2)} \leq \dots \leq p_{(m)}$, determina-se o maior índice *k* que satisfaz:

$$p_{(k)} \;\leq\; \frac{k}{m}\,\alpha \tag{16}$$

e rejeitam-se todas as hipóteses nulas associadas a $p_{(1)}, \dots, p_{(k)}$. Adotou-se $\alpha = 0{,}05$. O procedimento é uniformemente mais potente que a correção de Bonferroni (que controla a probabilidade de *qualquer* falso positivo, $p_{(k)} \leq \alpha/m$), sendo adequado ao caráter exploratório da AEDE.

### 9.3 Resolução de permutações exigida pelo FDR

Há um aspecto operacional relevante: com 999 permutações, o menor pseudo-valor-p alcançável é 0,001, insuficiente para a resolução exigida pelos limiares $\frac{k}{m}\alpha$ nas caudas do procedimento de Benjamini–Hochberg. Por isso, os pseudo-valores-p destinados à correção foram **recalculados com 9.999 permutações** (menor p alcançável: 0,0001). Trata-se de decisão puramente numérica, sem alteração conceitual do teste.

### 9.4 Resultados

Aplicada em duas escalas — dentro de cada mapa LISA e através do universo de pares —, a correção produz efeitos fortemente assimétricos entre *pipelines*, resumidos na Tabela 2.

**Tabela 2 — Sobrevivência à correção FDR de Benjamini–Hochberg (T1+T2, *Queen*, 9.999 permutações)**

| Análise | Sig. nominais | Sobreviventes ao FDR | Taxa |
|---|:---:|:---:|:---:|
| LISA univariado — Estoque | 6.042 | 4.032 | 66,7% |
| LISA univariado — CE + RIE | 5.118 | 3.870 | 75,6% |
| Moran bivariado global — Estoque | 3.915 | 1.792 (937 com I > 0) | 45,8% |
| Moran bivariado global — CE + RIE | 2.073 | 552 (238 com I > 0) | 26,6% |

Fonte: elaboração própria. Corte FDR do universo bivariado de estoques: p ≤ 0,00766. O recorte tipológico T1+T2 eleva substancialmente a sobrevivência em relação ao universo não classificado (10,3% e 4,2% nos casos correspondentes).

A leitura conjunta das seções 8 e 9 converge: os resultados do *pipeline* de estoques são majoritariamente robustos tanto à especificação de **W** quanto à multiplicidade, ao passo que os do *pipeline* *shift-share* — e sobretudo a camada bivariada — comportam-se como evidência exploratória de primeira triagem. A assimetria é esperada, pois CE + RIE mede componentes de variação (mais voláteis e sujeitos a ruído de janela temporal) sobre suporte municipal mais esparso, enquanto o estoque mede níveis acumulados. Recomenda-se que o painel sinalize, para cada aglomerado e cada par, sua pertença ou não ao núcleo robusto (invariante a **W** e sobrevivente ao FDR), preservando o restante como material de exploração.

---

## 10 PARÂMETROS CONSOLIDADOS

**Quadro 3 — Parâmetros consolidados do pipeline espacial**

| Parâmetro | Valor adotado |
|---|---|
| Unidades espaciais | 224 municípios do Piauí |
| Malha territorial | IBGE, Malha Municipal Digital 2025 |
| Sistema de referência | SIRGAS 2000 (EPSG:4674); projeção métrica EPSG:5880 |
| Variáveis de intensidade | Estoque (*pipeline* de estoques); CE + RIE (*pipeline shift-share*) |
| Deduplicação | Máximo da intensidade entre janelas (2013, 2018, 2022) |
| Transformação — estoque | *log1p*, seguida de padronização (escore-z) |
| Transformação — CE + RIE | log sinalizado, $\operatorname{sinal}(x)\cdot\ln(1+|x|)$, seguido de escore-z |
| Matrizes de pesos | *Queen* (referência); KNN-5; distância inversa; rede rodoviária; tempo (ORS) |
| Padronização de W | Por linha, em todas as matrizes |
| Permutações | 999 (mapas e concordância); 9.999 (FDR) |
| Semente aleatória | 42 |
| Significância nominal | p < 0,05 |
| Correção de multiplicidade | FDR de Benjamini–Hochberg, $\alpha = 0{,}05$ |
| Mínimo — LISA univariado | 10 municípios com presença da subclasse |
| Mínimo — LISA bivariado | 5 municípios com copresença do par |

Fonte: elaboração própria.

---

## 11 LIMITAÇÕES

**Problema da Unidade de Área Modificável (MAUP).** Os resultados são condicionados ao recorte municipal; agregações alternativas (microrregiões, territórios de desenvolvimento) poderiam produzir padrões distintos (OPENSHAW, 1984).

**Sensibilidade à especificação de W.** Conforme a seção 8, os aglomerados devem ser lidos em dois estratos: um núcleo robusto, invariante à especificação, e uma camada sensível à topologia de vizinhança. Para além das matrizes geométricas, testaram-se uma matriz rodoviária real e uma de tempo de viagem; os resultados sob a rodoviária aproximam-se dos da distância inversa (correlação de 0,972 entre as métricas; circuidade mediana de 1,40), indicando que, no Piauí, a topologia viária acompanha em larga medida a geografia — com exceções em municípios de acesso precário (onze sedes distam mais de 20 km de rodovia mapeada). Permanecem fora do escopo os fluxos efetivos de bens e pessoas e os vínculos funcionais não físicos, cuja modelagem demandaria dados de origem–destino.

**Comparações múltiplas.** Conforme a seção 9, o volume de testes torna o controle de multiplicidade indispensável. Os aglomerados e pares que sobrevivem ao FDR constituem o subconjunto sobre o qual a evidência é mais defensável; os demais devem ser tratados como hipóteses a validar com dados e desenhos complementares. Nenhum par bivariado satisfaz o critério de Bonferroni na resolução de permutação adotada.

**Natureza dos dados de origem.** As fontes primárias (PAM, PPM e PEVS do IBGE; RAIS do MTE) têm coberturas, unidades de medida e regimes de sigilo distintos; a comparabilidade entre subclasses de fontes diferentes exige cautela — em especial entre atividades agropecuárias (volume ou valor da produção) e atividades formais urbanas (vínculos de emprego).

**Ausência ≠ zero.** O tratamento de subclasses não observadas como valor zero confunde, potencialmente, ausência real de atividade com ausência de registro (por sigilo ou informalidade), o que tende a subestimar a presença de atividades em municípios de pequeno porte.

**Tráfego não observado.** Os tempos de viagem do OpenRouteService são modelados a partir de atributos viários do OpenStreetMap, não de tráfego real; quatro municípios tiveram tempos imputados por regressão ($R^2 = 0{,}933$).

---

## REFERÊNCIAS

ANSELIN, Luc. **Spatial econometrics**: methods and models. Dordrecht: Kluwer Academic Publishers, 1988.

ANSELIN, Luc. Local indicators of spatial association — LISA. **Geographical Analysis**, Columbus, v. 27, n. 2, p. 93-115, 1995.

ANSELIN, Luc. A local indicator of multivariate spatial association: extending Geary's c. **Geographical Analysis**, Columbus, v. 51, n. 2, p. 133-150, 2019.

ANSELIN, Luc; SYABRI, Ibnu; KHO, Youngihn. GeoDa: an introduction to spatial data analysis. **Geographical Analysis**, Columbus, v. 38, n. 1, p. 5-22, 2006.

ANSELIN, Luc; SYABRI, Ibnu; SMIRNOV, Oleg. Visualizing multivariate spatial correlation with dynamically linked windows. In: ANSELIN, L.; REY, S. (org.). **New tools for spatial data analysis**. Santa Barbara: CSISS, University of California, 2002.

BENJAMINI, Yoav; HOCHBERG, Yosef. Controlling the false discovery rate: a practical and powerful approach to multiple testing. **Journal of the Royal Statistical Society**: Series B (Methodological), Londres, v. 57, n. 1, p. 289-300, 1995.

CASTRO, Marcia C.; SINGER, Burton H. Controlling the false discovery rate: a new application to account for multiple and dependent tests in local statistics of spatial association. **Geographical Analysis**, Columbus, v. 38, n. 2, p. 180-208, 2006.

CLIFF, Andrew D.; ORD, J. Keith. **Spatial autocorrelation**. Londres: Pion, 1973.

DIJKSTRA, Edsger W. A note on two problems in connexion with graphs. **Numerische Mathematik**, v. 1, n. 1, p. 269-271, 1959.

DUNN, Edgar S. A statistical and analytical technique for regional analysis. **Papers of the Regional Science Association**, v. 6, n. 1, p. 97-112, 1960.

ESTEBAN-MARQUILLAS, José M. A reinterpretation of shift-share analysis. **Regional and Urban Economics**, v. 2, n. 3, p. 249-255, 1972.

HADDAD, Paulo Roberto (org.). **Economia regional**: teorias e métodos de análise. Fortaleza: BNB/ETENE, 1989.

INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). **Malha municipal digital do Brasil**: 2025. Rio de Janeiro: IBGE, 2025.

LEE, Sang-Il. Developing a bivariate spatial association measure: an integration of Pearson's r and Moran's I. **Journal of Geographical Systems**, v. 3, n. 4, p. 369-385, 2001.

MORAN, Patrick A. P. Notes on continuous stochastic phenomena. **Biometrika**, Oxford, v. 37, n. 1-2, p. 17-23, 1950.

OPENSHAW, Stan. **The modifiable areal unit problem**. Norwich: Geo Books, 1984. (Concepts and Techniques in Modern Geography, 38).

REY, Sergio J.; ANSELIN, Luc. PySAL: a Python library of spatial analytical methods. **The Review of Regional Studies**, v. 37, n. 1, p. 5-27, 2007.

TOBLER, Waldo R. A computer movie simulating urban growth in the Detroit region. **Economic Geography**, v. 46, p. 234-240, 1970.

MONTANÍA, Claudia V. *et al.* [Título do trabalho]. [Periódico], [v.], [n.], [p.], 2024. *(referência a completar conforme a fonte primária adotada no projeto)*
