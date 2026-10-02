# CONTEXTO DO PROJETO — arquivo vivo

Estado, decisões e pendências. **Atualize ao fim de cada etapa.** Regras e
arquitetura estáveis ficam no `CLAUDE.md`; aqui fica o que muda.

Última atualização: 02/10/2026.

---

## 1. Onde paramos

### Tarefas da rodada de 29/09/2026 (pedido do usuário)

1. **Organizar o projeto para robustez e reprodutibilidade**
   - [x] Pastas da raiz reorganizadas, só por movimentação (nada apagado; ver §5).
   - [x] Módulo comum `scripts/comum.py`: caminhos, parâmetros, `norm`, leitura, deduplicação, matriz, LISA, leitura e gravação do `LISA` do painel.
   - [x] Scripts ativos refatorados para usar o `comum`. Bugs do 10 corrigidos. Caminhos `/mnt` e `/home/claude` removidos (incluindo `t1_emergentes/`).
   - [x] Ambiente **uv** (`pyproject.toml` + `uv.lock`), Python 3.12, esda 2.10.0.
   - [x] Testes de regressão (`testes/test_regressao.py`, `uv run pytest`).
   - [x] Executor `scripts/executar_pipeline.py` (logs em `logs/`).
   - [x] `.gitignore` criado. (Em 02/10 o projeto passou para o repositório do GitHub Pages; ver abaixo.)
   - [x] Chave do ORS retirada do código (`extrair_matriz_ors.py`). Agora só via variável `ORS_API_KEY`.
   - [x] README.md novo, CLAUDE.md curto e `docs/REFERENCIA_DADOS_PAINEL.md` (material de referência do antigo PROJECT_CONTEXT, corrigido).
2. **Análise espacial univariada para TODOS os setores** (sem bivariado) + painel
   - [x] `scripts/20_univariado_todos.py`, com três variáveis: estoque, ganhos CE+RIE e perdas CE+RIE.
   - [x] `scripts/21_painel_v7.py` → `saidas/painel_potencialidades_v7.html` (3,03 MB, 2.261 mapas = 2.022 do v6 intactos + 143 `todest` + 35 `todganho` + 61 `todperda`). Seletor de escopo em grade; Bivariado desativado nos escopos "Todos"; cabeçalho com 1.122 subclasses.
   - [x] Testes do v7 e dos escopos "todos" (nenhum Alto em ausentes; ganhos e perdas particionam).
   - [x] v7 validado no navegador: 6 escopos, busca, botão Bivariado e 0 erros no console. Servidor: `.claude/launch.json` → "painel". A tela do painel não desenha, então a validação é feita por JavaScript no DOM.
   - [x] §3 com os números finais.

### 02/10/2026
- [x] ruff só com regras de bug (ver §2).
- [x] **Painel v8** (`scripts/22_painel_v8.py`): igual ao v7, mas abre na aba Clusters Espaciais com o escopo **Todos · Estoques** selecionado (Bivariado já desativado na abertura). Validado no navegador: 143 mapas listados, troca de escopo e aba Shift-Share funcionando, 0 erros no console. Teste `test_painel_v8`.
- [x] **Painel publicado (CIET)**: o `index.html` do repositório `Desktop/Repositorios/distribuicao-produtiva-pi` (GitHub Pages `matheusgirola/distribuicao-potencialidades-pi`) é o v6 com estética CIET (paleta, logo, filtro "Período de destaque", estoque final no tooltip, escopo inicial T1+T2). Dados idênticos ao v6. Base guardada em `saidas/painel_ciet_base_v6.html` (commit ef51b7d). `scripts/23_painel_ciet_v8.py` aplica os dados e as mudanças do v7/v8 → `saidas/painel_ciet_v8.html`, copiado para o `index.html` do repositório (não commitado). Validado no navegador.
- [x] **Projeto transferido para o repositório do Pages** `Desktop/Repositorios/distribuicao-produtiva-pi` (o versionamento passa a ser lá). A pasta antiga `Desktop/Python/Analise-Espacial-Shift-Share` ficou intacta como cópia de segurança. README e `.gitignore` mesclados (o README mantém o link do painel no topo). O 23 grava direto no `index.html` da raiz (`comum.INDEX_PAGES`). O servidor do `.claude/launch.json` agora serve a raiz (painel em `/index.html`, versões em `/saidas/`). O git versiona ~72 MB (maior arquivo 6 MB); o CSV de 116 MB segue fora. **Commit e push pendentes de OK do usuário**, incluindo decidir o que pode ficar público (o Pages serve todo arquivo versionado).

