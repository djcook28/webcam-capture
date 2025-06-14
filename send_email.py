import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import imghdr

PASSWORD = os.environ.get("pythonGmailPass")
host = "smtp.gmail.com"
port = 587

load_dotenv()
SENDER = os.getenv("SENDER")

RECEIVER = SENDER
def send_email(image_path):
    email_message = format_email(image_path)

    gmail = smtplib.SMTP(host, port)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()

def format_email(image_path):
    message = EmailMessage()
    message["Subject"] = "New movement detected"
    message.set_content("New distinct movement detected")

    with open(image_path, "rb") as file:
        content = file.read()

    message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))
    return message