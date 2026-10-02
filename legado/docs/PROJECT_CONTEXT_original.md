# CLAUDE.md — Mapa de Potencialidades do Piauí

Contexto essencial para trabalhar neste projeto. Leia antes de mexer nos arquivos.

## Visão geral

Diagnóstico de competitividade setorial dos **224 municípios do Piauí** via decomposição **shift-share**, com cada par (município × atividade) classificado pela tipologia regional de **Montanía et al. (2024)**. O resultado é consumido por um painel HTML estático (protótipo) com duas abas: tabela/KPIs dos resultados shift-share e mapas de clusters espaciais (LISA).

Idioma do projeto: **português (pt-BR)** — textos da interface, nomes de colunas, comentários e documentação.

## Arquivos

| Arquivo | O que é |
|---|---|
| `potencialidades_consolidado_v2.csv` | Base consolidada (50.513 linhas). Fonte de verdade dos resultados shift-share. |
| `painel_potencialidades_v6.html` | Painel autocontido (~2,8 MB). Dados embutidos como JSON em `const DB` e `const LISA`. Sem dependências JS externas; só Google Fonts. |

Não há, neste repositório, o pipeline que gera o CSV nem o cálculo do LISA — ambos foram produzidos fora daqui. Não tente "reproduzir" I de Moran ou clusters a partir do CSV sem as matrizes de vizinhança originais.

## CSV: `potencialidades_consolidado_v2.csv`

Formato: separador `;`, codificação **UTF-8 com BOM** (ler com `encoding='utf-8-sig'` no pandas, senão a 1ª coluna vira `\ufeffsubclasse`). Sem valores nulos. Sem linhas duplicadas; a chave única é `(subclasse, NM_MUN, ano_inicial)`.

| Coluna | Tipo | Conteúdo |
|---|---|---|
| `subclasse` | str | Atividade: produto IBGE (ex.: "Milho em grão", "Caprino") ou subclasse CNAE (RAIS). 1.122 distintas. |
| `classificacao_regiao` | str | Tipologia: `T1`…`T8` ou `T-1`. |
| `NM_MUN` | str | Nome do município (224, com acentos). |
| `Estoque_mun_ano_final` | int | Estoque no ano final (emprego, rebanho ou valor). |
| `Unidade_de_medida` | str | `pessoas`, `cabeças` ou `mil reais`. |
| `Fonte` | str | `RAIS`, `PPM`, `PAM`, `PEVS`. |
| `ano_inicial` | int | Ano-base da comparação: 2013, 2018 ou 2022. |
| `ano_final` | int | 2025 para RAIS; 2024 para as fontes IBGE. |

Relação fonte × unidade: RAIS → pessoas (1.049 subclasses); PAM e PEVS → mil reais; PPM → cabeças (rebanhos) ou mil reais (produtos de origem animal).

Atenção: estoques de fontes/unidades diferentes **não são somáveis**. Qualquer agregação deve ser feita dentro da mesma `Fonte` + `Unidade_de_medida`.

## Tipologia regional (Montanía et al., 2024)

Combina o sinal de três efeitos: **CE** (competitividade nacional), **RIE** (força dentro da economia municipal), **RSE** (dinamismo da economia municipal vs. nacional). Sinais na ordem CE / RIE / RSE:

| Tipo | Sinais | Leitura |
|---|---|---|
| T1 | + + + | Vantagem nacional e municipal, economia dinâmica. **Único tipo que entra no mapa físico de potencialidades.** |
| T2 | + + − | Competitivo nacional e municipal, economia menos dinâmica. |
| T3 | + − + | Competitivo nacional, fraco no município, economia dinâmica. |
| T4 | + − − | Competitivo só no nível nacional. |
| T5 | − + + | Forte no município, economia dinâmica, sem vantagem nacional. |
| T6 | − + − | Forte no município, economia lenta, sem vantagem nacional. |
| T7 | − − + | Sem vantagem, mas economia municipal dinâmica. |
| T8 | − − − | Sem vantagem e economia lenta. |
| T-1 | n/d | Emergente: estoque inicial zero, surgiu só no ano final. |

Ordem canônica de exibição: `T1, T2, …, T8, T-1`. Paleta verde (T1) → vermelho (T8), cinza-azulado para T-1 (variáveis CSS `--t1`…`--t8`, `--tm1`).

## Painel HTML: estrutura interna

Tudo está num único `<script>` inline. Blocos principais, em ordem:

**`const DB`** — dados compactados por índice (dicionários + linhas numéricas):

