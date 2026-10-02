# Revisão das Limitações 2 e 3 — Análises de Robustez

Este documento substitui as redações originais das limitações "Sensibilidade à especificação de W" e "Comparações múltiplas", incorporando os resultados de análises de robustez efetivamente conduzidas. A primeira parte traz os novos parágrafos, prontos para substituição direta no texto metodológico; a segunda parte é um anexo técnico (sugere-se numerá-lo como seção complementar à seção 6) documentando os procedimentos e resultados que fundamentam as novas redações.

---

## Parte 1 — Novas redações

### Limitação 2 (revisada): Sensibilidade à especificação de W

A definição de vizinhança não é neutra. A contiguidade Queen pressupõe que a interação econômica se dá por adjacência física, ignorando conectividade rodoviária, distância a mercados e vínculos funcionais não contíguos. Para quantificar o alcance dessa limitação, os indicadores locais foram recalculados sob duas especificações alternativas de W: k vizinhos mais próximos (k = 5) e distância inversa com banda de 76,5 km (menor limiar que garante grafo conexo entre os 224 municípios), mantidos inalterados os demais parâmetros (999 permutações condicionais, semente 42, p < 0,05). Os resultados indicam sensibilidade não desprezível. No pipeline de estoques, 68,5% das observações município–subclasse significativas sob Queen preservam o mesmo quadrante e a significância sob k-vizinhos, proporção que cai para 47,6% sob distância inversa; 39,0% resistem simultaneamente às duas especificações alternativas. No pipeline shift-share (CE + RIE), a estabilidade é menor: 51,8% sob k-vizinhos, 37,9% sob distância inversa e 27,7% sob ambas — reflexo do caráter mais ruidoso da variável de intensidade, que combina dois componentes de decomposição de variação. Na análise bivariada global, 17,9% dos pares significativos sob Queen permanecem significativos, com mesmo sinal, sob as duas matrizes alternativas. Conclui-se que os aglomerados espaciais identificados devem ser lidos em dois estratos: um núcleo robusto, invariante à especificação de W (documentado no Anexo, com listagem por subclasse), e uma camada sensível à topologia de vizinhança adotada, cuja interpretação exige cautela adicional. Permanece, ainda assim, a ressalva estrutural: nenhuma das três matrizes testadas incorpora conectividade rodoviária efetiva, tempos de deslocamento ou vínculos funcionais não contíguos, dimensões cuja modelagem demandaria matrizes de interação construídas a partir de dados de fluxo.

### Limitação 3 (revisada): Comparações múltiplas

Conforme a seção 6.3, o número esperado de falsos positivos não é desprezível, e o volume de pares bivariados avaliados amplifica essa preocupação: no universo de 92.020 pares testados, seriam esperados cerca de 4.601 pares espuriamente significativos ao nível nominal de 5% mesmo na ausência completa de estrutura espacial. Para dimensionar o problema, aplicou-se o controle da Taxa de Falsas Descobertas (FDR, procedimento de Benjamini–Hochberg, conforme Castro e Singer, 2006, e Anselin, 2019), com pseudo p-valores recalculados sob 9.999 permutações para viabilizar a resolução exigida pelo procedimento. Os efeitos são assimétricos entre pipelines e escalas de análise. No LISA univariado do pipeline de estoques, 71,5% das observações significativas sobrevivem à correção (16.045 de 22.433), e 373 das 380 subclasses mantêm ao menos um aglomerado — indício de que os padrões univariados de estoque são, em sua maioria, sinal e não artefato. No pipeline shift-share, apenas 10,3% sobrevivem (1.096 de 10.640), e o número de subclasses com aglomerado remanescente cai de 290 para 103. Na análise bivariada, a correção é ainda mais severa: dos 22.511 pares nominalmente significativos, 944 resistem ao FDR (dos quais 436 com associação espacial positiva), e nenhum resiste ao critério de Bonferroni. Reitera-se, portanto, o caráter exploratório, e não confirmatório, dos resultados — agora com uma gradação explícita: os aglomerados e pares que sobrevivem à correção FDR (listados no Anexo) constituem o subconjunto sobre o qual a evidência de associação espacial é mais defensável, ao passo que os demais devem ser tratados como hipóteses a validar com dados e desenhos complementares.

