const path = require('path');
const RAIZ = path.resolve(__dirname, '..');
const L = require(path.join(__dirname, 'docx_lib.js'));
const fs = require('fs');
const T = JSON.parse(fs.readFileSync(path.join(RAIZ, 'saidas/tab/tabelas_unif.json'), 'utf8'));
const SZ = JSON.parse(fs.readFileSync(path.join(RAIZ, 'saidas/fig/sizes.json'), 'utf8'));

L.setFontePadrao('Fonte: elaboração própria a partir de IBGE (2025) e RAIS/MTE (2025).');
const c = [];

c.push(...L.capa(
  'ANÁLISE ESPACIAL INTEGRADA DAS POTENCIALIDADES T1 E T2',
  'Magnitude, dinâmica competitiva e o duplo núcleo robusto de co-localização — Piauí',
  'Relatório analítico',
  'Fontes primárias: IBGE (PAM, PPM, PEVS, Malha Municipal 2025), RAIS/MTE, DNIT/DER-PI, OpenStreetMap',
  'Teresina, 2026'
));
c.push(...L.sumario());

// ---------------- 1 INTRODUÇÃO ----------------
c.push(L.H('1 INTRODUÇÃO', 1));
c.push(L.P('Este relatório consolida, em um único documento, a análise espacial das potencialidades econômicas classificadas como T1 e T2 do Piauí sob suas duas dimensões complementares. A primeira é a magnitude: o pipeline de estoques, construído sobre os levantamentos físicos e de emprego do IBGE (PAM, PPM, PEVS) e da RAIS, responde onde cada potencialidade é grande. A segunda é a dinâmica: o pipeline shift-share, construído sobre a soma dos componentes competitivo estrutural (CE) e regional idiossincrático (RIE) do emprego formal, responde onde cada potencialidade está ganhando competitividade. As classes T1 e T2 exigem, por construção, vantagem competitiva nacional e municipal simultâneas — T1 em economias municipais dinâmicas, T2 em economias mais lentas.'));
c.push(L.P('Além de reunir os resultados dos dois pipelines — cada um com seus aglomerados univariados, suas verificações de robustez e seu núcleo robusto de pares co-localizados —, o relatório introduz uma análise nova: o cruzamento formal dos dois núcleos. Um par de subclasses que se co-localiza de forma robusta tanto em magnitude quanto em dinâmica constitui a evidência mais exigente que o desenho do projeto permite produzir, e o conjunto desses pares — o duplo núcleo — é o principal produto deste documento.'));
c.push(L.P('O texto se organiza em nove seções: os aspectos metodológicos comuns (seção 2); os aglomerados de magnitude (seção 3) e de dinâmica competitiva (seção 4); a robustez à especificação de vizinhança (seção 5) e o controle de comparações múltiplas (seção 6), reportados de forma comparada; os núcleos robustos de co-localização de cada pipeline (seção 7); o cruzamento dos núcleos e sua geografia de convergência (seção 8); e as considerações finais (seção 9).'));

