# Potencialidades T-1 do Piauí: setores que surgem sem passado

### Análise dos setores ausentes no período-base e presentes em 2024/2025 nos 224 municípios piauienses

---

## Sumário executivo

A classe **T-1** — setores que não existiam no município no ano-base e que aparecem no ano final da série — reúne **6.727 pares município–subclasse** distribuídos por **todos os 224 municípios** do Piauí e **855 subclasses**. Ao contrário das demais classes tipológicas, ela não admite leitura relativa: sem estoque anterior, não há taxa de crescimento, não há efeito estrutural, não há *shift-share*. Resta o **valor absoluto** — e é justamente aí que mora o risco analítico.

Cinco conclusões orientam o restante do relatório:

1. **A emergência é numerosa, mas rasa.** Na RAIS, **61,1% dos pares emergentes têm de 1 a 4 vínculos** e respondem por apenas **8,9% do emprego emergente**. Os **20,3% de pares com 10 ou mais vínculos concentram 83,1% dos vínculos**. Amplitude e densidade são coisas distintas: a maioria dos "novos setores" é um CNPJ solitário.

2. **Parte relevante da emergência é artefato de codificação, não economia.** Identificamos **188 pares em códigos CNAE já desativados** (todos com estoque zero) e **150 pares que são simples migração de código** (o estabelecimento não nasceu — o código mudou de nome), que sozinhos carregavam **6.609 vínculos falsamente "emergentes"**. Depurados, restam **5.673 emergências candidatas** e **70.079 vínculos**.

3. **A antiga anomalia "Codornas" da PPM foi corrigida na origem.** Em versões anteriores da base, essa subclasse aparecia como T-1 em 222 dos 224 municípios, somando 8,86 milhões de cabeças — um artefato de quebra de série. A base corrigida reduz o plantel de codornas a dois registros plausíveis por janela (máximo de 13.440 cabeças), nenhum deles classificado como T-1. **Esta versão do relatório já usa a base corrigida**; nenhuma leitura substantiva depende mais dessa exclusão.

4. **O que mais "emerge" com peso é o Estado, não o mercado.** A seção **O (Administração pública)** tem apenas 72 pares emergentes mas **12.249 vínculos** — 170,1 vínculos por par. A subclasse líder isolada é *"Regulação das atividades de saúde, educação, serviços culturais e outros serviços sociais"* (9.160 vínculos em 37 municípios), padrão típico de **reclassificação de CNAE da prefeitura**, não de nova base econômica.

5. **Descontado tudo isso, a emergência real do Piauí é uma economia de serviços de proximidade:** saúde (10.048 vínculos), comércio (9.154), indústria de transformação (5.778), educação (5.586) e construção (4.588). O único vetor claramente **exportador** aparece nas fontes IBGE: **soja (R$ 221,4 milhões em 17 municípios novos)**, sorgo, algodão e melão — a fronteira agrícola do sul/sudoeste e do litoral avançando sobre municípios que antes não plantavam.

6. **A análise espacial (LISA/Moran) confirma que a emergência com estrutura territorial se concentra em dois arranjos** (seção 7): a **fronteira de grãos do Cerrado** (Milho ↔ Mandioca é a associação bivariada mais forte, I = 0,271) e um **complexo aquícola-industrial nascente no entorno de Teresina e no norte**, em que piscicultura, ração animal e cerâmica emergem de forma espacialmente acoplada. Das 177 subclasses avaliadas, 50 têm autocorrelação espacial significativa — e as mais estruturadas são agropecuárias, não as que lideram a contagem bruta de vínculos.

---

## 1. O problema metodológico da classe T-1

Nas classes T1 a T8, o município tem estoque em `ano_inicial` e em `ano_final`; toda a maquinaria de decomposição (CE, RIE, *shift-share*) se apoia nessa diferença. Em T-1 o denominador é zero. Isso impõe três decisões:

**(a) Só o valor absoluto informa.** A magnitude no ano final é o único sinal disponível.

**(b) O significado do valor absoluto depende radicalmente da fonte.** Nas fontes IBGE (PAM, PPM, PEVS), a unidade é valor da produção ou rebanho; um valor pequeno significa produção pequena, e ponto. Na RAIS, a unidade é o **vínculo empregatício formal** — e um vínculo pode ser um MEI que abriu no ano passado. Uma "nova subclasse com 1 empregado" não é uma potencialidade: é ruído estatístico com aparência de descoberta.