---

## Parte 2 — Anexo técnico: procedimentos e resultados das análises de robustez

### A.1 Dados e reconstrução da linha de base

As análises utilizaram a Malha Municipal Digital 2025 do IBGE (224 municípios do Piauí, EPSG:4674), a base consolidada de potencialidades (variável de intensidade: Estoque_mun_ano_final) e a base shift-share consolidada (variável de intensidade: CE + RIE). Nos dois casos, quando um par município–subclasse aparece em mais de uma janela temporal, manteve-se a observação de maior valor da variável de intensidade, conforme a regra de deduplicação do pipeline principal. A transformação aplicada foi log1p para estoques (variável não negativa) e, para CE + RIE — que assume valores negativos em 62% das observações —, a transformação logarítmica sinalizada, sinal(x) · log1p(|x|), que preserva o sinal econômico da variação e comprime magnitudes de forma simétrica. Foram elegíveis para a análise univariada as subclasses presentes em ao menos 10 municípios (380 no pipeline de estoques; 290 no shift-share); para a bivariada, pares ordenados (focal, parceira) com ao menos 5 municípios de copresença, totalizando 92.020 pares.

Registra-se uma ressalva de reprodutibilidade: os scripts originais do pipeline não estavam disponíveis nesta sessão de análise, de modo que a linha de base Queen foi reconstruída a partir dos parâmetros documentados na metodologia. A reconstrução produz um universo de pares bivariados significativos maior que o conjunto de 1.544 mapas incorporado ao painel, o que indica que o painel adotou critério de seleção mais restritivo (a combinação p < 0,01, I > 0 e copresença ≥ 10 produz contagem próxima, 1.490 pares). As estatísticas de concordância e de sobrevivência ao FDR aqui reportadas referem-se ao universo reconstruído e devem ser lidas como proporções, aplicáveis com boa aproximação a qualquer subconjunto dele.

### A.2 Especificações de W

Três matrizes de pesos espaciais foram construídas, todas padronizadas por linha: (i) contiguidade Queen (linha de base; média de 5,4 vizinhos); (ii) k vizinhos mais próximos com k = 5, calculados sobre centroides em projeção métrica (SIRGAS 2000 / Brazil Polyconic, EPSG:5880); e (iii) distância inversa (peso 1/d) com banda de 76,5 km, correspondente à menor distância limiar que assegura ao menos um vizinho a cada município (média de 17,3 vizinhos). Nenhuma das três especificações produz municípios-ilha.

### A.3 Robustez do LISA univariado à especificação de W

Para cada subclasse elegível e cada matriz, o I de Moran local foi computado com 999 permutações condicionais (esda.Moran_Local, semente 42) e cada município classificado em Alto-Alto, Baixo-Baixo, Alto-Baixo, Baixo-Alto ou não significativo (p ≥ 0,05). A tabela seguinte resume a concordância em relação à linha de base Queen, medida sobre as observações município–subclasse significativas sob Queen.

| Pipeline | Sig. sob Queen | Mesmo quadrante sob KNN-5 | Mesmo quadrante sob dist. inversa | Confirmados sob ambas |
|---|---|---|---|---|
| Estoque | 22.351 | 15.317 (68,5%) | 10.636 (47,6%) | 8.713 (39,0%) |
| CE + RIE | 10.490 | 5.431 (51,8%) | 3.973 (37,9%) | 2.904 (27,7%) |

A concordância global média por mapa (incluindo municípios não significativos) situa-se entre 76,4% e 88,9%, o que confirma que a divergência se concentra justamente nas bordas dos aglomerados — onde a topologia de vizinhança mais importa. A queda mais acentuada ocorre sob distância inversa, cuja vizinhança média (17,3) é mais de três vezes a da contiguidade Queen, suavizando defasagens espaciais e diluindo aglomerados pequenos. O arquivo `concordancia_univariada_por_subclasse.csv` detalha, para cada subclasse, o número de municípios significativos sob Queen e quantos são mantidos sob cada alternativa, permitindo identificar as subclasses de núcleo robusto.

### A.4 Robustez do Moran bivariado global à especificação de W