// ---------------- 2 METODOLOGIA ----------------
c.push(L.H('2 ASPECTOS METODOLÓGICOS', 1));
c.push(L.H('2.1 Dados e recortes', 2));
c.push(L.P('O pipeline de estoques parte da base consolidada de potencialidades (versão 2), com 50.513 registros; o filtro T1/T2 retém 10.032 registros que, após a deduplicação pelo maior estoque entre as três janelas de comparação (anos-base 2013, 2018 e 2022), resultam em 6.295 pares município–subclasse, distribuídos por 710 subclasses e pelos 224 municípios. A variável de intensidade é o estoque municipal no ano final, transformado por log1p. O pipeline shift-share parte do consolidado do emprego formal (RAIS/MTE), com 915.936 registros; o filtro T1/T2 com decomposição válida retém 6.198 registros que, deduplicados pelo maior CE+RIE, resultam em 3.920 pares, em 650 subclasses e 222 municípios (Pau D\u2019Arco do Piauí e Pedro Laurentino não registram potencialidade classificada com decomposição válida). A variável de intensidade é CE+RIE sob a transformação logarítmica sinalizada — que, no recorte T1/T2, equivale ao log1p simples, pois ambos os componentes são positivos por definição. A malha territorial comum é a Malha Municipal Digital 2025 do IBGE.'));
c.push(L.H('2.2 Estatísticas espaciais', 2));
c.push(L.P('Nos dois pipelines, a análise univariada usa o I de Moran local (LISA) com matriz de contiguidade Queen padronizada por linha, 999 permutações condicionais e semente 42, ao nível de 5%, para as subclasses presentes em ao menos dez municípios — 120 elegíveis nos estoques e 87 no shift-share. O I de Moran global ordena a força do agrupamento. A análise bivariada usa o I de Moran bivariado global e local (variável focal contra a defasagem espacial da parceira), para os pares com ao menos cinco municípios de copresença — 11.690 e 7.047 pares, respectivamente.'));
c.push(L.H('2.3 Verificações de robustez e definição dos núcleos', 2));
c.push(L.P('Dois critérios qualificam todos os resultados. O primeiro é a estabilidade sob quatro matrizes alternativas de vizinhança: k vizinhos mais próximos (k = 5); distância inversa euclidiana com banda de 76,5 km; distância rodoviária inversa sobre a malha viária estadual e federal construída (13,9 mil km, excluídos trechos planejados; banda conexa de 107,9 km); e tempo de viagem inverso entre sedes municipais, extraído do OpenRouteService sobre a base OpenStreetMap (banda conexa de 133 minutos). O segundo é a sobrevivência à correção de comparações múltiplas pela taxa de falsas descobertas (FDR) de Benjamini e Hochberg (1995), na aplicação de Castro e Singer (2006), com pseudo p-valores sob 9.999 permutações. O núcleo robusto de pares de cada pipeline exige simultaneamente: I bivariado positivo e significativo sob Queen, subclasse focal com agrupamento global significativo, sobrevivência ao FDR e confirmação sob as quatro matrizes alternativas. O duplo núcleo, objeto da seção 8, é a interseção dos dois núcleos, comparados como pares não ordenados de subclasses.'));
c.push(L.P('Três ressalvas acompanham a leitura: os tempos de viagem são modelados a partir de atributos viários, não de tráfego observado; quatro municípios tiveram tempos imputados pela relação tempo–distância ajustada (R² = 0,933); e a variável CE+RIE, por medir componentes de variação entre janelas, é estruturalmente mais ruidosa que o estoque — assimetria que as seções comparadas 5 e 6 quantificam. Resultados fora dos filtros de robustez permanecem válidos como evidência exploratória.'));

// ---------------- 3 MAGNITUDE ----------------
c.push(L.H('3 AGLOMERADOS DE MAGNITUDE (PIPELINE DE ESTOQUES)', 1));
c.push(L.P('Das 120 subclasses elegíveis, 54 apresentam autocorrelação espacial global positiva e significativa, com 560 observações municipais em núcleos Alto-Alto distribuídas por 185 municípios — mais de quatro quintos do território participa de ao menos um aglomerado de magnitude. A Tabela 1 apresenta as doze subclasses de agrupamento mais forte.', { after: 0 }));
c.push(L.Titulo('Tabela 1 – Subclasses T1/T2 com agrupamento espacial mais forte da magnitude (estoques), com indicadores de robustez – Piauí – 2025'));
c.push(L.mkTable(T.t1, { size: 14, firstW: 2600 }));
c.push(L.Nota('Nota: "Pós-FDR" conta municípios significativos em qualquer quadrante após a correção de Benjamini–Hochberg (9.999 permutações), incluindo núcleos Baixo-Baixo de ausência conjunta; "Robustos às 4 W alt." conta núcleos que mantêm o quadrante sob as quatro matrizes alternativas.'));
c.push(L.Fonte('Fonte: elaboração própria a partir de IBGE (2025) e RAIS/MTE (2025).'));
c.push(L.P('O mel de abelha lidera (I = 0,720), seguido do bloco extrativo-pecuário (babaçu, caprinos, galináceos) e das culturas de grãos. A geografia organiza-se em duas macrorregiões: o eixo norte — Região Metropolitana de Teresina e Vale do Longá/Cocais, com União (16 subclasses em núcleo AA), Teresina (13), Altos e José de Freitas (12) — e a fronteira de grãos do Cerrado no sudoeste, capitaneada por Baixa Grande do Ribeiro. A Figura 1 mapeia a distribuição.', { after: 0 }));
c.push(L.Titulo('Figura 1 – Número de subclasses T1/T2 em núcleo Alto-Alto significativo da magnitude, por município – Piauí – 2025'));
c.push(L.Fig('f1', 'fig', SZ));
c.push(L.Nota('Nota: contorno em destaque nos oito municípios de maior contagem.'));
c.push(L.Fonte('Fonte: elaboração própria a partir de IBGE (2025) e RAIS/MTE (2025).'));