**(c) Emergências raras precisam ser agregadas para serem lidas.** Uma subclasse com 2 vínculos em 3 municípios não diz nada sozinha; agregada à sua **seção CNAE 2.0**, passa a compor um padrão setorial legível.

Daí o desenho adotado, seguindo a sugestão do escopo:

| Faixa | Critério (RAIS) | Tratamento analítico |
|---|---|---|
| **0** | Estoque = 0 | Descartada — artefato de código desativado |
| **A** | 1 a 4 vínculos | Não interpretar individualmente. **Agregar por seção CNAE 2.0** |
| **B** | 5 a 9 vínculos | Leitura agregada por seção; subclasse só quando recorrente entre municípios |
| **C** | 10 a 49 vínculos | Leitura por subclasse |
| **D** | 50 ou mais | Leitura por par município–subclasse |

As faixas C e D são reportadas juntas como **"≥ 10 vínculos"** sempre que a comparação com A e B for o objetivo.

### 1.1 Uma dimensão extra: quando o setor emergiu

O arquivo consolidado contém **três janelas de observação** (ano-base 2013, 2018 e 2022). O mesmo par município–subclasse pode ser T-1 em uma, duas ou três delas — e isso data a emergência:

| Coorte | Leitura | Pares |
|---|---|---|
| **1. Emergência recente** | Ausente em 2013, 2018 **e 2022** → nasceu depois de 2022 | 2.024 |
| **2. Reemergência / intermitente** | Ausente em 2022, mas presente em janelas anteriores → atividade volátil, vai e volta | 524 |
| **3. Emergência 2019–2022** | Já existia em 2022 | 2.448 |
| **4. Emergência 2014–2018** | Presente desde ~2018 — já consolidada, "nova" apenas em relação a 2013 | 1.731 |

A coorte 2 é o alerta de fragilidade: **524 pares (7,8%)** não são setores novos, são setores que **oscilam entre existir e não existir**. E a coorte 1 é o alvo mais legítimo da leitura "não existia antes de 2024/2025".

![Figura 5](figuras/fig5_coortes.png)

---

## 2. A depuração: o que sobra depois de tirar o que não é economia

### 2.1 Códigos CNAE desativados (188 pares, estoque zero)

Todos os **189 registros com estoque igual a zero** na RAIS pertencem a subclasses marcadas `(Desativado)` — *Lojas de departamentos ou magazines (Desativado)*, *Comércio a varejo de peças e acessórios para motocicletas (Desativado)*, entre 13 códigos. São registros administrativos residuais. **Descartados.**

### 2.2 Migração de código: a emergência que é só um nome novo

Este é o achado mais importante da depuração. A subclasse **"Lojas de departamentos ou magazines, exceto lojas francas (Duty free)"** aparecia como a **2ª maior emergência do estado** (3.570 vínculos, 54 municípios). Mas ela é o **código sucessor** de *"Lojas de departamentos ou magazines"*, desativado — e em **76 dos 89 municípios** em que "emerge", o código antigo já existia na base. A loja não abriu; o CNAE foi renomeado.

O mesmo vale para peças de motocicleta (43 municípios, 997 vínculos) e bares (10 municípios, 527 vínculos). Somados os 13 pares antigo→novo mapeados: **150 pares e 6.609 vínculos removidos.**

> **Regra prática para as próximas iterações:** antes de declarar um setor "emergente", verifique se o município já tinha o código antecessor. A migração de códigos CNAE é uma fonte sistemática de falsos positivos em análises T-1 — e produz justamente os maiores números, porque são estabelecimentos grandes e antigos reaparecendo sob nova etiqueta.

### 2.3 A anomalia "Codornas" (PPM) — corrigida

Numa iteração anterior desta base, `Codornas` aparecia como T-1 em **666 de 672 registros da PPM** — em praticamente todos os municípios e todas as janelas —, com mediana de 19.836 cabeças e máximo de 1.092.406 (Altos). Um plantel de codornas simultâneo em 222 municípios, superior ao de galináceos, era incompatível com qualquer realidade produtiva: tratava-se de quebra/reestruturação da série da PPM.

**O problema foi corrigido na origem.** Na base atual, `Codornas` reduz-se a dois registros por janela (máximo de 13.440 cabeças) e **nenhum** deles é classificado como T-1. A subclasse simplesmente deixa de figurar entre as potencialidades emergentes — resultado coerente. Este relatório foi integralmente reprocessado sobre a base corrigida (`potencialidades_consolidado_v2.csv`), de modo que a antiga marcação de artefato de série não é mais necessária.

### 2.4 O funil

![Figura 9](figuras/fig9_funil.png)