**Rodada de 29/09 concluída.** Próximos passos possíveis (a decidir com o usuário):
- escrever a seção de resultados dos escopos "Todos" no relatório (docs/) e/ou na planilha;
- bivariado restrito, por exemplo só entre as subclasses que entraram nos escopos "Todos" (143 + 35 + 61);
- trocar o `cnae_map` heurístico pela API CNAE do IBGE;
- reexecutar 19/14/15/17/planilha no uv e conferir contra o xlsx e o docx publicados (precisa de Node para o docx).

### Pendências abertas (fora desta rodada)
- **2 mapas CE+RIE do v6 não se reproduzem** com o CSV local de shift-share: "Comércio varejista de artigos do vestuário e acessórios" e "Padaria e confeitaria com predominância de revenda". O p recalculado fica entre 0,12 e 0,49 onde o painel marca significância; `npres` e `n_aa` batem. Hipótese: foram gerados com uma versão ligeiramente diferente do consolidado. Os testes declaram a exceção (`CERIE_V6_NAO_REPRODUZ`). Os mapas do v6 foram mantidos como estavam.
- Node não está instalado na máquina, então `gerar_relatorio_unificado.js` (docx) não roda aqui.
- Etapas 19, 14, 15, 17 e da planilha **não** foram reexecutadas nesta rodada (10 e 16 foram, e reproduzem).
- Mapeamento subclasse → seção CNAE (`scripts/cnae_map.py`) é **heurístico** (regex + overrides). Alternativa exata: API CNAE do IBGE (`servicodados.ibge.gov.br/api/v2/cnae/subclasses`), ainda não usada.
- Temporários do Word apagados em 29/09 com o OK do usuário.
- O script 14 tinha `n05 = 6042; nfdr = 4032` fixos no código. O 10 reproduz exatamente esses valores; o ideal é ler do `t1t2_v2_extra.pkl`.

---

## 2. Decisões (com motivo)

| Data | Decisão | Motivo |
|---|---|---|
| 29/09 | Ambiente de referência = **uv, esda 2.10.0, sem numba** | Reproduz 54/54 mapas T1+T2 e 26/28 CE+RIE do painel v6, e os números dos relatórios (sigQ = 5.991). O conda base (esda 2.8.1) usa outras permutações: 204/240 LISA divergem na margem de p = 0,05 (I e quadrante iguais). |
| 29/09 | `t1t2_5w_estoque.pkl`, `resumo_5w.pkl` e `concordancia_T1T2_5matrizes.csv` regerados no uv | A versão local (11/08) tinha sido feita com esda 2.8.1 e não batia com o painel. Os antigos estão em `legado/robustez_esda281/`. |
| 29/09 | Moran global com `np.random.seed(42)` antes de cada chamada (`comum.moran_global`) | Tornar o pseudo p determinístico. Verificado: o conjunto de subclasses com I significativo não muda (54 T1+T2, 28 CE+RIE). |
| 29/09 | `n_jobs=1` no `Moran_Local` | No Windows o paralelo é mais lento e o resultado é o mesmo. |
| 29/09 | `pandas<3` | O pandas 3 muda o dtype de texto e o copy-on-write; não vale o risco agora. |
| 29/09 | "Todos os setores" = todas as tipologias (T1…T8, T-1), mínimo de 10 municípios presentes | Pedido do usuário; análise **só univariada** (o bivariado teria ~10^5 pares). |
| 29/09 | Estoque "todos": presença = estoque final > 0 | 5.951 linhas do consolidado têm estoque final 0 (setor desapareceu). |
| 29/09 | CE+RIE "todos": deduplicação pelo **máximo** entre anos-base (convenção dos escopos T1+T2) | Escolha do usuário. Tem viés otimista, documentado. |
| 29/09 | CE+RIE "todos" separado em **ganhos** (log1p(CE+RIE>0)) e **perdas** (log1p(\|CE+RIE<0\|)) | Com o sinal, o ausente (0) fica acima da média em 183/290 subclasses, e 91,5% dos Alto-Alto eram municípios **sem** o setor. Separado, o artefato cai a 0%. Escolha do usuário. |
| 29/09 | Critério para o mapa entrar no painel (escopos "todos"): I global signif. **ou** ≥ 3 núcleos AA **robustos às 4 W alternativas** | O AA nominal é ruidoso (≈5% de 224 municípios saem significativos por acaso; no CE+RIE com sinal, a mediana era de 9 AA entre subclasses sem padrão global). Escolha do usuário. |
| 29/09 | Painel novo = **v7** gerado a partir do v6 (que fica congelado) | Convenção de versões. O script 18 regravaria o v6 e fica marcado como "congelado" no executor. |
| 29/09 | Seção CNAE dos mapas novos via `cnae_map.py` (IBGE/<fonte> para PAM/PPM/PEVS) | Mais informativo que "MTE/RAIS" para tudo. |
| 02/10 | Painel abre em **Clusters · Todos · Estoques** (v8) | Pedido do usuário: é o escopo principal. A aba Shift-Share continua acessível como segunda opção. |
| 02/10 | **ruff só com regras de bug** (E9, F63, F7, F82, F811, B; sem B007/B008/B905), fora `legado/`, `esda_aulas/`, `robustez/`, `saidas/` | Pedido do usuário: nada de estilo. Passa limpo; o único achado (B023 em `12_t1t2_5w.py`) era falso positivo e foi marcado com `noqa`. |

