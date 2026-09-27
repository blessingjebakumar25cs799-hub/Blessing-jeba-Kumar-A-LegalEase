from io import BytesIO
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from fpdf import FPDF


ROOT = Path(__file__).resolve().parents[2]

LOGO_PATH = ROOT / "assets" / "logo.png"


def _lines(text: str) -> list[str]:
    return [
        line.strip()
        for line in text.splitlines()
    ]


def _is_heading(line: str) -> bool:

    if not line:
        return False

    if line.isupper() and len(line) < 140:
        return True

    if line[:2].isdigit() and "." in line[:5]:
        return True

    return line.startswith(
        (
            "ARTICLE ",
            "SECTION ",
            "RECITALS",
            "PARTIES",
            "SIGNATURES",
        )
    )


def format_docx(
    text: str,
    doc_type: str,
) -> bytes:

    doc = Document()

    section = doc.sections[0]

    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.85)
    section.right_margin = Inches(0.85)

    styles = doc.styles

    styles["Normal"].font.name = "Times New Roman"
    styles["Normal"].font.size = Pt(11)

    if LOGO_PATH.exists():

        paragraph = doc.add_paragraph()

        paragraph.alignment = (
            WD_ALIGN_PARAGRAPH.CENTER
        )

        paragraph.add_run().add_picture(
            str(LOGO_PATH),
            width=Inches(1.35),
        )

    title = doc.add_paragraph()

    title.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )

    run = title.add_run(
        doc_type.upper()
    )

    run.bold = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(16)

    for line in _lines(text):

        if not line:
            doc.add_paragraph()
            continue

        paragraph = doc.add_paragraph()

        paragraph.paragraph_format.space_after = Pt(6)

        if _is_heading(line):

            run = paragraph.add_run(line)

            run.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)

        else:
            paragraph.add_run(line)

    footer = section.footer.paragraphs[0]

    footer.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )

    footer.add_run(
        "LegalEase | Draft document - "
        "review by a qualified legal professional recommended."
    )

    output = BytesIO()

    doc.save(output)

    return output.getvalue()


class LegalPDF(FPDF):

    def __init__(
        self,
        logo_path: Path | None = None,
    ):
        super().__init__()
        self.logo_path = logo_path

    def header(self):

        if (
            self.logo_path
            and self.logo_path.exists()
        ):

            try:
                self.image(
                    str(self.logo_path),
                    x=88,
                    y=8,
                    w=34,
                )

                self.ln(20)

            except Exception:
                self.ln(8)

        else:
            self.ln(8)

    def footer(self):

        self.set_y(-15)

        self.set_font(
            "Helvetica",
            size=8,
        )

        self.cell(
            0,
            8,
            "LegalEase | Draft - review by a "
            "qualified legal professional recommended.",
            align="C",
        )


def format_pdf(
    text: str,
    doc_type: str,
) -> bytes:

    pdf = LegalPDF(
        LOGO_PATH
        if LOGO_PATH.exists()
        else None
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=20,
    )

    pdf.add_page()

    pdf.set_font(
        "Helvetica",
        "B",
        15,
    )

    pdf.cell(
        0,
        10,
        doc_type.upper(),
        align="C",
    )

    pdf.ln(14)

    for line in _lines(text):

        if not line:
            pdf.ln(4)
            continue

        if _is_heading(line):

            pdf.set_font(
                "Helvetica",
                "B",
                11,
            )

            pdf.multi_cell(
                0,
                7,
                line,
            )

        else:

            pdf.set_font(
                "Helvetica",
                size=10,
            )

            pdf.multi_cell(
                0,
                6,
                line,
            )

        pdf.ln(1)

    return bytes(pdf.output())


def format_html_preview(text: str) -> str:

    import html

    blocks = []

    for raw in _lines(text):

        if not raw:
            continue

        safe = html.escape(raw)

        if _is_heading(raw):

            blocks.append(
                f"<h3>{safe}</h3>"
            )

        else:

            blocks.append(
                f"<p>{safe}</p>"
            )

    return """
    <div style="
        background:#111827;
        color:#f9fafb;
        padding:24px;
        border-radius:14px;
        border:1px solid #374151;
        max-height:620px;
        overflow-y:auto;
        font-family:Georgia,'Times New Roman',serif;
        line-height:1.65;
    ">
    """ + "\n".join(blocks) + """
    </div>
    """