Dos **6.011 pares emergentes da RAIS**, sobrevivem **5.673 candidatos** (70.079 vínculos); destes, **1.131 têm ≥ 10 vínculos** (57.420); e **1.079 são atividades de mercado** (45.229 vínculos), depois de separada a administração pública.

---

## 3. A anatomia das faixas: massa sem peso

![Figura 1](figuras/fig1_faixas.png)

| Faixa | Pares | % pares | Vínculos | % vínculos | Municípios | Subclasses | Mediana |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 — sem vínculo ativo | 189 | 3,1% | 0 | 0,0% | 102 | 14 | 0 |
| **A — 1 a 4 vínculos** | **3.670** | **61,1%** | **6.835** | **8,9%** | **224** | **666** | **2** |
| B — 5 a 9 vínculos | 933 | 15,5% | 6.117 | 8,0% | 184 | 354 | 6 |
| C — 10 a 49 vínculos | 938 | 15,6% | 18.627 | 24,3% | 164 | 368 | 17 |
| D — 50 ou mais | 281 | 4,7% | 45.109 | 58,8% | 117 | 112 | 96 |

**1.805 pares — 30% de toda a classe T-1 na RAIS — têm exatamente 1 vínculo**, espalhados por 221 dos 224 municípios. Se listássemos setores emergentes sem estratificar, um terço da lista seria composto por um único trabalhador formal.

A assimetria é brutal: **os 4,7% de pares com 50 ou mais vínculos concentram 58,8% do emprego emergente.** A conclusão de política pública é direta — *contar* setores novos é um péssimo indicador de dinamismo; é preciso *pesar* o que eles empregam.

### 3.1 A faixa A (1 a 4 vínculos): leitura agregada por seção CNAE

![Figura 6](figuras/fig6_faixaA_secao.png)

| Seção CNAE 2.0 | Pares | Vínculos | Municípios |
|---|---:|---:|---:|
| G — Comércio; reparação de veículos | 1.453 | 2.446 | 221 |
| C — Indústrias de transformação | 334 | 612 | 107 |
| A — Agropecuária, floresta, pesca | 288 | 512 | 124 |
| F — Construção | 257 | 486 | 140 |
| M — Profissionais, científicas e técnicas | 203 | 410 | 120 |
| Q — Saúde e serviços sociais | 193 | 344 | 103 |
| S — Outras atividades de serviços | 190 | 323 | 106 |
| R — Artes, cultura, esporte e recreação | 157 | 279 | 123 |
| N — Administrativas e complementares | 156 | 280 | 67 |
| I — Alojamento e alimentação | 149 | 267 | 91 |

**Quase 40% de toda a faixa A é comércio varejista.** É o retrato de um tecido produtivo que, quando "diversifica", diversifica abrindo lojas. As subclasses individualmente mais ubíquas nessa faixa confirmam o diagnóstico: **casas lotéricas (87 municípios)**, cartórios (59), comércio de peças de moto (56), organizações religiosas (55), comércio de material de construção (52), farmácias (42). Nada disso é base exportadora; é **infraestrutura mínima de consumo local chegando a municípios que não a tinham** — o que é socialmente relevante, mas não constitui potencialidade econômica no sentido de vantagem comparativa.

### 3.2 Faixa B (5 a 9 vínculos): a mesma estrutura, um degrau acima

| Seção | Pares | Vínculos | Municípios |
|---|---:|---:|---:|
| G — Comércio | 295 | 1.920 | 141 |
| C — Indústria de transformação | 119 | 761 | 56 |
| F — Construção | 87 | 607 | 72 |
| A — Agropecuária | 69 | 442 | 54 |
| M — Profissionais/técnicas | 58 | 384 | 49 |
| I — Alojamento e alimentação | 46 | 293 | 33 |

O comércio segue dominante, mas **a indústria de transformação e a construção ganham peso relativo** — sinal de que, onde a emergência tem alguma densidade, ela já não é apenas varejo.

### 3.3 O perfil de tamanho por seção

![Figura 2](figuras/fig2_secao_faixa.png)

A figura mostra qual seção "emerge grande" e qual "emerge pequena". Nas extremidades:

- **Emergem grandes:** O (Administração pública), D (Eletricidade e gás), P (Educação), Q (Saúde) — seções onde uma única unidade nova já traz dezenas ou centenas de vínculos.
- **Emergem minúsculas:** R (Artes/recreação), K (Financeiro), L (Imobiliário), S (Serviços pessoais) — dominadas por 1 a 4 vínculos. Nessas seções, a leitura **só faz sentido agregada**.

