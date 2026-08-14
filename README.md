# Mapa de Potencialidades Econômicas do Piauí — Painel Interativo

Painel interativo (dashboard) com o mapeamento de potencialidades produtivas dos 224 municípios e 12 Territórios de Desenvolvimento do Piauí, com base na tipologia de análise shift-share de Montanía et al. (2024).

## 🔗 Acesso ao painel

Depois de publicado, o painel ficará disponível em:

```
https://<SEU-USUARIO>.github.io/mapa-potencialidades-pi/
```

(substitua `<SEU-USUARIO>` pelo seu nome de usuário do GitHub — veja o passo a passo abaixo)

## 📁 Estrutura do repositório

```
.
├── index.html      # Painel completo (HTML autocontido, dados embutidos)
├── .nojekyll       # Impede que o GitHub Pages processe o site com Jekyll
└── README.md       # Este arquivo
```

O arquivo `index.html` é autocontido: os dados (objeto `DB`) e as imagens estão embutidos no próprio HTML, então não há dependência de arquivos externos além das fontes carregadas via Google Fonts.

## 🔄 Como atualizar o painel

Sempre que houver uma nova versão do dashboard (v7, v8...):

1. Substitua o arquivo `index.html` pela nova versão (renomeando o novo HTML para `index.html`).
2. Rode:
   ```bash
   git add index.html
   git commit -m "Atualiza painel para vX"
   git push
   ```
3. O GitHub Pages republica automaticamente em 1–2 minutos.

## 📌 Metodologia

Baseado na tipologia T1–T8/T-1 de Montanía et al. (2024), classificando setores segundo os componentes shift-share:
- **CE** — Efeito Competitivo
- **RIE** — Efeito Regional Industrial (Reestruturação Intra-Econômica)
- **RSE** — Efeito de Reestruturação Sistêmica

Fontes de dados: RAIS (MTE) e pesquisas IBGE (PAM, PPM, PEVS), janelas de comparação 2013, 2018 e 2022.
