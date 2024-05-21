import os
from dotenv import load_dotenv
from email_service import send_email

# Load environment variables
load_dotenv()

# Fetch the test email address from .env
TEST_EMAIL = os.getenv("TEST_EMAIL")

# Define the test email subject and body
subject = "Test Email"
body = "This is a test email from FastAPI."

# Send the test email
try:
    send_email(TEST_EMAIL, subject, body)
    print(f"Test email sent to {TEST_EMAIL}")
except Exception as e:
    print(f"Failed to send test email: {e}")
