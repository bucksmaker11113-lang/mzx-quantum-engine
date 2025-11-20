# backend/utils/mailer.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class Mailer:
    def __init__(self):
        self.sender = os.getenv("SMTP_EMAIL", "")
        self.password = os.getenv("SMTP_PASS", "")
        self.server = "smtp.gmail.com"
        self.port = 587

    def send(self, target: str, subject: str, message: str):
        if not self.sender or not self.password:
            return {"error": "SMTP credentials missing"}

        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["To"] = target
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        try:
            with smtplib.SMTP(self.server, self.port) as smtp:
                smtp.starttls()
                smtp.login(self.sender, self.password)
                smtp.send_message(msg)
            return {"sent": True}
        except Exception as e:
            return {"error": str(e)}

mailer = Mailer()