---

## 4. O que emerge com peso: faixa ≥ 10 vínculos

**1.131 pares depurados, 57.420 vínculos, 182 municípios, 389 subclasses.**

![Figura 3](figuras/fig3_top_subclasses.png)

### 4.1 As 15 subclasses emergentes mais relevantes

| # | Subclasse | Seção | Municípios | Vínculos | Mediana |
|---:|---|:--:|---:|---:|---:|
| 1 | Regulação das atividades de saúde, educação, serviços culturais e outros | O | 37 | 9.160 | 175 |
| 2 | Ensino fundamental | P | 17 | 3.413 | 153 |
| 3 | Práticas integrativas e complementares em saúde humana | Q | 17 | 2.112 | 84 |
| 4 | **Serviços de comunicação multimídia — SCM** | J | **47** | 2.068 | 26 |
| 5 | Pronto-socorro e unidades hospitalares de urgência | Q | 3 | 1.585 | 325 |
| 6 | Atividades de apoio à gestão de saúde | Q | 15 | 1.545 | 61 |
| 7 | Outras atividades de atenção à saúde humana | Q | 12 | 1.398 | 80 |
| 8 | Atendimento hospitalar (exceto urgências) | Q | 13 | 1.396 | 68 |
| 9 | Administração pública em geral | O | 4 | 1.290 | 333 |
| 10 | Seleção e agenciamento de mão de obra | N | 22 | 1.253 | 35 |
| 11 | Comércio atacadista de mercadorias em geral (alimentos) | G | 7 | 1.009 | 71 |
| 12 | Construção de rodovias e ferrovias | F | 23 | 912 | 28 |
| 13 | **Construção de edifícios** | F | **31** | 823 | 20 |
| 14 | Construção de estações e redes de distribuição de energia elétrica | D | 5 | 821 | 94 |
| 15 | Fabricação de artefatos de cerâmica e barro cozido para construção | C | 14 | 668 | 26 |

### 4.2 A ressalva decisiva: emergência ou reclassificação?

A subclasse nº 1 — *Regulação das atividades de saúde, educação e serviços sociais* (CNAE 8412-4) — é **atividade de prefeitura**. Ela "emerge" com 9.160 vínculos em 37 municípios, mediana de 175 empregados. Nenhuma nova indústria faz isso. O que acontece é que o ente municipal **migra seu CNAE** (tipicamente de *Administração pública em geral*, 8411-6, para 8412-4) e todo o quadro de servidores da saúde e educação "aparece" num setor até então inexistente.

O mesmo mecanismo explica **Ensino fundamental** (3.413 vínculos, mediana 153 — são as escolas municipais) e boa parte de **Atendimento hospitalar** e **Apoio à gestão de saúde**.

Por isso, a leitura correta **separa a seção O do restante**:

- **Seção O:** 72 pares, **12.249 vínculos** — praticamente toda emergência aqui é reclassificação. **Não é base econômica nova.**
- **Atividades de mercado (≥10, exclui O):** 1.079 pares, **45.229 vínculos**, 177 municípios, 383 subclasses.

Recomenda-se, na consolidação do painel, um **filtro explícito "excluir seção O"**, e um alerta nas seções P e Q quando a mediana de vínculos por município ultrapassar ~100 (assinatura de rede pública).

### 4.3 A emergência de mercado, depurada — por seção

| Seção | Pares ≥10 | Vínculos | Interpretação |
|---|---:|---:|---|
| G — Comércio | 256 | 9.509 | Adensamento do varejo/atacado; supermercados e atacado alimentar |
| Q — Saúde | 117 | 9.451 | Rede de saúde (parte pública, parte clínicas privadas) |
| P — Educação | 50 | 5.199 | Majoritariamente rede pública |
| C — Indústria de transformação | 151 | 4.562 | **Cerâmica vermelha, alimentos, confecção** |
| N — Administrativas | 77 | 3.814 | Terceirização de mão de obra |
| F — Construção | 117 | 3.495 | Rodovias, edifícios, redes |
| A — Agropecuária | 89 | 3.289 | **Milho, soja, apoio à agricultura** |
| J — Informação e comunicação | 66 | 2.982 | **SCM — provedores de internet** |

Dois vetores merecem destaque por serem **genuinamente novos e disseminados**:

