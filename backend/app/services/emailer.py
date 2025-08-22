import smtplib
from email.message import EmailMessage
import os

def send_email(to_email: str, subject: str, body: str, file_path: str = None):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = os.getenv("SMTP_USER")
    msg["To"] = to_email
    msg.set_content(body)

    if file_path and os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        msg.add_attachment(data, maintype="application", subtype="octet-stream", filename=os.path.basename(file_path))

    with smtplib.SMTP_SSL(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as smtp:
        smtp.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        smtp.send_message(msg)