// ---------------- 4 DINÂMICA ----------------
c.push(L.H('4 AGLOMERADOS DE DINÂMICA COMPETITIVA (PIPELINE CE+RIE)', 1));
c.push(L.P('Das 87 subclasses elegíveis, 28 agrupam-se de forma significativa, com 97 núcleos Alto-Alto concentrados em apenas 33 municípios. A dinâmica competitiva, portanto, não acompanha a difusão territorial da magnitude: adensa-se em poucos polos. A Tabela 2 apresenta as doze subclasses mais fortes.', { after: 0 }));
c.push(L.Titulo('Tabela 2 – Subclasses T1/T2 com agrupamento espacial mais forte da dinâmica competitiva (CE+RIE), com indicadores de robustez – Piauí – 2013-2025'));
c.push(L.mkTable(T.t2, { size: 14, firstW: 2600 }));
c.push(L.Nota('Nota: ver nota da Tabela 1; a coluna Pós-FDR pode exceder os municípios presentes por incluir núcleos Baixo-Baixo.'));
c.push(L.Fonte('Fonte: elaboração própria a partir de RAIS/MTE (2025).'));
c.push(L.P('A intensidade é sistematicamente menor (I máximo de 0,229, no cultivo de arroz, contra 0,720 da magnitude) e a composição setorial muda de natureza: agricultura empresarial (arroz, soja, frangos, bovinos de corte) convive com um bloco urbano e de consumo — hotéis, restaurantes, comércio varejista, serviços administrativos, educação infantil. É o retrato de onde o emprego formal está ganhando competitividade. A geografia repete o quadrilátero metropolitano (União, Teresina, José de Freitas, Altos) e acrescenta o litoral (Luís Correia) e um ponto na fronteira de grãos, como mostra a Figura 2.', { after: 0 }));
c.push(L.Titulo('Figura 2 – Número de subclasses T1/T2 em núcleo Alto-Alto significativo da dinâmica competitiva, por município – Piauí – 2013-2025'));
c.push(L.Fig('f1ss', 'fig', SZ));
c.push(L.Nota('Nota: contorno em destaque nos oito municípios de maior contagem.'));
c.push(L.Fonte('Fonte: elaboração própria a partir de RAIS/MTE (2025).'));

// ---------------- 5 ROBUSTEZ W ----------------
c.push(L.H('5 ROBUSTEZ À ESPECIFICAÇÃO DE VIZINHANÇA', 1));
c.push(L.P('A Tabela 3 compara, para os dois pipelines, a estabilidade dos resultados quando a matriz Queen é substituída pelas quatro especificações alternativas.', { after: 0 }));
c.push(L.Titulo('Tabela 3 – Proporção dos resultados significativos sob Queen mantidos sob matrizes alternativas de vizinhança – dois pipelines, recorte T1+T2 – Piauí'));
c.push(L.mkTable(T.t3, { size: 14, firstW: 2600 }));
c.push(L.Nota('Nota: univariado — mesmo quadrante e significância; bivariado — mesma significância e sinal do I. "As 4 alternativas" exige manutenção simultânea sob KNN-5, distância inversa, rede rodoviária e tempo de viagem.'));
c.push(L.Fonte('Fonte: elaboração própria a partir de IBGE (2025) e RAIS/MTE (2025).'));
c.push(L.P('Três leituras emergem da comparação. Primeiro, a sensibilidade à vizinhança é real nos dois pipelines, e maior na dinâmica: o núcleo invariante às quatro alternativas retém 20,9% dos aglomerados univariados de magnitude, mas apenas 14,3% dos de dinâmica — coerente com contornos mais estreitos e ruidosos. Segundo, o padrão entre matrizes repete-se: KNN-5 é a alternativa mais concordante e o tempo de viagem, a mais exigente, por sua vizinhança mais densa e por penalizar trechos lentos que a distância pura não captura. Terceiro, as matrizes de infraestrutura comportam-se de forma próxima à distância inversa euclidiana — a correlação entre distância rodoviária e euclidiana é de 0,972, com circuidade mediana de 1,40 —, indicando que, no Piauí, a topologia viária acompanha em larga medida a geografia; as divergências concentram-se nos municípios de acesso precário, onde a contiguidade superestima a vizinhança efetiva.'));

