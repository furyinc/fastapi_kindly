import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config

# SMTP configuration
EMAIL_HOST = 'smtp.gmail.com'  # Gmail's SMTP host
EMAIL_PORT = 587  # Port for STARTTLS
EMAIL_USER = 'frilancer029@gmail.com'  # Your email address
EMAIL_PASSWORD = 'xcqv dedl qget cquo'  # Your email account password or app-specific password

def send_email(to_email: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()  # Start TLS encryption
            server.login(EMAIL_USER, EMAIL_PASSWORD)  # Log in to the email account
            server.send_message(msg)  # Send the email
        print("Email sent successfully")
    except Exception as e:
        print("Failed to send email:", e)