```js
DB = { subclasses:[...1122], municipios:[...224], fontes:['PAM','PEVS','PPM','RAIS'],
       unidades:['cabeças','mil reais','pessoas'], classes:['T-1','T1',...,'T8'],
       anos:[2013,2018,2022], rows:[[sub, cls, mun, estoque, fonte, uni, ano], ...] }
// COL = {SUB:0, CLS:1, MUN:2, EST:3, FON:4, UNI:5, ANO:6}
```

Dicionários em ordem alfabética (inclusive `classes`, por isso `T-1` é o índice 0). `ano_final` não é armazenado: é derivado por `anoFinal(r)` (RAIS → 2025, senão 2024).

**Aba de resultados** — `TINFO` (descrições/cores dos tipos), `state` (filtros: ano, classificação, município, busca de subclasse, ordenação, paginação), `apply()` → `renderKPIs()`, `renderCharts()`, `renderTable()`. Exporta CSV filtrado com BOM.

**`const LISA`** — mapas de clusters espaciais:

```js
LISA = { W:420, H:470,
         paths:[...224 SVG paths],   // mesma ordem de DB.municipios
         names:[...224],
         rotulos_cat:['Alto-Alto','Alto-Baixo','Baixo-Alto','Baixo-Baixo','Não signif.'],
         cores:['#c0392b','#e08e79','#7fb0d8','#2c6fbb','#eef1f4'],
         mapas:[ {tipo, esc, rotulo, titulo_full, secao, I, n_aa, npres, subt, cats:[224 ints 0–4]}, ... ] }
```

`tipo`: `uni` (univariado) ou `biv` (bivariado, "X × vizinhança de Y"). `esc` (escopo): `tm1` (Emergentes T-1; é o default quando ausente), `t1t2` (T1+T2 · Estoques), `cerie` (T1+T2 · CE+RIE do emprego RAIS). `secao`: `IBGE/PAM`, `IBGE/PEVS`, `IBGE/PPM`, `MTE/RAIS` ou seção CNAE ("C - Indústrias de transformação" etc.). Hoje são 2.022 mapas (1.890 bivariados). Campos numéricos `I`, `n_aa`, `npres` vêm como string.

Parâmetros metodológicos citados no painel: contiguidade Queen, `log1p`, 999 permutações, p < 0,05; nos escopos T1+T2, ★ marca pares que sobrevivem ao FDR (Benjamini–Hochberg, 9.999 permutações), com teste de robustez em matrizes alternativas (distância rodoviária e tempo de viagem via OpenRouteService/OSM).

**Invariante crítica:** `LISA.paths`, `LISA.names`, cada `mapas[i].cats` e `DB.municipios` têm 224 posições na **mesma ordem**. Qualquer reordenação de municípios quebra os mapas silenciosamente.

## Fluxo de trabalho recomendado

O HTML é grande demais para editar à mão/ler inteiro. Separe dados de código:

```python
import re, json
h = open('painel_potencialidades_v6.html', encoding='utf-8').read()
js = re.search(r'<script>(.*?)</script>', h, re.S).group(1)
a = js.find('{'); DB = json.loads(js[a:js.find('\n', a)].rstrip().rstrip(';'))
i = js.find('const LISA = ') + 13; LISA = json.loads(js[i:js.find('};\n', i) + 1])
```

Para regenerar `DB` a partir de um CSV novo: ler com pandas, montar dicionários ordenados (`sorted(unique)`), mapear cada linha para índices na ordem de `COL`, e substituir a linha `const DB = …;` no HTML via script (nunca por `str_replace` manual). Validar depois: nº de linhas, 224 municípios na mesma ordem de `LISA.names`, e que o painel abre sem erro no console.

Ao buscar no HTML, use `grep -o` com contexto limitado — linhas únicas têm megabytes e estouram o terminal.

## Problemas conhecidos

- O cabeçalho do painel mostra **"622 subclasses" fixo no HTML**, mas `DB.subclasses` tem 1.122. Deveria ser calculado (`DB.subclasses.length`) ou corrigido.
- `ano_final` difere por fonte (RAIS 2025 × IBGE 2024); comparações "mesmo período" entre fontes são aproximadas.

## Convenções

- Números formatados com `toLocaleString('pt-BR')` (milhar com ponto, decimal com vírgula).
- CSVs de saída: `;` como separador e BOM UTF-8 (compatível com Excel pt-BR).
- Fontes da interface: Space Grotesk (títulos), Inter (texto), JetBrains Mono (rótulos/código).
- Versões por sufixo no nome (`_v2`, `_v6`); ao alterar, crie nova versão em vez de sobrescrever.
