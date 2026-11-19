import json
from flask import Flask, request, jsonify, send_file

from config import Config
from services.ai_service import AIComparisonService
from services.pdf_service import PDFReportBuilder
from services.email_service import send_email_with_pdf
from utils import clean_ai_output

app = Flask(__name__)

ai_service = AIComparisonService(Config.GROQ_API_KEY)
pdf_builder = PDFReportBuilder()

PDF_CACHE = {}  # simple in-memory cache for generated PDFs


@app.route("/generate_pdf", methods=["POST"])
def generate_pdf():
    """
    Generates a PDF report based on selected offers and user priority.
    """
    data = request.json

    offers = json.loads(data.get("offers", "[]"))
    priority = data.get("priority")

    if not offers or not priority:
        return jsonify({"error": "Missing offers or priority"}), 400

    ai_text = ai_service.compare_offers(offers, priority)
    formatted_text = clean_ai_output(ai_text, offers)

    pdf_buffer = pdf_builder.build(offers, formatted_text)
    PDF_CACHE["latest"] = pdf_buffer

    return jsonify({"message": "PDF generated successfully"}), 200


@app.route("/send_email", methods=["POST"])
def send_email():
    """
    Emails the most recently generated PDF report.
    """
    email = request.json.get("email")

    if not email or "latest" not in PDF_CACHE:
        return jsonify({"error": "No PDF available"}), 400

    success = send_email_with_pdf(email, PDF_CACHE["latest"], Config)

    if not success:
        return jsonify({"error": "Failed to send email"}), 500
    return jsonify({"sent": True}), 200


@app.route("/download_pdf", methods=["GET"])
def download_pdf():
    """
    Allows manual PDF download if needed.
    """
    if "latest" not in PDF_CACHE:
        return jsonify({"error": "No PDF generated"}), 404

    return send_file(
        PDF_CACHE["latest"],
        as_attachment=True,
        download_name="Offer_Analysis_Report.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
