# CLAUDE.md — Análise espacial dos setores produtivos do Piauí (shift-share)

**Leia antes o `CONTEXTO_PROJETO.md`**: estado atual, decisões, pendências e
"onde paramos". Atualize-o ao fim de cada etapa (o usuário dá `/clear` com
frequência). Colunas dos insumos, tipologia e estrutura interna do painel
(`DB`, `LISA`): `docs/REFERENCIA_DADOS_PAINEL.md`.

## O que é
Clusters espaciais (Moran global, LISA univariado e bivariado) dos resultados
shift-share dos 224 municípios do Piauí, com cada par município × subclasse
classificado pela tipologia de Montanía et al. (2024) (T1…T8, T-1). Os resultados
vão para um painel HTML autocontido: o publicado é o `index.html` da raiz (GitHub Pages,
estética CIET); as versões de trabalho ficam em `saidas/painel_potencialidades_vN.html`.
Idioma: **pt-BR** em tudo.

## Ambiente
- **uv** (não conda): `uv sync`, `uv run python scripts/<x>.py`, `uv run pytest`.
- Python 3.12 · **esda 2.10.0** fixado (as permutações do LISA mudam entre versões) · `pandas<3` · sem numba.
- Shell do Windows: o PowerShell é o padrão; no Bash, use `-X utf8` ou `sys.stdout.reconfigure(encoding='utf-8')`.

## Arquitetura
```
index.html        painel publicado no GitHub Pages (gerado pelo 23; não editar à mão)
dados/            insumos (CSV consolidados, matrizes ORS, geo/ com malha, sedes e rodovias)
scripts/comum.py  ÚNICA fonte de caminhos, parâmetros e funções compartilhadas
scripts/NN_*.py   etapas numeradas (ordem em executar_pipeline.py --listar)
robustez/         pickles intermediários (regeneráveis, fora do git)
saidas/           produtos: painéis, CSV, xlsx, docx; tab/ e fig/ do relatório
docs/             metodologia e textos escritos à mão
testes/           regressão contra os resultados publicados
legado/           versões antigas e arquivos substituídos (não apagar sem OK)
t1_emergentes/    subprojeto das emergentes T-1 (escopo tm1 do painel)
```
Etapas principais: 00/08/00b (malha e matrizes W) → 12, 10, 16 (T1+T2) → 19, 14, 15, 17, planilha, js (relatório) → 20 → 21 (univariado de todos os setores → painel v7) → 22 (v8: abre em Clusters, Todos · Estoques) → 23 (`index.html` = base CIET `saidas/painel_ciet_base_v6.html` + dados e mudanças do v8). O 18 (painel v6) está **congelado**.

## Regras
- Nunca redefina `norm()`, caminhos ou parâmetros num script: importe de `comum`.
- Parâmetros: Queen padronizada por linha, 999 permutações, seed 42, p < 0,05; FDR BH com 9.999 permutações; robustez = mesmo quadrante nas 4 W alternativas (KNN-5, distância inversa, rede rodoviária, tempo ORS); mínimo de 10 municípios (univariado) e 5 copresentes (bivariado).
- **Invariante:** `LISA.paths`, `LISA.names`, cada `mapas[i].cats` e `DB.municipios` têm 224 posições na **mesma ordem** (alfabética com acento). `base.pkl` está na ordem de `norm()`; converta com `comum.reordenacao_painel` / `comum.para_cats`.
- Painel: nunca edite o HTML à mão. Gere uma **nova versão** (`_v8`…) por script, a partir da anterior, com `comum.ler_lisa_painel` / `gravar_lisa_painel`, e confirme que cada trecho substituído ocorre 1 vez. Mudança de painel que deva ir ao ar também entra no 23 (que preserva a estética CIET).
- Estoques de fontes/unidades diferentes não se somam; o LISA é sempre por subclasse.
- CSV de saída: `;`, decimal `,`, UTF-8 com BOM (`comum.CSV_OUT`). Consolidado shift-share: latin-1.
- Depois de refatorar ou trocar pacote: `uv run pytest` e `uv run ruff check` (só regras de bug; têm que passar).
- O HTML tem linhas de megabytes: use `grep -o` com contexto curto, nunca `cat`.
- Não apagar dados nem saídas publicadas sem OK; mova para `legado/`.
- Segredos (chave ORS) só em variável de ambiente.
- Git: este repositório é o do GitHub Pages (`matheusgirola/distribuicao-potencialidades-pi`, branch `main`); o push republica o painel. Commit e push só quando o usuário pedir.