- **Serviços de comunicação multimídia (SCM)** — provedores regionais de internet. Emergem com ≥10 vínculos em **47 municípios** (e aparecem na faixa 1–4 em outros 42). É a emergência mais **espacialmente difusa** do estado, e a única do setor J com essa penetração. Um candidato natural a cluster espacial na próxima rodada de Moran.
- **Fabricação de artefatos de cerâmica e barro cozido** — 668 vínculos em 14 municípios, mediana 26. Indústria de base local ligada à construção civil, com potencial de encadeamento.

### 4.4 Municípios: onde a emergência tem densidade

![Figura 4](figuras/fig4_top_municipios.png)

| Município | Setores emergentes ≥10 | Vínculos | Leitura |
|---|---:|---:|---|
| Parnaíba | 53 | 3.581 | Diversificada, majoritariamente de mercado |
| Teresina | 68 | 3.523 | Maior amplitude setorial do estado |
| Piripiri | 32 | 1.959 | Puxada por saúde hospitalar |
| Bom Jesus | 29 | 1.837 | Agronegócio + serviços |
| Floriano | 38 | 1.733 | Diversificada |
| Picos | 46 | 1.616 | Alta amplitude, densidade média |
| Uruçuí | 34 | 1.597 | Fronteira agrícola |
| Campo Maior | 22 | 1.554 | **Fortemente concentrada em seção O** |
| Buriti dos Lopes | 11 | 1.454 | **1.183 dos 1.454 vínculos = seção O** |
| Altos | 19 | 1.435 | Atacado alimentar |

**Buriti dos Lopes e Campo Maior são os exemplos didáticos da armadilha:** aparecem no topo do ranking bruto, mas seu "dinamismo" é quase inteiramente reclassificação administrativa. Depois de excluir a seção O, Buriti dos Lopes cai para ~270 vínculos emergentes.

Na outra ponta: **42 municípios (18,8% do estado) não possuem uma única subclasse emergente com 10 ou mais vínculos.** Toda a sua "emergência" cabe na faixa de 1 a 4.

![Figura 8](figuras/fig8_dispersao.png)

A dispersão amplitude × profundidade mostra o padrão: **a mediana municipal é de 15 subclasses emergentes**, mas a maioria delas soma pouquíssimos vínculos. Diversificação nominal sem densidade produtiva.

### 4.5 O que nasceu *de fato* depois de 2022 (coorte 1) e já é grande

Cruzando coorte × faixa, **296 pares** são simultaneamente **emergência recente** (ausentes até 2022) e **≥ 10 vínculos**, somando **23.878 vínculos em 135 municípios**. Sua composição:

| Seção | Pares | Vínculos |
|---|---:|---:|
| O — Administração pública | 34 | 8.017 |
| Q — Saúde | 62 | 7.115 |
| P — Educação | 15 | 2.918 |
| N — Administrativas | 25 | 1.467 |
| F — Construção | 39 | 1.061 |
| D — Eletricidade e gás | 8 | 681 |

Ou seja: **a emergência pós-2022 no Piauí é esmagadoramente pública ou parapública** (O + Q + P = 76% dos vínculos). Uma vez removida a seção O, o que resta de genuinamente novo e robusto é a **rede de saúde**, a **terceirização de mão de obra** e a **construção de infraestrutura elétrica** (Lagoa do Barro do Piauí, 408 vínculos — muito provavelmente canteiro de energia renovável).

---

## 5. As fontes IBGE: onde a potencialidade é de fato produtiva

Aqui o problema do "1 empregado" não existe. A leitura é direta em valor da produção.

![Figura 7](figuras/fig7_ibge.png)

### 5.1 PAM — lavouras (270 pares, 142 municípios, R$ 452,5 milhões)

| Cultura | Municípios novos | Valor total (R$ mil) | Maior município |
|---|---:|---:|---|
| **Soja em grão** | 17 | **221.427** | Barreiras do Piauí (118.985) |
| Milho em grão | 42 | 50.715 | Fronteiras (9.984) |
| Sorgo em grão | 7 | 49.394 | Uruçuí (20.253) |
| **Melão** | 2 | 48.974 | Pajeú do Piauí (47.678) |
| Algodão herbáceo | 8 | 33.045 | Sebastião Leal (24.990) |
| Melancia | 31 | 10.179 | — |
| Feijão em grão | 9 | 10.156 | — |
| Mandioca | 37 | 9.480 | — |

**Esta é a potencialidade T-1 economicamente mais significativa do estado.** A soja entra em 17 municípios que não a cultivavam, movimentando R$ 221 milhões — mais do que todo o emprego emergente de mercado da RAIS em valor econômico plausível. Somados soja + sorgo + algodão (R$ 303,9 milhões), tem-se o **avanço da fronteira agrícola dos Cerrados piauienses** (Uruçuí, Sebastião Leal, Barreiras do Piauí, Baixa Grande do Ribeiro), agora transbordando para municípios vizinhos.

