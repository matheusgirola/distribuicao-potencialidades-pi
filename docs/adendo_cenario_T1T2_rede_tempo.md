# Adendo (3ª revisão) — Cenário T1+T2 com matrizes rodoviária e de tempo de viagem

*Esta versão substitui as anteriores em dois pontos: (i) o pipeline de estoques passa a usar a base atualizada `potencialidades_consolidado_v2.csv` (que incorpora as novas classificações T1); (ii) a análise de robustez ganha uma quarta especificação de W, construída sobre a malha rodoviária real do estado — respondendo diretamente à ressalva residual da Limitação 2 de que nenhuma matriz incorporava conectividade rodoviária.*

## A matriz de vizinhança rodoviária (W-rede)

A malha viária foi montada a partir dos arquivos de rodovias estaduais (532 trechos) e federais do Piauí, excluídos os 84 trechos federais com situação "Planejada" (não construídos) e mantidos os pavimentados e em leito natural — 733 trechos e 13.896 km no total. A rede foi nodada nas interseções (56.900 segmentos), densificada a cada 2 km e convertida em grafo (54.605 nós; 62.560 arestas ponderadas pelo comprimento); 99,8% dos nós pertencem ao componente conexo gigante, adotado como rede de referência. Cada sede municipal foi conectada ao nó mais próximo por uma "perna de acesso" euclidiana (média de 5,4 km; máximo de 34,5 km — 11 municípios distam mais de 20 km de rodovia mapeada, informação relevante por si só para a agenda de conectividade). As distâncias rodoviárias entre as 224 sedes foram calculadas por Dijkstra. A razão mediana entre distância rodoviária e euclidiana (circuidade) é de 1,40 (percentil 90: 1,84), com correlação de 0,972 entre as duas métricas. A matriz W-rede usa pesos 1/d sobre a banda mínima que garante ao menos um vizinho a cada município — 107,9 km de distância rodoviária — com padronização por linha (média de 12,8 vizinhos). Ferrovias (incluindo a Transnordestina, em implantação) não foram incorporadas à matriz de conectividade vigente, mas os arquivos permitem construir cenários prospectivos.

## Robustez a W sob quatro especificações (Limitação 2)

Concordância medida sobre as observações município–subclasse (univariado) e pares (bivariado global) significativos sob Queen, com 999 permutações e semente 42; "mantido" = mesmo quadrante (uni) ou mesma significância e sinal (biv).

| Pipeline T1+T2 | Sig. Queen | KNN-5 | Dist. inversa | **Rede rodoviária** | 3 alternativas |
|---|---|---|---|---|---|
| Estoque — univariado | 5.991 | 57,7% | 45,5% | **46,1%** | 27,4% |
| Estoque — bivariado | 3.857 | 49,8% | 50,1% | **45,1%** | 30,8% |
| CE + RIE — univariado | 5.065 | 67,4% | 37,2% | **39,5%** | 22,8% |
| CE + RIE — bivariado | 2.061 | 37,8% | 32,1% | **29,3%** | 13,4% |

Dois achados merecem destaque. Primeiro, a matriz rodoviária se comporta de forma muito próxima à distância inversa euclidiana (46,1% contra 45,5% no univariado de estoques, por exemplo), coerente com a correlação de 0,972 entre as métricas: no Piauí, a conectividade rodoviária acompanha em larga medida a geografia. Isso não torna a matriz redundante — ela converte uma hipótese ("adjacência aproxima interação econômica") em medida empírica de acessibilidade, e as divergências localizadas (municípios de alta circuidade ou acesso precário) são justamente os casos em que Queen e a distância euclidiana superestimam a vizinhança efetiva. Segundo, o núcleo confirmado sob as três alternativas simultaneamente (22,8%–30,8% no univariado; 13,4%–30,8% no conjunto) constitui agora um critério de robustez exigente e defensável para leitura confirmatória.

## A matriz de tempo de viagem (W-tempo, OpenRouteService)

Como quinta especificação, construiu-se uma matriz de tempos de viagem entre as sedes municipais a partir da Matrix API do OpenRouteService (perfil driving-car, base OpenStreetMap), extraída localmente pelo pesquisador em 15 chamadas em lote. A matriz retornou tempos válidos para 24.090 dos 24.976 pares; quatro municípios (Dom Inocêncio, Socorro do Piauí, Valença do Piauí e Passagem Franca do Piauí) tiveram as sedes ancoradas em trechos não roteáveis do OSM e foram imputados pela relação tempo–distância ajustada nos pares válidos sobre a matriz rodoviária oficial (tempo = 2.193 s + 46,4 s/km; R² = 0,933; velocidade implícita de 78 km/h). Diagnósticos de validação cruzada: correlação de 0,968 entre as distâncias ORS/OSM e as distâncias da malha oficial DNIT/DER (validação mútua das duas fontes); circuidade mediana de 1,38; velocidade média implícita mediana de 66,5 km/h; assimetria direcional desprezível (0,1%), permitindo simetrização. A W-tempo usa pesos 1/t sobre a banda mínima conexa de 133 minutos (média de 21,2 vizinhos), padronizada por linha. Ressalva: os tempos OSM são modelados a partir de atributos viários, não de tráfego observado.

