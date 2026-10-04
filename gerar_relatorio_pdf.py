from html import escape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)


PASTA = Path(__file__).parent
FONTE = PASTA / "RELATORIO_TECNICO.md"
DESTINO = PASTA / "RELATORIO_TECNICO.pdf"

estilos_base = getSampleStyleSheet()
estilos = {
    "title": ParagraphStyle(
        "ReportTitle", parent=estilos_base["Title"], fontName="Helvetica-Bold",
        fontSize=22, leading=27, textColor=colors.HexColor("#174A45"),
        alignment=TA_CENTER, spaceAfter=14,
    ),
    "subtitle": ParagraphStyle(
        "ReportSubtitle", parent=estilos_base["Normal"], fontName="Helvetica",
        fontSize=12, leading=17, textColor=colors.HexColor("#3D5551"),
        alignment=TA_CENTER, spaceAfter=12,
    ),
    "h2": ParagraphStyle(
        "ReportH2", parent=estilos_base["Heading2"], fontName="Helvetica-Bold",
        fontSize=15, leading=19, textColor=colors.HexColor("#174A45"),
        spaceBefore=4, spaceAfter=11,
    ),
    "h3": ParagraphStyle(
        "ReportH3", parent=estilos_base["Heading3"], fontName="Helvetica-Bold",
        fontSize=11, leading=14, textColor=colors.HexColor("#9A542A"),
        spaceBefore=9, spaceAfter=5,
    ),
    "body": ParagraphStyle(
        "ReportBody", parent=estilos_base["BodyText"], fontName="Helvetica",
        fontSize=9.5, leading=14, textColor=colors.HexColor("#202B2A"),
        alignment=TA_LEFT, spaceAfter=7,
    ),
    "bullet": ParagraphStyle(
        "ReportBullet", parent=estilos_base["BodyText"], fontName="Helvetica",
        fontSize=9.2, leading=13, leftIndent=14, firstLineIndent=-9,
        textColor=colors.HexColor("#202B2A"), spaceAfter=4,
    ),
    "code": ParagraphStyle(
        "ReportCode", parent=estilos_base["Code"], fontName="Courier",
        fontSize=8.3, leading=11, leftIndent=8, rightIndent=8,
        backColor=colors.HexColor("#F0F4F2"), borderColor=colors.HexColor("#CCD8D3"),
        borderWidth=0.5, borderPadding=7, spaceBefore=4, spaceAfter=9,
    ),
}


def converter_inline(texto):
    texto = escape(texto)
    texto = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", texto)
    texto = re.sub(r"`(.+?)`", r'<font name="Courier">\1</font>', texto)
    texto = re.sub(
        r"(https?://[^\s&lt;&gt;]+)",
        r'<link href="\1" color="#176B87">\1</link>',
        texto,
    )
    return texto


def desenhar_pagina(canvas, documento):
    canvas.saveState()
    largura, altura = A4
    canvas.setStrokeColor(colors.HexColor("#D4DFDA"))
    canvas.line(18 * mm, altura - 17 * mm, largura - 18 * mm, altura - 17 * mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#526661"))
    canvas.drawString(18 * mm, altura - 13 * mm, "MGPEB | Aurora Siger | Relatório técnico")
    canvas.line(18 * mm, 15 * mm, largura - 18 * mm, 15 * mm)
    canvas.drawRightString(largura - 18 * mm, 10 * mm, f"Página {documento.page}")
    canvas.restoreState()


def gerar():
    texto = FONTE.read_text(encoding="utf-8")
    documento = SimpleDocTemplate(
        str(DESTINO), pagesize=A4,
        rightMargin=20 * mm, leftMargin=20 * mm,
        topMargin=23 * mm, bottomMargin=22 * mm,
        title="MGPEB - Relatório técnico",
        author="Equipe Aurora Siger",
    )
    elementos = []
    paragrafo = []
    em_codigo = False
    linhas_codigo = []

    def fechar_paragrafo():
        if paragrafo:
            conteudo = " ".join(item.strip() for item in paragrafo)
            elementos.append(Paragraph(converter_inline(conteudo), estilos["body"]))
            paragrafo.clear()

    for linha in texto.splitlines():
        if linha.strip() == "<!-- PAGE BREAK -->":
            fechar_paragrafo()
            elementos.append(PageBreak())
            continue
        if linha.strip().startswith("```"):
            fechar_paragrafo()
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
        if not linha.strip():
            fechar_paragrafo()
        elif linha.startswith("# "):
            fechar_paragrafo()
            elementos.append(Spacer(1, 38 * mm))
            elementos.append(Paragraph(converter_inline(linha[2:]), estilos["title"]))
        elif linha.startswith("## "):
            fechar_paragrafo()
            estilo = estilos["subtitle"] if len(elementos) < 4 else estilos["h2"]
            elementos.append(Paragraph(converter_inline(linha[3:]), estilo))
        elif linha.startswith("### "):
            fechar_paragrafo()
            elementos.append(Paragraph(converter_inline(linha[4:]), estilos["h3"]))
        elif linha.startswith("- "):
            fechar_paragrafo()
            elementos.append(Paragraph("• " + converter_inline(linha[2:]), estilos["bullet"]))
        elif re.match(r"^\d+\. ", linha):
            fechar_paragrafo()
            elementos.append(Paragraph(converter_inline(linha), estilos["bullet"]))
        else:
            paragrafo.append(linha)
    fechar_paragrafo()
    documento.build(elementos, onFirstPage=desenhar_pagina, onLaterPages=desenhar_pagina)
    print(f"PDF gerado: {DESTINO.name} ({documento.page} páginas)")


if __name__ == "__main__":
    gerar()