O caso do **melão** é o mais concentrado do conjunto: dois municípios, R$ 49 milhões, praticamente todo em **Pajeú do Piauí**. Um evento produtivo singular que merece investigação de campo.

### 5.2 PPM — pecuária e aquicultura

Com a série de codornas corrigida, a PPM conta uma história coerente e interessante: **piscicultura**.

| Produto | Municípios novos | Valor (R$ mil) |
|---|---:|---:|
| Tambacu / tambatinga | 78 | 13.837 |
| Tilápia | 82 | 8.607 |
| Tambaqui | 84 | 5.690 |
| Mel de abelha | 27 | 4.871 |
| Camarão | 1 | 3.902 |
| Outros peixes | 66 | 3.205 |

A **aquicultura continental emerge em ~80 municípios** para cada espécie — uma difusão espacial notável, ainda que com valores modestos por município (mediana de R$ 22 a 110 mil). É o tipo de padrão que, agregado, pode formar **cluster espacial detectável** e que merece entrar na próxima rodada de Moran bivariado.

### 5.3 PEVS — extrativismo (76 pares, 41 municípios, R$ 2,2 milhões)

Escala marginal. Destaques: **carnaúba em pó / ceras** (R$ 534 mil, 5 municípios) e aromáticos/medicinais (R$ 253 mil). Não sustenta leitura de potencialidade econômica isolada, mas é relevante como **indicador de reativação de cadeias tradicionais**.

---

## 6. Recomendações para as próximas iterações

1. **Adotar a base depurada.** O arquivo `tabelas/t1_pares_final.csv` traz a coluna `flag` com três valores (`Emergência efetiva (candidata)`, `Artefato: código CNAE desativado`, `Artefato: migração de código CNAE`). Filtrar pela primeira antes de qualquer análise espacial. A antiga marcação de codornas foi dispensada porque a série foi corrigida na origem.

2. **Criar o filtro "seção O" no painel** e sinalizar visualmente subclasses de P e Q com mediana de vínculos > 100 — assinatura de reclassificação de ente público.

3. **Aplicar Moran local apenas às emergências candidatas com ≥ 5 vínculos** (faixas B, C e D), agregadas por seção CNAE quando o número de municípios copresentes for < 10. Os candidatos naturais a cluster: **SCM (J)**, **cerâmica vermelha (C)**, **soja/sorgo/algodão (PAM)** e **piscicultura (PPM)**.

4. **Considerar um índice de emergência ponderada** por município, do tipo `Σ log1p(estoque)` restrito à faixa ≥ 5, em vez de contagem simples de setores novos — corrige a distorção entre amplitude e densidade evidenciada na Figura 8.

---

---

## 7. Análise espacial LISA/Moran da emergência T-1

Esta seção aplica autocorrelação espacial à base depurada (5.673 emergências candidatas), respondendo à pergunta que a análise descritiva deixa em aberto: **a emergência de um setor é um evento isolado ou forma manchas contíguas no território?** Um cluster Alto-Alto indica que municípios com forte emergência de determinada atividade estão cercados por vizinhos igualmente fortes — assinatura de um processo regional, não de um acaso municipal.

### 7.1 Nota sobre a malha municipal

A análise usa a malha oficial **IBGE Malha Municipal Digital 2025** (`PI_Municipios_2025.shp`, 224 municípios, EPSG:4674/SIRGAS 2000), com os campos `CD_MUN → cod_ibge` e `NM_MUN`. Todos os 224 municípios — inclusive Nazária (IBGE 2206720) — batem exatamente com os nomes da base de potencialidades, sem necessidade de normalização ou reconstrução geométrica. A contiguidade Queen é calculada sobre os limites administrativos reais.

### 7.2 Parâmetros

Mantidos os padrões do projeto: contiguidade **Queen row-standardized**, transformação **log1p** da intensidade, **999 permutações**, **seed 42**, significância **p < 0,05**, mínimo de **10 municípios** presentes para avaliação univariada e **5 copresentes** para pares bivariados. A intensidade é o estoque no ano final (vínculos para RAIS; valor da produção ou rebanho para IBGE), tratada **coluna a coluna**, já que só é comparável dentro da mesma subclasse. Clusters Baixo-Baixo formados por ausência conjunta (município zero cercado de zeros) foram descartados por não informarem sobre emergência.

