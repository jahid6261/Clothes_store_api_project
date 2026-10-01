import smtplib
from email.mime.text import MIMEText

from src.utils.settings import settings


def email_utility(
    email_to: str,
    email_subject: str,
    email_body: str,
) -> None:

    message = MIMEText(email_body, "plain", "utf-8")

    message["Subject"] = email_subject
    message["From"] = settings.EMAIL_FROM
    message["To"] = email_to

    with smtplib.SMTP(
        settings.EMAIL_HOST,
        settings.EMAIL_PORT,
        timeout=30,
    ) as server:

        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(
            settings.EMAIL_USER,
            settings.EMAIL_PASSWORD,
        )

        server.send_message(message)