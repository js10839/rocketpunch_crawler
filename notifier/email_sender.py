import smtplib
from email.message import EmailMessage

def send_email_with_attachment(to_email: str, subject: str, body: str, file_path: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "jjjr0617@gmail.com"
    msg["To"] = to_email
    msg.set_content(body)

    with open(file_path, "rb") as f:
        file_data = f.read()
        file_name = f.name
    msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    # SMTP 서버 설정 (예: Gmail)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("jjjr0617@gmail.com", "kphp jmhg auqn qenj")
        smtp.send_message(msg)