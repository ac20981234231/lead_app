import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")
ATTORNEY_EMAIL = os.getenv("ATTORNEY_EMAIL")

def send_email(to: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = to
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.sendmail(EMAIL_FROM, to, msg.as_string())
            print(f"Email sent to {to}")
    except Exception as e:
        print(f"Failed to send email to {to}: {e}")

def send_email_to_prospect(email: str):
    subject = "Thank you for your submission"
    body = "Dear Prospect,\n\nThank you for your submission. We will get back to you soon.\n\nBest regards,\nCompany Name"
    send_email(email, subject, body)

def send_email_to_attorney(prospect_email: str):
    subject = "New Lead Submission"
    body = f"Dear Attorney,\n\nA new lead has been submitted by {prospect_email}. Please review it.\n\nBest regards,\nCompany Name"
    send_email(ATTORNEY_EMAIL, subject, body)
