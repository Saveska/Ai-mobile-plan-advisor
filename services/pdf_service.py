from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER


class PDFReportBuilder:
    """
    Responsible for generating a professional PDF report.
    All PDF layout and styling logic is encapsulated here.
    """

    def __init__(self):
        self.styles = getSampleStyleSheet()

        # Customize styles for consistency
        self.styles["Title"].alignment = TA_CENTER
        self.styles["Title"].fontSize = 20
        self.styles["Title"].spaceAfter = 20

        self.styles["Heading2"].fontSize = 14
        self.styles["Heading2"].spaceAfter = 12

        self.styles["BodyText"].leading = 14
        self.styles["BodyText"].spaceAfter = 6

    def build(self, offers: list, analysis_text: str) -> BytesIO:
        """
        Builds and returns a PDF buffer containing the offer comparison report.
        A new buffer is created on every call so reports never overwrite each other.
        """
        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            topMargin=0.75 * inch,
            bottomMargin=1 * inch
        )

        story = []

        # Title
        story.append(Paragraph("Offer Analysis Report", self.styles["Title"]))
        story.append(Spacer(1, 0.25 * inch))

        # Comparison Table
        story.append(Paragraph("Side-by-Side Offer Comparison", self.styles["Heading2"]))
        story.append(self._build_offer_table(offers))
        story.append(Spacer(1, 0.5 * inch))

        # AI Analysis
        story.append(Paragraph("Expert Analysis & Conclusion", self.styles["Heading2"]))

        for line in analysis_text.split("\n"):
            if line.strip():
                story.append(Paragraph(line, self.styles["BodyText"]))

        doc.build(
            story,
            onFirstPage=self._draw_page_number,
            onLaterPages=self._draw_page_number
        )

        buffer.seek(0)
        return buffer

    def _draw_page_number(self, canvas, doc):
        """
        Adds a page number to the bottom of each page.
        """
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.drawString(letter[0] - inch, 0.75 * inch, f"Page {doc.page}")
        canvas.restoreState()

    def _build_offer_table(self, offers: list) -> Table:
        """
        Creates a styled comparison table for the two offers.
        """
        headers = ["Feature", offers[0]["OfferName"], offers[1]["OfferName"]]
        rows = [headers]

        ordered_keys = ["Internet", "Minutes_x0026_SMS", "Safe", "Roaming", "Price"]

        for key in ordered_keys:
            label = "Minutes & SMS" if key == "Minutes_x0026_SMS" else key
            rows.append([label, offers[0].get(key, "N/A"), offers[1].get(key, "N/A")])

        table = Table(rows, colWidths=[1.5 * inch, 2.5 * inch, 2.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F81BD')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ]))

        return table