import smtplib
from email.mime.text import MIMEText
from src.utils.settings import settings


def email_utility(
        email_to:str,
        email_subject:str,
        email_body:str
):
    
    msg=MIMEText(email_body)
    msg["Subject"]=email_subject
    msg["From"]=settings.EMAIL_FROM
    msg["To"]=email_to

    try:
         with smtplib.SMTP(
              settings.EMAIL_HOST,
              settings.EMAIL_PORT,
              ) as server:
                   server.ehlo()
                   server.starttls()
                   server.ehlo()
                   server.login(
                   settings.EMAIL_USER,
                   settings.EMAIL_PASSWORD
              )
                   server.send_message(msg)
                   return True
    except Exception as e:
          raise e
     