### 7.3 Resultado univariado: 52 setores com estrutura espacial

Das **177 subclasses** com presença em ≥ 10 municípios, **50 (28%) apresentam I de Moran global significativo**. O I médio dessas é 0,064, mas os líderes são muito mais concentrados:

![Figura 10](figuras/fig10_lisa_resumo.png)

| Subclasse | Fonte/Seção | Municípios | I global | Municípios AA |
|---|---|---:|---:|---:|
| Milho em grão | IBGE/PAM | 42 | 0,475 | 27 |
| Mandioca | IBGE/PAM | 37 | 0,468 | 27 |
| Cultivo de milho | A – Agropecuária | 23 | 0,451 | 7 |
| Tambacu tambatinga | IBGE/PPM | 74 | 0,219 | 20 |
| Fava em grão | IBGE/PAM | 32 | 0,188 | 10 |
| Outros peixes | IBGE/PPM | 64 | 0,175 | 16 |
| Obras de terraplenagem | F – Construção | 22 | 0,162 | 3 |
| **SCM (provedores de internet)** | J – Info./Com. | — | 0,08 | 10 |
| Construção de rodovias e ferrovias | F – Construção | 53 | 0,113 | 7 |

**A estrutura espacial mais forte é agropecuária** — mandioca, milho e as espécies de piscicultura formam manchas nítidas. Isso é coerente: cultivo e criação obedecem a solo, clima e bacias hidrográficas, que são contínuos no espaço. Atividades de serviço e comércio, sujeitas a decisões empresariais dispersas, têm I bem menor — mas o **SCM se destaca como o único serviço com clusterização relevante**, confirmando a hipótese levantada na análise descritiva: a expansão dos provedores regionais de internet segue corredores, não pontos isolados.

### 7.4 Os municípios-núcleo da emergência

Cruzando todos os clusters Alto-Alto, emergem **hubs recorrentes** — municípios que são núcleo de emergência para muitas subclasses ao mesmo tempo:

| Município | Nº de subclasses em que é núcleo AA | Leitura |
|---|---:|---|
| Barras | 18 | Polo do norte-central, difusão múltipla |
| José de Freitas | 15 | Entorno metropolitano de Teresina |
| Batalha | 12 | Norte, agropecuária + piscicultura |
| Baixa Grande do Ribeiro | 12 | Núcleo do Cerrado (soja, milho) |
| Altos | 11 | Região metropolitana |
| Ribeiro Gonçalves | 9 | Fronteira agrícola do sudoeste |
| Gilbués | 7 | Cerrado sul |

Dois eixos geográficos se desenham: **o entorno metropolitano de Teresina** (José de Freitas, Altos, Batalha — piscicultura e serviços) e **a fronteira agrícola do sudoeste/Cerrado** (Baixa Grande do Ribeiro, Ribeiro Gonçalves, Gilbués — grãos).

Os mapas a seguir ilustram os quatro vetores-chave.

![SCM](figuras/uni_scm.png)

![Soja](figuras/uni_soja.png)

![Tilápia](figuras/uni_tilapia.png)

![Cerâmica](figuras/uni_ceramica.png)

### 7.5 Resultado bivariado: 100 associações espaciais entre setores emergentes

O Moran bivariado testa se a emergência de X num município se associa à emergência de Y na sua vizinhança — revelando **encadeamentos produtivos que se difundem juntos**. Foram testadas seis âncoras (SCM, cerâmica, soja, milho, tilápia, tambacu) contra todas as demais subclasses; **100 pares** resultaram significativos com ao menos um núcleo Alto-Alto. Os mais fortes:

| Âncora X | Vizinhança Y | Copres. | I bivariado | Núcleos AA |
|---|---|---:|---:|---:|
| Milho em grão | **Mandioca** | 17 | 0,271 | 15 |
| Tambacu | Corretagem de imóveis | 5 | 0,191 | 9 |
| Milho | Assistência social sem alojamento | 6 | 0,189 | 12 |
| Tambacu | **Produção de ovos** | 9 | 0,177 | 10 |
| Tambacu | **Hipermercados** | 8 | 0,177 | 10 |
| Cerâmica | Lojas de conveniência | 6 | 0,174 | 6 |
| Tambacu | **Fabricação de alimentos para animais** | 10 | 0,126 | 11 |
| Tilápia | **Tambacu tambatinga** | 28 | 0,093 | 11 |
| Tilápia | **Cerâmica vermelha** | 11 | 0,090 | 8 |

Três encadeamentos merecem destaque analítico:

