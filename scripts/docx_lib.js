/**
 * docx_lib.js — helpers para relatórios analíticos em ABNT.
 *
 * Requer: npm install docx
 * Uso:    const L = require('./scripts/docx_lib.js');
 *
 * Toda medida em twips (1 cm = 567). Tamanhos de fonte em meios-pontos (24 = 12 pt).
 * Veja references/docx.md para um exemplo completo.
 */

const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow,
  TableCell, WidthType, ShadingType, BorderStyle, ImageRun, PageBreak, TableOfContents,
} = require('docx');

const FONT = 'Times New Roman';

// Largura útil da página A4 com margens ABNT (3 cm esq. + 2 cm dir.), em twips.
const USABLE = 9071;

const NONE = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const LINE = (sz) => ({ style: BorderStyle.SINGLE, size: sz, color: '000000' });

let FONTE_PADRAO = 'Fonte: elaboração própria.';

/** Define a fonte usada quando Fonte() é chamada sem argumento. */
function setFontePadrao(txt) { FONTE_PADRAO = txt; }

// ---------------------------------------------------------------- corpo

/**
 * Parágrafo de corpo: justificado, entrelinhas 1,5, recuo 1,25 cm.
 * opts: { after, before, line, size, align, noIndent, bold, italics }
 * Use after:0 no parágrafo que antecede um título de tabela/figura.
 */
function P(text, opts = {}) {
  return new Paragraph({
    alignment: opts.align || AlignmentType.JUSTIFIED,
    spacing: {
      line: opts.line || 360,
      after: opts.after === undefined ? 0 : opts.after,
      before: opts.before || 0,
    },
    indent: opts.noIndent ? undefined : { firstLine: 708 },
    children: [new TextRun({
      text, font: FONT, size: opts.size || 24,
      italics: !!opts.italics, bold: !!opts.bold,
    })],
  });
}

/** Título de seção. level 1 = primária (caixa alta), level 2 = secundária. */
function H(text, level) {
  return new Paragraph({
    heading: level === 1 ? HeadingLevel.HEADING_1 : HeadingLevel.HEADING_2,
    alignment: AlignmentType.LEFT,
    spacing: { line: 360, before: 360, after: 240 },
    children: [new TextRun({
      text, font: FONT, size: 24, bold: true,
      allCaps: level === 1, color: '000000',
    })],
  });
}

// ------------------------------------------------- títulos, fontes, notas

/**
 * Título de tabela ou figura — sempre ACIMA do elemento.
 * brk=true força início de página nova (use em tabelas longas).
 * keepNext impede que o título fique órfão no fim da página.
 */
function Titulo(text, brk) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { line: 240, before: 240, after: 60 },
    pageBreakBefore: !!brk, keepNext: true, keepLines: true,
    children: [new TextRun({ text, font: FONT, size: 22 })],
  });
}

/** Fonte — sempre ABAIXO do elemento. Sem argumento, usa a fonte padrão. */
function Fonte(text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { line: 240, before: 60, after: 300 },
    children: [new TextRun({ text: text || FONTE_PADRAO, font: FONT, size: 20 })],
  });
}

/** Nota metodológica — entre o elemento e a fonte. */
function Nota(text) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 240, before: 0, after: 60 },
    children: [new TextRun({ text, font: FONT, size: 20 })],
  });
}

// ---------------------------------------------------------------- tabela

/**
 * Tabela a partir de uma matriz (primeira linha = cabeçalho).
 * opts:
 *   size        tamanho da fonte em meios-pontos (padrão 16 = 8 pt)
 *   firstW      largura da primeira coluna em twips; as demais dividem o resto
 *   widths      larguras explícitas de todas as colunas (soma deve dar USABLE)
 *   headerRows  nº de linhas de cabeçalho (padrão 1) — repetem a cada página
 *   boldRows    índices (base 0) de linhas em negrito, p.ex. totais
 *   leftAll     alinha todas as células à esquerda
 *
 * Estilo: sem bordas verticais; linha superior e inferior grossas, linha fina
 * sob o cabeçalho. É o padrão de tabela científica e o que o IBGE usa.
 */
