"""
PDF Export Service — converts Markdown resume to a downloadable PDF.
Uses markdown2 for HTML conversion and xhtml2pdf (pisa) for PDF rendering.
Falls back to plain-text PDF if CSS rendering isn't available.
"""
import io
import markdown2

# ── PDF CSS Styling ────────────────────────────────────────────────────────────
RESUME_CSS = """
@page {
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
}

body {
    font-family: 'Helvetica', 'Arial', sans-serif;
    font-size: 12pt;
    line-height: 1.5;
    color: #000000;
}

h1 {
    font-size: 13pt;
    color: #000000;
    font-weight: bold;
    border-bottom: 2px solid #000000;
    padding-bottom: 4px;
    margin-bottom: 6px;
}

h2 {
    font-size: 13pt;
    color: #000000;
    font-weight: bold;
    border-bottom: 1px solid #cccccc;
    margin-top: 14px;
    margin-bottom: 4px;
}

h3 {
    font-size: 13pt;
    color: #000000;
    font-weight: bold;
    margin-bottom: 2px;
}

ul {
    margin-top: 2px;
    padding-left: 20px;
}

li {
    margin-bottom: 2px;
}

p {
    margin: 4px 0;
}

hr {
    border: none;
    border-top: 1px solid #e0e0e0;
    margin: 8px 0;
}

strong {
    color: #1e3a5f;
}

a {
    color: #1e3a5f;
    text-decoration: none;
}
"""


def markdown_to_pdf(markdown_text: str) -> bytes:
    """
    Convert a Markdown-formatted resume to a styled PDF.

    Args:
        markdown_text: Resume content in Markdown format

    Returns:
        PDF file as bytes

    Raises:
        RuntimeError: If PDF generation fails
    """
    # Step 1: Convert Markdown → HTML
    html_body = markdown2.markdown(
        markdown_text,
        extras=["tables", "fenced-code-blocks", "strike", "header-ids"]
    )

    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <style>{RESUME_CSS}</style>
</head>
<body>
{html_body}
</body>
</html>"""

    # Step 2: HTML → PDF using xhtml2pdf (pisa)
    try:
        from xhtml2pdf import pisa

        pdf_buffer = io.BytesIO()
        pisa_status = pisa.CreatePDF(
            src=full_html,
            dest=pdf_buffer,
            encoding='utf-8'
        )

        if pisa_status.err:
            raise RuntimeError(f"PDF generation error: {pisa_status.err}")

        pdf_buffer.seek(0)
        return pdf_buffer.read()

    except ImportError:
        # Fallback: use reportlab for basic text-only PDF
        return _fallback_reportlab_pdf(markdown_text)


def _fallback_reportlab_pdf(markdown_text: str) -> bytes:
    """
    Fallback PDF generator using reportlab if xhtml2pdf is unavailable.
    Produces a simple plain-text PDF.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.enums import TA_LEFT

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=15*mm,
            leftMargin=15*mm,
            topMargin=20*mm,
            bottomMargin=20*mm
        )
        styles = getSampleStyleSheet()
        story = []

        heading_style = ParagraphStyle(
            'Heading', parent=styles['Heading1'],
            textColor=colors.black, fontSize=13, fontName='Helvetica-Bold'
        )
        body_style = ParagraphStyle(
            'Body', parent=styles['Normal'],
            fontSize=12, leading=14, textColor=colors.black
        )

        for line in markdown_text.splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                story.append(Paragraph(stripped[2:], heading_style))
                story.append(Spacer(1, 4*mm))
            elif stripped.startswith("## "):
                story.append(Paragraph(stripped[3:], heading_style))
                story.append(Spacer(1, 2*mm))
            elif stripped.startswith("### "):
                story.append(Paragraph(stripped[4:], heading_style))
            elif stripped.startswith("- ") or stripped.startswith("* "):
                story.append(Paragraph(f"• {stripped[2:]}", body_style))
            elif stripped:
                story.append(Paragraph(stripped, body_style))
            else:
                story.append(Spacer(1, 3*mm))

        doc.build(story)
        buffer.seek(0)
        return buffer.read()

    except Exception as e:
        raise RuntimeError(f"Both PDF backends failed. Error: {str(e)}")