// ---------------- 6 FDR ----------------
c.push(L.H('6 CONTROLE DE COMPARAÇÕES MÚLTIPLAS', 1));
c.push(L.P('Ao nível nominal de 5%, seriam esperados cerca de 11 falsos positivos por mapa univariado em cada pipeline, além de 585 e 352 pares bivariados espúrios nos universos de 11.690 e 7.047 pares. Aplicada a correção FDR, a magnitude retém 4.032 dos 6.042 municípios nominalmente significativos no univariado (66,7%) e 1.792 dos 3.915 pares bivariados (45,8%, dos quais 937 com associação positiva; corte p ≤ 0,0077). A dinâmica retém 3.870 de 5.118 no univariado (75,6% — a maior taxa do projeto) e 552 de 2.073 no bivariado (26,6%, dos quais 238 positivos; corte p ≤ 0,0039).'));
c.push(L.P('Os perfis de robustez dos dois pipelines são, portanto, espelhados: a magnitude resiste mais à troca da matriz de vizinhança, a dinâmica resiste mais à correção de multiplicidade. A explicação é geométrica — os aglomerados de CE+RIE são poucos, compactos e de significância local muito forte, sobrevivendo bem ao FDR, mas com contornos facilmente redesenhados quando a definição de vizinhança muda. Em ambos os casos, o filtro tipológico T1/T2 atua como pré-filtro de qualidade estatística: no universo completo das bases, a mesma correção elimina a grande maioria dos resultados.'));

// ---------------- 7 NÚCLEOS ROBUSTOS ----------------
c.push(L.H('7 CO-LOCALIZAÇÃO: OS NÚCLEOS ROBUSTOS DE CADA PIPELINE', 1));
c.push(L.P('Aplicados os quatro requisitos do núcleo robusto — associação positiva e significativa, focal significativa, FDR e confirmação sob as quatro matrizes —, a magnitude produz um núcleo de 340 pares (de 1.298 candidatos) e a dinâmica, um núcleo de 50 pares (de 568). As Tabelas 4 e 5 listam os vinte mais fortes de cada um; as listas completas constam da planilha de apoio.', { after: 0 }));
c.push(L.Titulo('Tabela 4 – Os vinte pares mais co-localizados do núcleo robusto da magnitude (estoques) – Piauí – 2025', true));
c.push(L.mkTable(T.t4, { size: 13, firstW: 500 }));
c.push(L.Nota('Nota: I biv. sob matriz Queen; núcleos AA do LISA bivariado local (999 permutações).'));
c.push(L.Fonte('Fonte: elaboração própria a partir de IBGE (2025) e RAIS/MTE (2025).'));
c.push(L.P('O núcleo da magnitude é dominado pelo complexo apícola-extrativo-pecuário do norte (caprino×mel lidera, I = 0,431; galináceos, ovinos, babaçu) e pelo complexo de grãos do sudoeste (soja, milho, arroz e seus elos de serviços). A Figura 3 mapeia a frequência municipal de participação nesses 340 pares.', { after: 0 }));
c.push(L.Titulo('Figura 3 – Número de pares robustos da magnitude com núcleo Alto-Alto no município – Piauí – 2025'));
c.push(L.Fig('f2', 'fig', SZ));
c.push(L.Nota('Nota: contorno em destaque nos oito municípios de maior contagem.'));
c.push(L.Fonte('Fonte: elaboração própria a partir de IBGE (2025) e RAIS/MTE (2025).'));
c.push(L.P('No núcleo da dinâmica, três assinaturas se destacam: o complexo turístico-imobiliário do litoral (hotéis×condomínios, com núcleo Alto-Alto em Cajueiro da Praia, Luís Correia e Parnaíba), o complexo pecuária–grãos (bovinos de corte com milho, arroz e soja) e o tecido de serviços urbanos do quadrilátero metropolitano. O primeiro é a contribuição mais distintiva do pipeline: um aglomerado invisível nas magnitudes, dominadas pelas cadeias agropecuárias.', { after: 0 }));
c.push(L.Titulo('Tabela 5 – Os vinte pares mais co-localizados do núcleo robusto da dinâmica competitiva (CE+RIE) – Piauí – 2013-2025', true));
c.push(L.mkTable(T.t5, { size: 13, firstW: 500 }));
c.push(L.Nota('Nota: I biv. sob matriz Queen; núcleos AA do LISA bivariado local (999 permutações).'));
c.push(L.Fonte('Fonte: elaboração própria a partir de RAIS/MTE (2025).'));
c.push(L.P('A Figura 4 completa o quadro com a frequência municipal de participação nos 50 pares robustos da dinâmica: Teresina (33), Altos (31), União e José de Freitas (27) repetem o quadrilátero, e Ilha Grande e Cajueiro da Praia inscrevem o litoral.', { after: 0 }));
c.push(L.Titulo('Figura 4 – Número de pares robustos da dinâmica competitiva com núcleo Alto-Alto no município – Piauí – 2013-2025'));
c.push(L.Fig('f2ss', 'fig', SZ));
c.push(L.Nota('Nota: contorno em destaque nos oito municípios de maior contagem.'));
c.push(L.Fonte('Fonte: elaboração própria a partir de RAIS/MTE (2025).'));

