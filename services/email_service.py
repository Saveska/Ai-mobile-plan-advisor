import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText


def send_email_with_pdf(to_address, pdf_buffer, config) -> bool:
    """
    Sends the generated PDF report as an email attachment.
    """
    msg = MIMEMultipart()
    msg["From"] = config.EMAIL_USER
    msg["To"] = to_address
    msg["Subject"] = "Your Offer Analysis Report"

    msg.attach(MIMEText(
        "Please find your personalized offer analysis report attached.",
        "plain"
    ))

    attachment = MIMEApplication(pdf_buffer.getvalue(), _subtype="pdf")
    attachment.add_header(
        "Content-Disposition",
        "attachment",
        filename="Offer_Analysis_Report.pdf"
    )
    msg.attach(attachment)

    try:
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception:
        return False