O I de Moran bivariado global foi computado para os 92.020 pares sob as três matrizes, replicando exatamente o esquema de permutação condicional do esda.Moran_BV (variável focal fixa, parceira permutada; 999 permutações; implementação vetorizada validada contra o pacote, com divergência máxima do I observado da ordem de 10⁻¹⁷ e diferenças de pseudo p-valor compatíveis com ruído de Monte Carlo). Dos 21.964 pares significativos sob Queen, 7.837 (35,7%) permanecem significativos com mesmo sinal sob KNN-5, 6.298 (28,7%) sob distância inversa e 3.933 (17,9%) sob ambas. Restringindo aos pares de associação positiva (I > 0), de maior interesse para a leitura de potencialidades co-localizadas, 1.702 de 10.092 (16,9%) resistem às duas alternativas.

### A.5 Controle de comparações múltiplas (FDR)

A correção adotou o procedimento de Benjamini–Hochberg na forma implementada em esda.fdr, aplicada em duas escalas: dentro de cada mapa LISA (224 testes locais por subclasse) e através do universo de pares bivariados (92.020 testes globais). Um aspecto operacional relevante: com 999 permutações, o menor pseudo p-valor alcançável é 0,001, insuficiente para a resolução exigida pelos limiares de Benjamini–Hochberg nas caudas — razão pela qual os p-valores destinados à correção foram recalculados com 9.999 permutações (menor p alcançável: 0,0001). Os resultados:

| Análise | Sig. nominais (p < 0,05) | Sobreviventes ao FDR | Taxa de sobrevivência |
|---|---|---|---|
| LISA univariado — Estoque (Queen) | 22.433 | 16.045 | 71,5% |
| LISA univariado — CE + RIE (Queen) | 10.640 | 1.096 | 10,3% |
| Moran bivariado global (Queen) | 22.511 | 944 (436 com I > 0) | 4,2% |

No pipeline de estoques, 373 das 380 subclasses mantêm ao menos um aglomerado após a correção; no shift-share, 103 de 290. O corte FDR do universo bivariado foi p ≤ 0,000513; nenhum par satisfaz o critério de Bonferroni (p ≤ 5,4 × 10⁻⁷), inalcançável na resolução de permutação adotada. Os 944 pares sobreviventes estão listados em `pares_bivariados_pos_FDR.csv`, ordenados por pseudo p-valor, e constituem o subconjunto recomendado para leituras confirmatórias preliminares e priorização de estudos de caso.

### A.6 Interpretação conjunta

As duas análises convergem para a mesma leitura: os resultados do pipeline de estoques são majoritariamente robustos tanto à especificação de W quanto à correção de multiplicidade, enquanto os resultados do pipeline shift-share — e, sobretudo, a camada bivariada — comportam-se como evidência exploratória de primeira triagem. Essa assimetria é esperada: a variável CE + RIE mede componentes de variação (mais voláteis e sujeitos a ruído de janela temporal) sobre um suporte municipal mais esparso, ao passo que os estoques medem níveis acumulados. Recomenda-se que o painel e os relatórios derivados sinalizem, para cada aglomerado e cada par exibido, sua pertença ou não ao núcleo robusto (invariante a W e sobrevivente ao FDR), preservando o restante como material de exploração.

### A.7 Reprodutibilidade

Os scripts `01_bivariado_global.py`, `02_univariado_fdr.py` e `03_univ_fdr9999.py` acompanham este anexo. Ambiente: Python 3.12, esda 2.10.0, libpysal 4.15.0, geopandas 1.1.4. Parâmetros fixos: permutações condicionais com semente 42; padronização por linha em todas as matrizes; significância nominal p < 0,05; FDR a α = 0,05.

---

**Referências adicionais sugeridas para a seção de limitações:**
Anselin, L. (2019). A local indicator of multivariate spatial association: extending Geary's c. *Geographical Analysis*, 51(2), 133–150. · Benjamini, Y.; Hochberg, Y. (1995). Controlling the false discovery rate. *JRSS-B*, 57(1), 289–300. · Castro, M. C.; Singer, B. H. (2006). Controlling the false discovery rate: a new application to account for multiple and dependent tests in local statistics of spatial association. *Geographical Analysis*, 38(2), 180–208.