// ---------------- 8 CRUZAMENTO ----------------
c.push(L.H('8 O DUPLO NÚCLEO: CRUZAMENTO FORMAL DOS DOIS PIPELINES', 1));
c.push(L.P('O cruzamento compara os dois núcleos como pares não ordenados de subclasses, após normalização dos nomes. O resultado é notável: 32 pares pertencem simultaneamente aos dois núcleos — quase dois terços (64%) do núcleo da dinâmica também é núcleo da magnitude. São pares que se co-localizam de forma estatisticamente exigente tanto onde a potencialidade é grande quanto onde ela está ganhando competitividade, e constituem os candidatos mais fortes do estado a políticas de adensamento produtivo. A Tabela 6 lista o duplo núcleo completo, com o I bivariado de cada pipeline e o número de municípios em que os núcleos Alto-Alto dos dois pipelines coincidem.', { after: 0 }));
c.push(L.Titulo('Tabela 6 – O duplo núcleo: os 32 pares de subclasses presentes nos núcleos robustos dos dois pipelines – Piauí', true));
c.push(L.mkTable(T.t6, { size: 13, firstW: 500, widths: [500, 5271, 1100, 1100, 1100] }));
c.push(L.Nota('Nota: pares comparados como conjuntos não ordenados; quando um par aparece nas duas direções (x→lag y e y→lag x), reporta-se o maior I. "AA conv." é o número de municípios classificados Alto-Alto no LISA bivariado local do par nos DOIS pipelines simultaneamente.'));
c.push(L.Fonte('Fonte: elaboração própria a partir de IBGE (2025) e RAIS/MTE (2025).'));
c.push(L.P('Três características do duplo núcleo merecem registro. Primeiro, sua composição: o par turístico hotéis×condomínios prediais encabeça a lista, seguido do bloco pecuária–grãos (bovinos de corte com arroz, milho e soja) e de um denso tecido de comércio e serviços urbanos — varejo especializado, padarias, hipermercados, educação infantil, obras de urbanização, serviços administrativos. Segundo, sua consistência interna: todos os 32 pares têm ao menos um município de convergência, com média de 5,4 municípios por par em que os núcleos Alto-Alto dos dois pipelines coincidem. Terceiro, sua leitura setorial: os grandes complexos agroextrativistas exclusivos da magnitude (mel, babaçu, caprinos entre si) não entram no duplo núcleo — são potencialidades grandes cuja dinâmica de emprego formal ainda não se agrupa —, enquanto o núcleo urbano-turístico entra quase inteiro.'));
c.push(L.P('A Figura 5 mapeia a geografia da convergência: para cada município, o número de pares do duplo núcleo em que ele integra o núcleo Alto-Alto dos dois pipelines simultaneamente.', { after: 0 }));
c.push(L.Titulo('Figura 5 – Convergência entre magnitude e dinâmica: número de pares do duplo núcleo com coincidência Alto-Alto no município – Piauí'));
c.push(L.Fig('f5conv', 'fig', SZ));
c.push(L.Nota('Nota: contorno em destaque nos oito municípios de maior contagem.'));
c.push(L.Fonte('Fonte: elaboração própria a partir de IBGE (2025) e RAIS/MTE (2025).'));
c.push(L.P('A convergência concentra-se em 36 municípios, e sua hierarquia é inequívoca: Teresina participa da coincidência em 21 dos 32 pares, Altos em 20, União em 17, Demerval Lobão e José de Freitas em 15 — o quadrilátero metropolitano ampliado por Nazária (10). Fora dele, dois territórios emergem: o litoral (Cajueiro da Praia, 8; Ilha Grande, 7), ancorado no par turístico, e a fronteira de grãos (Baixa Grande do Ribeiro, 5; Currais, 4), ancorada no bloco pecuária–grãos. É o mapa mais seletivo que o projeto produz: onde magnitude acumulada e ganho de competitividade coincidem, par a par.'));