1. **Grãos do Cerrado (Milho ↔ Mandioca, I = 0,271)** — a associação bivariada mais forte de todo o conjunto. Onde o milho emerge, a mandioca emerge no entorno: é o avanço conjunto da lavoura temporária na mesma fronteira agrícola, o padrão espacialmente mais estruturado das potencialidades T-1.

2. **Complexo da piscicultura (Tambacu ↔ ração animal ↔ produção de ovos; Tilápia ↔ Tambacu).** A criação de peixes emerge acompanhada, na vizinhança, de **fabricação de alimentos para animais** e **produção de ovos** — indício de um arranjo produtivo local nascente, em que a aquicultura puxa cadeias de fornecimento a montante. Este é o achado com maior interesse para política de desenvolvimento: não é um setor isolado, é um **cluster agroindustrial em formação** no entorno de Teresina e no norte do estado.

![Milho × Mandioca](figuras/biv_milho_mandioca.png)

![Tambacu × ração animal](figuras/biv_tambacu_racao.png)

![Tilápia × Tambacu](figuras/biv_tilapia_tambacu.png)

3. **Cerâmica ↔ piscicultura (I = 0,090).** A cerâmica vermelha e a tilápia compartilham o mesmo cinturão espacial — ambas dependem de várzeas e recursos hídricos. A coincidência sugere um território (o entorno metropolitano e o médio Parnaíba) que concentra simultaneamente indústria de base e aquicultura emergentes.

### 7.6 Síntese espacial

A emergência T-1 do Piauí, uma vez depurada e mapeada, não é aleatória: **concentra-se em dois territórios funcionais**. O **sudoeste do Cerrado** (Baixa Grande do Ribeiro, Ribeiro Gonçalves, Gilbués, Bom Jesus) é o núcleo da emergência de grãos — soja, milho, sorgo, mandioca —, com a associação bivariada mais forte do conjunto. O **entorno metropolitano de Teresina e o norte** (José de Freitas, Altos, Batalha, Barras) é o núcleo de um **complexo aquícola-industrial nascente**, em que piscicultura, ração animal, cerâmica e comércio alimentar emergem de forma espacialmente acoplada. O SCM, por fim, é o único serviço com difusão espacial própria, seguindo corredores no norte-central.

Para a política regional, a leitura é direta: as potencialidades T-1 com maior densidade e maior estrutura espacial **não são as que aparecem no topo da contagem bruta de vínculos** (dominada por reclassificação administrativa), e sim os arranjos agro e aquícolas do Cerrado e do entorno de Teresina — territórios onde a emergência é, ao mesmo tempo, econômica, contígua e encadeada.

### 7.7 Arquivos gerados

- `out_lisa/moran_global_univariado.csv` — I global e contagem de quadrantes por subclasse (177 avaliadas).
- `out_lisa/lisa_univariado_clusters.csv` — municípios em cluster local significativo, por subclasse.
- `out_lisa/moran_bivariado_pares.csv` — 100 pares bivariados significativos.
- `out_lisa/lisa_bivariado_clusters.csv` — núcleos Alto-Alto bivariados.
- `figuras/uni_*.png`, `figuras/biv_*.png`, `figuras/fig10_lisa_resumo.png` — mapas e síntese.
- Scripts: `spatial_utils_t1.py`, `lisa_univariado.py`, `lisa_bivariado.py`, `mapas_lisa.py`.

---

## Anexo — Nota metodológica

- **Universo:** 6.727 pares município–subclasse classificados como T-1 (deduplicados por município × subclasse × fonte; verificou-se que o `Estoque_mun_ano_final` é idêntico entre as três janelas de ano-base, portanto a deduplicação não envolve escolha de valor).
- **Coorte de emergência** derivada do conjunto de janelas `ano_inicial` em que o par aparece como T-1.
- **Mapeamento CNAE 2.0:** as 806 subclasses da RAIS foram atribuídas a seções (A–S) por regras lexicais sobre a descrição oficial, com 121 atribuições revisadas manualmente; cobertura de 100%, sem resíduo "não classificado". O mapeamento é heurístico — erros pontuais em subclasses limítrofes são possíveis, mas não afetam a leitura agregada. Código em `cnae_map.py`.
- **Fontes:** RAIS (vínculos, ano final 2025), PAM/PPM/PEVS (IBGE, ano final 2024).
- **Scripts:** `analise_t1.py` (estratificação e tabelas), `sanitizar.py` (depuração de artefatos), `figuras.py` / `figuras2.py` (gráficos).