function mkTable(rows, opts = {}) {
  const fsz = opts.size || 16;
  const ncol = rows[0].length;
  let widths = opts.widths;
  if (!widths) {
    const first = opts.firstW || Math.round(USABLE * 0.26);
    const rest = Math.floor((USABLE - first) / (ncol - 1));
    widths = [USABLE - rest * (ncol - 1)].concat(Array(ncol - 1).fill(rest));
  }
  const headerRows = opts.headerRows || 1;
  const trs = rows.map((r, i) => {
    const isHead = i < headerRows;
    const isLast = i === rows.length - 1;
    const bold = isHead || (opts.boldRows || []).includes(i);
    return new TableRow({
      tableHeader: isHead,
      children: r.map((cellText, j) => new TableCell({
        width: { size: widths[j], type: WidthType.DXA },
        shading: isHead ? { type: ShadingType.CLEAR, fill: 'E8E8E8', color: 'auto' } : undefined,
        margins: { top: 40, bottom: 40, left: 60, right: 60 },
        borders: {
          top: (isHead && i === 0) ? LINE(8) : NONE,
          bottom: (i === headerRows - 1) ? LINE(6) : (isLast ? LINE(8) : NONE),
          left: NONE, right: NONE,
        },
        verticalAlign: 'center',
        children: [new Paragraph({
          alignment: (j === 0 || opts.leftAll) ? AlignmentType.LEFT : AlignmentType.CENTER,
          spacing: { line: 200, before: 0, after: 0 },
          children: [new TextRun({ text: String(cellText), font: FONT, size: fsz, bold })],
        })],
      })),
    });
  });
  return new Table({
    columnWidths: widths,
    width: { size: USABLE, type: WidthType.DXA },
    rows: trs,
  });
}

// ---------------------------------------------------------------- figura

/**
 * Figura centralizada. `sizes` é o dicionário {nome: {w, h}} em pixels,
 * gerado por scripts/figuras.py (função salvar_dimensoes).
 */
function Fig(name, dir, sizes) {
  const s = sizes[name];
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 0 },
    children: [new ImageRun({
      type: 'png',
      data: fs.readFileSync(`${dir}/${name}.png`),
      transformation: { width: s.w, height: s.h },
    })],
  });
}

// -------------------------------------------------------- capa e sumário

/** Capa. sub2 e rodape são opcionais. */
function capa(titulo, subtitulo, tipo, fonteDados, local) {
  const out = [];
  const centro = (text, size, bold, after) => new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after, before: 0 },
    children: [new TextRun({ text, font: FONT, size, bold: !!bold })],
  });
  out.push(new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { before: 2400, after: 240 },
    children: [new TextRun({ text: titulo, font: FONT, size: 32, bold: true })],
  }));
  if (subtitulo) out.push(centro(subtitulo, 26, false, 1200));
  if (tipo) out.push(centro(tipo, 24, false, 120));
  if (fonteDados) out.push(centro(fonteDados, 22, false, 2400));
  if (local) out.push(centro(local, 24, false, 0));
  out.push(new Paragraph({ children: [new PageBreak()] }));
  return out;
}

/**
 * Sumário automático. Fica vazio até o usuário atualizar o campo no Word
 * (botão direito > Atualizar campo, ou Ctrl+A e F9) — avise isso na entrega.
 */
function sumario() {
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { after: 360 },
      children: [new TextRun({ text: 'SUMÁRIO', font: FONT, size: 24, bold: true })],
    }),
    new TableOfContents('Sumário', { hyperlink: true, headingStyleRange: '1-2' }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

/** Referência bibliográfica: sem recuo, entrelinhas simples, separadas por espaço. */
function referencia(text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT, spacing: { line: 240, after: 240 },
    children: [new TextRun({ text, font: FONT, size: 24 })],
  });
}

/** Quebra de página avulsa. */
function quebra() {
  return new Paragraph({ children: [new PageBreak()] });
}

// ---------------------------------------------------------------- saída

/** Monta o documento com margens ABNT em A4 e grava no caminho indicado. */
function montarDocumento(children, caminho) {
  const doc = new Document({
    styles: { default: { document: { run: { font: FONT, size: 24 } } } },
    sections: [{
      properties: {
        page: {
          size: { width: 11906, height: 16838 },              // A4
          margin: { top: 1701, right: 1134, bottom: 1134, left: 1701 }, // 3/2/2/3 cm
        },
      },
      children,
    }],
  });
  return Packer.toBuffer(doc).then((b) => {
    fs.writeFileSync(caminho, b);
    console.log('gravado:', caminho);
  });
}

module.exports = {
  P, H, Titulo, Fonte, Nota, mkTable, Fig, capa, sumario, referencia, quebra,
  montarDocumento, setFontePadrao, FONT, USABLE,
};