## Robustez a W sob cinco especificações (Limitação 2) — tabela consolidada

| Pipeline T1+T2 | Sig. Queen | KNN-5 | Dist. inversa | Rede rodov. | **Tempo (ORS)** | 4 alternativas |
|---|---|---|---|---|---|---|
| Estoque — univariado | 5.991 | 57,7% | 45,5% | 46,1% | **40,7%** | 20,9% |
| Estoque — bivariado | 3.857 | 49,8% | 50,1% | 45,1% | **46,3%** | 26,9% |
| CE + RIE — univariado | 5.065 | 67,4% | 37,2% | 39,5% | **32,0%** | 14,3% |
| CE + RIE — bivariado | 2.061 | 37,8% | 32,1% | 29,3% | **29,7%** | 10,1% |

A matriz de tempo é a mais exigente das quatro alternativas no univariado (40,7% e 32,0% de manutenção), coerente com sua vizinhança mais densa (21,2 vizinhos médios) e com o fato de o tempo penalizar trechos lentos que a distância pura não captura. O núcleo confirmado sob as quatro alternativas simultaneamente — o critério mais exigente disponível — retém 20,9% (estoques) e 14,3% (CE + RIE) dos aglomerados univariados e 26,9% / 10,1% dos pares bivariados. Com a incorporação do tempo de viagem, a ressalva residual da Limitação 2 fica restrita a fluxos efetivos de bens e pessoas e vínculos funcionais não físicos (dados de origem–destino).

## Comparações múltiplas (Limitação 3) — números atualizados (base v2)

| Análise (T1+T2, Queen, 9.999 perm.) | Sig. nominais | Sobreviventes ao FDR | Taxa |
|---|---|---|---|
| LISA univariado — Estoque (v2) | 6.042 | 4.032 | 66,7% |
| LISA univariado — CE + RIE | 5.118 | 3.870 | 75,6% |
| Moran bivariado global — Estoque (v2) | 3.915 | 1.792 (937 com I > 0) | 45,8% |
| Moran bivariado global — CE + RIE | 2.073 | 552 (238 com I > 0) | 26,6% |

O corte FDR do universo bivariado de estoques foi p ≤ 0,00766. A leitura das versões anteriores se mantém: o recorte tipológico T1+T2 eleva substancialmente a sobrevivência à correção em relação ao universo completo (10,3% e 4,2% nos casos correspondentes), concentrando o caráter exploratório no universo não classificado.

## Texto sugerido para a Limitação 2 (parágrafo final, substituindo a ressalva residual)

"Para além das matrizes geométricas, construiu-se uma matriz de vizinhança baseada em distâncias rodoviárias efetivas sobre a malha estadual e federal (13,9 mil km, excluídos trechos planejados), com pernas de acesso das sedes à rede. Os resultados sob a matriz rodoviária aproximam-se dos obtidos com distância inversa euclidiana (correlação de 0,972 entre as métricas; circuidade mediana de 1,40), indicando que, no Piauí, a topologia viária acompanha em larga medida a geografia — com exceções localizadas em municípios de acesso precário (onze sedes distam mais de 20 km de rodovia mapeada). Permanecem fora do escopo das matrizes testadas os tempos de deslocamento (condição do pavimento), fluxos efetivos de bens e pessoas e vínculos funcionais não físicos, cuja modelagem demandaria dados de origem–destino."

## Reflexo no painel interativo (v4)

O escopo "Classificadas (T1+T2)" da aba Clusters Espaciais foi regenerado com a base v2: 54 mapas univariados (subclasses com I de Moran global significativo, de 119 elegíveis) e 1.298 mapas bivariados (pares positivos e significativos com focal significativa). Marcações: ★ e "robusto (FDR)" para os 601 pares que sobrevivem à correção de Benjamini–Hochberg; "confirmado sob as 3 W alt." para os 483 pares estáveis sob KNN-5, distância inversa e rede rodoviária; subtítulos univariados informam núcleos pós-FDR e núcleos robustos às três matrizes alternativas (incluindo a rodoviária). O escopo "Emergentes (T-1)" permanece intacto. Arquivo: `painel_potencialidades_v5.html` (2,3 MB, 1.426 mapas), que substitui o v4: os subtítulos passam a reportar robustez às quatro matrizes alternativas (446 pares bivariados confirmados sob as quatro) e a introdução menciona a matriz de tempo de viagem.

## Arquivos e reprodutibilidade

`painel_potencialidades_v4.html` · `T1T2_pares_bivariados_pos_FDR_estoque.csv` (937 pares I > 0, base v2) · `concordancia_T1T2_4matrizes.csv` (detalhe por subclasse sob as quatro matrizes) · scripts `08_rede_rodoviaria.py` (construção da W-rede), `09_t1t2_com_rede.py` (análise sob 4 W), `10_v2_extra.py` (FDR base v2) e `11_painel_v4.py` (painel). Ambiente: Python 3.12, esda 2.10.0, libpysal 4.15.0, geopandas ≥ 1.1, scipy (Dijkstra), shapely (nodação da rede). Parâmetros: semente 42; 999 permutações (concordância) e 9.999 (FDR); p < 0,05; α FDR = 0,05.