// ---------------- 9 CONSIDERAÇÕES ----------------
c.push(L.H('9 CONSIDERAÇÕES FINAIS', 1));
c.push(L.P('Cinco conclusões consolidam o relatório. Primeira: o agrupamento espacial das potencialidades T1/T2 é real nos dois pipelines, com perfis complementares — a magnitude é difusa (54 subclasses, 185 municípios) e a dinâmica é concentrada (28 subclasses, 33 municípios). Segunda: os perfis de robustez são espelhados — a magnitude resiste mais à especificação de vizinhança, a dinâmica resiste mais à correção de comparações múltiplas — e, em ambos, o filtro tipológico atua como pré-filtro de qualidade estatística. Terceira: os núcleos robustos de co-localização (340 e 50 pares) são economicamente interpretáveis: complexos apícola-extrativo-pecuário e de grãos na magnitude; turismo litorâneo, pecuária–grãos e serviços urbanos na dinâmica. Quarta: o duplo núcleo de 32 pares — presentes nos dois núcleos, com convergência municipal verificada par a par — é o produto de síntese do projeto, e sua geografia (quadrilátero metropolitano, litoral turístico, fronteira de grãos) identifica os territórios onde magnitude e dinamismo coincidem. Quinta: a ausência dos grandes complexos agroextrativistas no duplo núcleo não os desqualifica — indica que são potencialidades consolidadas em produção cuja formalização do emprego ainda não gera aglomeração dinâmica, uma agenda de política em si.'));
c.push(L.P('Como desdobramentos: validar os 32 pares do duplo núcleo com evidência qualitativa junto aos territórios de desenvolvimento; construir o cenário prospectivo de conectividade com a ferrovia Transnordestina sobre as matrizes de infraestrutura já montadas; e monitorar, nas próximas edições da RAIS, se a dinâmica de emprego dos complexos agroextrativistas converge para seus estoques.'));

// ---------------- REFERÊNCIAS ----------------
c.push(L.H('REFERÊNCIAS', 1));
c.push(L.referencia('ANSELIN, L. Local indicators of spatial association — LISA. Geographical Analysis, v. 27, n. 2, p. 93–115, 1995.'));
c.push(L.referencia('BENJAMINI, Y.; HOCHBERG, Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. Journal of the Royal Statistical Society: Series B, v. 57, n. 1, p. 289–300, 1995.'));
c.push(L.referencia('CASTRO, M. C. de; SINGER, B. H. Controlling the false discovery rate: a new application to account for multiple and dependent tests in local statistics of spatial association. Geographical Analysis, v. 38, n. 2, p. 180–208, 2006.'));
c.push(L.referencia('INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA. Malha Municipal Digital 2025. Rio de Janeiro: IBGE, 2025.'));
c.push(L.referencia('INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA. Produção Agrícola Municipal; Pesquisa da Pecuária Municipal; Produção da Extração Vegetal e da Silvicultura. Rio de Janeiro: IBGE, 2025.'));
c.push(L.referencia('MINISTÉRIO DO TRABALHO E EMPREGO. Relação Anual de Informações Sociais (RAIS). Brasília: MTE, 2025.'));
c.push(L.referencia('OPENROUTESERVICE. Matrix API. Heidelberg: HeiGIT, Universidade de Heidelberg, 2026. Disponível em: https://openrouteservice.org. Acesso em: ago. 2026.'));
c.push(L.referencia('REY, S. J.; ANSELIN, L. PySAL: a Python library of spatial analytical methods. Review of Regional Studies, v. 37, n. 1, p. 5–27, 2007.'));

L.montarDocumento(c, path.join(RAIZ, 'saidas/Analise_espacial_integrada_potencialidades.docx'));
console.log('docx gerado');
