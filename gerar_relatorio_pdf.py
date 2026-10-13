from html import escape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.graphics.renderPDF import draw
from reportlab.platypus import (
    Flowable,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from svglib.svglib import svg2rlg


PASTA = Path(__file__).parent
FONTE = PASTA / "RELATORIO_TECNICO.md"
DESTINO = PASTA / "RELATORIO_TECNICO.pdf"

estilos_base = getSampleStyleSheet()
estilos = {
    "title": ParagraphStyle(
        "ReportTitle", parent=estilos_base["Title"], fontName="Helvetica-Bold",
        fontSize=22, leading=27, textColor=colors.HexColor("#06141c"),
        alignment=TA_CENTER, spaceAfter=14,
    ),
    "subtitle": ParagraphStyle(
        "ReportSubtitle", parent=estilos_base["Normal"], fontName="Helvetica",
        fontSize=12, leading=17, textColor=colors.HexColor("#536070"),
        alignment=TA_CENTER, spaceAfter=12,
    ),
    "h2": ParagraphStyle(
        "ReportH2", parent=estilos_base["Heading2"], fontName="Helvetica-Bold",
        fontSize=15, leading=19, textColor=colors.HexColor("#06141c"),
        spaceBefore=4, spaceAfter=11,
    ),
    "h3": ParagraphStyle(
        "ReportH3", parent=estilos_base["Heading3"], fontName="Helvetica-Bold",
        fontSize=11, leading=14, textColor=colors.HexColor("#a51e56"),
        spaceBefore=9, spaceAfter=5,
    ),
    "body": ParagraphStyle(
        "ReportBody", parent=estilos_base["BodyText"], fontName="Helvetica",
        fontSize=9.5, leading=14, textColor=colors.HexColor("#202630"),
        alignment=TA_LEFT, spaceAfter=7,
    ),
    "bullet": ParagraphStyle(
        "ReportBullet", parent=estilos_base["BodyText"], fontName="Helvetica",
        fontSize=9.2, leading=13, leftIndent=14, firstLineIndent=-9,
        textColor=colors.HexColor("#202630"), spaceAfter=4,
    ),
    "code": ParagraphStyle(
        "ReportCode", parent=estilos_base["Code"], fontName="Courier",
        fontSize=8.3, leading=11, leftIndent=8, rightIndent=8,
        backColor=colors.HexColor("#F0F3F6"), borderColor=colors.HexColor("#CCD8D3"),
        borderWidth=0.5, borderPadding=7, spaceBefore=4, spaceAfter=9,
    ),
    "tableCell": ParagraphStyle(
        "TableCell", parent=estilos_base["BodyText"], fontName="Helvetica",
        fontSize=7.8, leading=10, textColor=colors.HexColor("#202630"),
        spaceAfter=0,
    ),
    "tableHeader": ParagraphStyle(
        "TableHeader", parent=estilos_base["BodyText"], fontName="Helvetica-Bold",
        fontSize=7.8, leading=10, textColor=colors.white, spaceAfter=0,
    ),
}


def converter_inline(texto):
    texto = escape(texto)
    texto = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", texto)
    texto = re.sub(r"`(.+?)`", r'<font name="Courier">\1</font>', texto)
    texto = re.sub(
        r"(https?://[^\s<>]+)",
        r'<link href="\1" color="#176B87">\1</link>',
        texto,
    )
    return texto


def desenhar_pagina(canvas, documento, cabecalho="MGPEB | Aurora Siger | Relatório técnico"):
    canvas.saveState()
    largura, altura = A4
    capa = documento.page == 1
    canvas.setFillColor(colors.HexColor("#0c0b1e" if capa else "#F7F8FA"))
    canvas.rect(0, 0, largura, altura, fill=1, stroke=0)
    if capa:
        # Moldura de monitor e cores extraídas do painel HTML.
        canvas.setStrokeColor(colors.HexColor("#46f0ff"))
        canvas.setLineWidth(0.8)
        canvas.roundRect(13 * mm, 22 * mm, largura - 26 * mm,
                         altura - 49 * mm, 9, stroke=1, fill=0)
        canvas.setFillColor(colors.HexColor("#ff3d7f"))
        canvas.rect(13 * mm, 31 * mm, 3, 24, fill=1, stroke=0)
    canvas.setFont("Courier-Bold", 9)
    canvas.setFillColor(colors.HexColor("#c4fbff" if capa else "#06141c"))
    canvas.drawString(20 * mm, altura - 16 * mm, "AURORA SIGER")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(largura - 20 * mm, altura - 16 * mm, "FASE 02 | POUSO E ESTABILIZAÇÃO")
    canvas.setStrokeColor(colors.HexColor("#ff3d7f"))
    canvas.setLineWidth(2)
    canvas.line(20 * mm, altura - 21 * mm, 55 * mm, altura - 21 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.HexColor("#AAB8C6" if capa else "#536070"))
    canvas.drawString(20 * mm, 12 * mm, "CIÊNCIA DA COMPUTAÇÃO | FIAP | 2026")
    canvas.drawRightString(largura - 20 * mm, 12 * mm, f"{documento.page:02d}")
    canvas.restoreState()


class GraficoSVG(Flowable):
    """Redimensiona um SVG para caber no corpo da página mantendo a proporção."""

    def __init__(self, desenho, largura_maxima, altura_maxima):
        super().__init__()
        fator = min(largura_maxima / desenho.width, altura_maxima / desenho.height)
        self.desenho = desenho
        self.fator = fator
        self.width = desenho.width * fator
        self.height = desenho.height * fator
        self.keepWithNext = True  # Mantém o gráfico junto de sua legenda.

    def draw(self):
        self.canv.saveState()
        self.canv.scale(self.fator, self.fator)
        draw(self.desenho, self.canv, 0, 0)
        self.canv.restoreState()


def gerar(fonte=FONTE, destino=DESTINO, titulo="MGPEB - Relatório técnico"):
    fonte, destino = Path(fonte), Path(destino)
    texto = fonte.read_text(encoding="utf-8")
    documento = SimpleDocTemplate(
        str(destino), pagesize=A4,
        rightMargin=20 * mm, leftMargin=20 * mm,
        topMargin=23 * mm, bottomMargin=22 * mm,
        title=titulo,
        author="Equipe Aurora Siger",
    )
    elementos = []
    paragrafo = []
    linhas_tabela = []
    em_codigo = False
    capa = True
    linhas_codigo = []

    def estilo(nome):
        if not capa:
            return estilos[nome]
        cor = "#46C9F7" if nome in ("h3", "subtitle") else "#EDF4F8"
        return ParagraphStyle("Capa_" + nome, parent=estilos[nome], textColor=colors.HexColor(cor))

    def fechar_paragrafo():
        if paragrafo:
            conteudo = " ".join(item.strip() for item in paragrafo)
            elementos.append(Paragraph(converter_inline(conteudo), estilo("body")))
            paragrafo.clear()

    def fechar_tabela():
        if not linhas_tabela:
            return
        linhas = []
        for texto_linha in linhas_tabela:
            celulas = [celula.strip() for celula in texto_linha.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", celula) for celula in celulas):
                continue
            estilo_celula = estilos["tableHeader"] if not linhas else estilos["tableCell"]
            linhas.append([Paragraph(converter_inline(celula), estilo_celula) for celula in celulas])
        linhas_tabela.clear()
        if not linhas:
            return
        largura_celula = documento.width / len(linhas[0])
        tabela = Table(
            linhas,
            colWidths=[largura_celula] * len(linhas[0]),
            repeatRows=1,
            hAlign="LEFT",
        )
        tabela.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#06141c")),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C7D2CE")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F0F3F6")]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elementos.append(tabela)
        elementos.append(Spacer(1, 5))

    for linha in texto.splitlines():
        if linha.strip() == "<!-- PAGE BREAK -->":
            fechar_paragrafo()
            fechar_tabela()
            elementos.append(PageBreak())
            capa = False
            continue
        if linha.strip().startswith("```"):
            fechar_paragrafo()
            fechar_tabela()
            if em_codigo:
                elementos.append(Preformatted("\n".join(linhas_codigo), estilos["code"]))
                linhas_codigo.clear()
                em_codigo = False
            else:
                em_codigo = True
            continue
        if em_codigo:
            linhas_codigo.append(linha)
            continue
        if linha.strip().startswith("|") and linha.strip().endswith("|"):
            fechar_paragrafo()
            linhas_tabela.append(linha)
            continue
        fechar_tabela()
        if not linha.strip():
            fechar_paragrafo()
        elif linha.startswith("# "):
            fechar_paragrafo()
            elementos.append(Spacer(1, 22 * mm))
            elementos.append(Paragraph(converter_inline(linha[2:]), estilo("title")))
        elif linha.startswith("## "):
            fechar_paragrafo()
            tipo_estilo = "subtitle" if len(elementos) < 4 else "h2"
            elementos.append(Paragraph(converter_inline(linha[3:]), estilo(tipo_estilo)))
        elif linha.startswith("### "):
            fechar_paragrafo()
            elementos.append(Paragraph(converter_inline(linha[4:]), estilo("h3")))
        elif linha.startswith("- "):
            fechar_paragrafo()
            elementos.append(Paragraph("• " + converter_inline(linha[2:]), estilo("bullet")))
        elif re.match(r"^\d+\. ", linha):
            fechar_paragrafo()
            elementos.append(Paragraph(converter_inline(linha), estilo("bullet")))
        elif linha.startswith("!["):
            fechar_paragrafo()
            correspondencia = re.search(r"\]\(([^)]+\.svg)\)", linha)
            if correspondencia:
                caminho_svg = fonte.parent / correspondencia.group(1)
                desenho = svg2rlg(str(caminho_svg))
                if desenho is None:
                    raise ValueError(f"Não foi possível ler o gráfico: {caminho_svg}")
                elementos.append(GraficoSVG(desenho, documento.width, 210))
        else:
            paragrafo.append(linha)
    fechar_paragrafo()
    fechar_tabela()
    def pagina(canvas, doc):
        desenhar_pagina(canvas, doc, "Aurora Siger | " + titulo)
    documento.build(elementos, onFirstPage=pagina, onLaterPages=pagina)
    print(f"PDF gerado: {destino.name} ({documento.page} páginas)")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gera PDFs a partir dos relatórios Markdown do MGPEB.")
    parser.add_argument("--fonte", type=Path, default=FONTE)
    parser.add_argument("--destino", type=Path, default=DESTINO)
    parser.add_argument("--titulo", default="MGPEB - Relatório técnico")
    args = parser.parse_args()
    gerar(args.fonte, args.destino, args.titulo)
