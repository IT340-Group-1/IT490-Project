import email.message
import smtplib
from .cred import get_credentials

smtp_user, smtp_password = get_credentials('craappgoogle.txt')

def send_email_smtp(receiver, subject, body):
    msg = email.message.Message()
    msg['From'] = smtp_user
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.add_header('Content-Type','text/html')
    msg.set_payload(body)

    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.starttls()
    smtp_server.login(smtp_user, smtp_password)
    smtp_server.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_server.quit()