---

## 3. Resultados da univariada "todos" (script 20, 29/09)

| Variável | Subclasses | Elegíveis (≥10 mun.) | I global signif. | No painel | Só por hotspots robustos | LISA sig. Queen | Pós-FDR | Robustos 4W |
|---|---|---|---|---|---|---|---|---|
| Estoque | 972 | 278 | 125 | 143 | 18 | 13.801 | 9.066 | 2.893 (21,0%) |
| Ganhos CE+RIE | 682 | 97 | 34 | 35 | 1 | 4.432 | 2.937 | 609 (13,7%) |
| Perdas CE+RIE | 946 | 216 | 58 | 61 | 3 | 10.506 | 7.904 | 1.424 (13,6%) |

- **Estoque:** maiores I para arroz em casca (0,770), babaçu, mel, oleaginosos, cera e pó de carnaúba, caprinos e ovinos. Municípios com mais núcleos AA robustos: Altos, União, José de Freitas, Lagoa Alegre e Teresina.
- **Perdas CE+RIE:** serviços de sepultamento (0,521), carvão vegetal de floresta nativa, soja e corretagem de imóveis. São aglomerados de perda competitiva, em geral fora de T1/T2.
- **Ganhos CE+RIE:** cultivo de arroz, hotéis, promoção de vendas, frangos, soja e bovinos de corte.

Saídas: `saidas/todos_moran_global_<var>.csv`, `saidas/todos_lisa_municipios_<var>.csv` e `robustez/todos_uni_<var>.pkl`.

---

## 4. Reprodutibilidade: fatos verificados

- `uv run pytest`: **12 testes passam** (29/09). `executar_pipeline.py todos testes` roda do zero em cerca de 3 min.
- O script 10 reproduz os valores fixos do 14 (6.042 nominais, 4.032 pós-FDR). O CSV de pares pós-FDR é idêntico ao publicado (937 pares); só mudava a ordem dos empates, agora determinística.
- O bivariado global vetorizado (RNG do numpy) é idêntico entre esda 2.8.1 e 2.10.0.
- `testes/diagnosticos/diag_versoes_esda.py` mede a divergência entre versões do esda.
- O `numba` não está no ambiente. Instalá-lo pode mudar o caminho de código das permutações do esda: rode os testes antes de adicionar.
- `DB.municipios` e `LISA.names` estão na mesma ordem (alfabética com acento); `base.pkl` está em ordem de `norm()`. Use `comum.reordenacao_painel`.
- No `LISA.mapas`, `I`, `n_aa` e `npres` são **números** (o antigo PROJECT_CONTEXT dizia strings, o que estava errado).

---

## 5. Reorganização de 29/09 (para achar arquivos antigos)

- `dados/geo/` ← `PI_limites_municipais_2025/`, `PI_localidades/`, `RODOVIAS/`, `Localidades_UFs_gpkg.zip`, `LEIA-ME.txt` (renomeado para `LEIA-ME_IBGE.txt`).
- `dados/ors_progresso.npz` ← raiz.
- `saidas/` ← painéis v5/v6, xlsx, docx integrado, CSVs de pares/duplo núcleo/concordância (antes em `outputs/`).
- `docs/` ← Metodologia (md/html), metodologia_clusters_espaciais, adendos, limitações, relatório T-1. `docs/relatorios/` ← docx `_1408` (versão editada à mão).
- `legado/` ← READMEs antigos, INSTRUCOES, report*.md, overview*.png, tabelas *_ss antigas, docx antigos, `Metodologia.docx` (0 bytes), `PROJECT_CONTEXT.md` original, cópias duplicadas de `t1_emergentes` (CSV e malha, idênticos por md5), pickles do esda 2.8.1.
- `scripts/legado/` ← 01, 02, 03, 09, 13b (históricos, com caminhos antigos).
- `scripts/ferramentas/montar_arvore.py` ← `montar_arvore_folder.py`.
- `scripts/cnae_map.py` ← `t1_emergentes/cnae_map.py` (lá ficou um redirecionamento via importlib).
